""" 
Tadqeeq - Image Annotator Tool
An interactive image annotation tool for efficient labeling.
Developed by Mohamed Behery @ RTR Software Development (2025-04-27).
Licensed under the MIT License.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox, QShortcut
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QKeySequence, QFont
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint
import numpy as np
import os
from functools import reduce
from collections.abc import Iterable
from skimage.io import imsave
from skimage.transform import resize
from skimage.feature import canny
from scipy.ndimage import binary_fill_holes

from .utils import compute_segment_areas, rgba_array_to_pixmap, \
                   apply_lut_replacement, detect_overlapping_boxes_to_clean, \
                   mask_to_bounding_box, pixmap_to_rgba_array, \
                   locate_all_pixels_via_floodfill
                  
from warnings import filterwarnings
filterwarnings('ignore', category=UserWarning, message='.*low contrast image.*')

class ImageAnnotator(QWidget):
    
    """
    Interactive PyQt5 widget for image annotation using segmentation masks or bounding boxes.

    Parameters:
        image_path (str): Path to the input image.
        annotation_path (str): Path to save/load annotations (.npy, .png, or .txt).
        void_background (bool): Whether to treat background as a void region (labelled 255) or not.
        autosave (bool): Automatically save annotations after each edit.
        key_sequence_to_save (str): Keyboard shortcut to manually trigger saving (default: "Ctrl+S").
        minimum_pen_width (int): Minimum width of the drawing pen.
        minimum_font_size (int): Minimum font size for floating label displays.
        hsv_offsets (tuple): Starting HSV offsets for label color generation.
        opacity (float): Opacity of drawn segmentation masks.
        label_slider_sensitivity (float): Scroll sensitivity for switching between labels.
        label_color_pairs (int): Number of label-color pairs to support.
        pen_width_slider_sensitivity (float): Sensitivity for adjusting pen width via scroll.
        maximum_pen_width_multiplier (float): Maximum multiplier allowed for pen width.
        floating_label_display_offsets (tuple): (x, y) pixel offset for floating label placement.
        bounding_box_side_length_thresholds (tuple): Min and max allowed bounding box side lengths.
        overlap_vs_smallest_area_threshold (float): Overlap threshold for suppressing small box collisions.
        overlap_vs_union_area_threshold (float): Overlap threshold for suppressing boxes using union ratio.
        corner_label_attached_to_bounding_box (bool): Whether labels appear attached to bounding box corners.
        verbose (bool): Enables logging and debug prints if True.
    """
    
    __RESIZE_DELAY = 200
    
    def __init__(self, 
                 image_path, 
                 annotation_path,
                 void_background=False,
                 autosave=True,
                 key_sequence_to_save='Ctrl+S',
                 minimum_pen_width=4,
                 minimum_font_size=16,
                 hsv_offsets=(0,255,200), 
                 opacity=0.5,
                 label_slider_sensitivity=0.30,
                 label_color_pairs=32,
                 pen_width_slider_sensitivity=0.05,
                 maximum_pen_width_multiplier=4.0,
                 floating_label_display_offsets=(15,30),
                 bounding_box_side_length_thresholds=(25,2000),
                 overlap_vs_smallest_area_threshold=0.95,
                 overlap_vs_union_area_threshold=0.95,
                 corner_label_attached_to_bounding_box=True,
                 verbose=True):
        
        def configure_verbosity():
            self.__verbose = verbose
            self.__previous_message = ''
        
        def disable_maximize_button():
            nonlocal self
            self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
        def configure_resize_scheduler():
            nonlocal self
            self.__resize_scheduler = QTimer(self)
            self.__resize_scheduler.setSingleShot(True)
            self.__resize_scheduler.timeout.connect(self.__resize_user_interface_update_routine)
            self.__resize_flag = False
            
        def configure_saving_parameters():
            nonlocal self, key_sequence_to_save, autosave
            key_sequence_to_save = QKeySequence(key_sequence_to_save)
            self.__key_sequence_to_save = QShortcut(key_sequence_to_save, self)
            self.__key_sequence_to_save.activated.connect(self.save)
            self.__autosave = autosave
            
        def configure_displays():
            nonlocal self
            self.__image_display = QLabel(self)
            self.__label_to_annotate_display = QLabel('Label: N/A', self)
            self.__label_annotated_display = QLabel('Label: N/A', self)
            self.__minimum_widget_size_set = False
            self.floating_label_display_offsets = floating_label_display_offsets
            self.__label_index_hovered_over = -1
            self.__label_displays_configuration_complete = False
            
        def initialize_annotation_pen():
            nonlocal self, minimum_pen_width
            self.__annotation_pen = QPen(Qt.black, minimum_pen_width, Qt.SolidLine)
            self.last_pen_position = None
            self.__erasing = False
        
        def configure_annotation_parameters():
            nonlocal self, minimum_pen_width, minimum_font_size, hsv_offsets, opacity
            self.__minimum_pen_width = minimum_pen_width
            self.__label_font_size = minimum_font_size
            self.__hsv_offsets = hsv_offsets
            self.__opacity = opacity
            self.__void_background = void_background
            
        def configure_bounding_boxes():
            self.__use_bounding_boxes = os.path.splitext(annotation_path)[-1].lower().strip() == '.txt'
            self.__bounding_box_side_length_thresholds = bounding_box_side_length_thresholds
            self.__overlap_vs_smallest_area_threshold = overlap_vs_smallest_area_threshold
            self.__overlap_vs_union_area_threshold = overlap_vs_union_area_threshold
            self.__corner_label_attached_to_bounding_box = corner_label_attached_to_bounding_box
        
        def initialize_sliders():
            self.__label_slider_enabled = True
            self.__pen_width_slider_sensitivity = pen_width_slider_sensitivity
            self.maximum_pen_width_multiplier = maximum_pen_width_multiplier
            self.pen_width_multiplier_accumulator = 0.0
            self.__label_slider_sensitivity = label_slider_sensitivity
            self.label_color_pairs = label_color_pairs
            self.label_index_accumulator = 0.0
        
        def load_image_annotation_pair():
            self.image_path = image_path
            self.annotation_path = annotation_path
            
        def enable_mouse_tracking():
            self.setMouseTracking(True)
            self.__image_display.setMouseTracking(True)
            self.__label_to_annotate_display.setMouseTracking(True)
            self.__label_annotated_display.setMouseTracking(True)

        super().__init__()
        
        configure_verbosity()
        disable_maximize_button()
        configure_resize_scheduler()
        configure_saving_parameters()
        configure_displays()
        initialize_annotation_pen()
        configure_annotation_parameters()
        configure_bounding_boxes()
        initialize_sliders()
        load_image_annotation_pair()
        enable_mouse_tracking()
        
    @property
    def void_background(self):
        """Indicates whether the background is treated as a void class, labelled 255."""
        return self.__void_background
        
    @property
    def RESIZE_DELAY(cls):
        return cls.__RESIZE_DELAY
        
    @property
    def last_pen_position(self):
        return self.__last_pen_position
    
    @last_pen_position.setter
    def last_pen_position(self, value:QPoint):
        self.__last_pen_position = value
        self.__update_yx_cursor_within_original_image(value)
        
    @property
    def maximum_pen_width_multiplier(self):
        return self.__maximum_pen_width_multiplier
    
    @maximum_pen_width_multiplier.setter
    def maximum_pen_width_multiplier(self, value):
        self.__maximum_pen_width_multiplier = value
    
    @property
    def verbose(self):
        """Returns the current verbosity setting."""
        return self.__verbose
        
    @property
    def erasing(self):
        """Returns whether erasing mode is currently active."""
        return self.__erasing
    
    @property
    def floating_label_display_offsets(self):
        """Returns floating label display pixel offsets."""
        return self.__floating_label_display_offsets
    
    @floating_label_display_offsets.setter
    def floating_label_display_offsets(self, value):
        """
        Sets the floating label display pixel offsets.

        This setter method updates the pixel offsets for displaying floating 
        labels on the image. The provided value sets the position of the floating 
        labels. If the value is non-empty or non-zero, it enables floating label 
        display. Otherwise, it disables the floating label feature.
        Args:
            value: The pixel offsets (e.g., a tuple or array) for positioning 
                   floating labels on the image. If the value is empty or zero, 
                   floating labels will be disabled.
        """
        self.__floating_label_display_offsets = value
        self.__is_floating_label = bool(self.__floating_label_display_offsets)
    
    @property
    def image_path(self):
        """Returns the currently loaded image as QPixmap."""
        return self.__image_path
    
    @image_path.setter
    def image_path(self, value:str):
        """Sets a new QPixmap image and rescale."""
        self.__image_path = value
        self.image = QPixmap(value)
        
    @property
    def label_index_to_annotate(self):
        """Returns the index of the label currently selected for annotation."""
        return self.__label_index_to_annotate
    
    @label_index_to_annotate.setter
    def label_index_to_annotate(self, value:int):
        """
        Sets the label index for annotation.
        
        This setter method updates the label that is currently selected for 
        annotating objects in the image. The provided index is used to select 
        the appropriate label from the internal list of labels. Additionally, 
        the annotation pen color is updated to match the color associated with 
        the selected label.
        """
        self.__label_index_to_annotate = value
        self.__label_to_annotate = self.labels[value]
        self.__label_to_annotate_color = self.label_colors[value]
        
    @property
    def label_to_annotate_color(self):
        """Returns the label color currently selected for annotation."""
        return self.__label_to_annotate_color
        
    @property
    def label_to_annotate(self):
        """Returns the label currently selected for annotation."""
        return self.__label_to_annotate
        
    @property
    def is_floating_label(self):
        """Returns whether floating label display mode is active."""
        return self.__is_floating_label
    
    @property
    def label_color_pairs(self):
        return self.__label_color_pairs
    
    @label_color_pairs.setter
    def label_color_pairs(self, value):
        """
        Sets the dictionary of label-color pairs and adjusts internal label and color mappings.
        
        This setter method:
        - Accepts a dictionary or iterable input and sets it to the internal `__label_color_pairs` attribute.
        - If the input is a dictionary, it directly updates the `__label_color_pairs`, `__labels`, and `__label_colors` attributes.
        - If the input is an iterable (e.g., list of labels), it automatically generates corresponding colors based on the label indices.
        - If the input is an integer, it generates labels from `0` to `value-1` and assigns unique colors to each label.
        - If the input format is invalid, it raises a `ValueError` indicating that the input should either be an iterable or an integer.
        
        Args:
            value (dict, Iterable, int): 
                - A dictionary of label-color pairs (label: color), 
                - A list of labels to generate colors for, 
                - Or an integer specifying the number of labels to generate with sequential numeric values.
        
        Raises:
            ValueError: If the input is neither an iterable nor an integer.
        """
        try:
            self.__label_color_pairs = dict(value)
            self.__labels = list(self.__label_color_pairs.keys())
            self.__label_colors = list(self.__label_color_pairs.values())
            self.__n_labels = len(self.__labels)
        except (ValueError, TypeError):
            if isinstance(value, Iterable):
                self.labels = list(value)
            elif type(value) is int:
                self.labels = list(range(value))
            else:
                raise ValueError('`labels` should either be `Iterable` or `int`.')
                
    @property
    def labels(self):
        return self.__labels
    
    @labels.setter
    def labels(self, value:list):
        """
        Sets the list of labels and generates corresponding colors for each label.
        
        This setter method:
        - Accepts a list of labels and sets it to the internal `__labels` attribute.
        - Calculates the number of labels (`__n_labels`) from the length of the provided list.
        - Generates a unique color for each label using a color model based on HSV (Hue, Saturation, Value).
        - Maps each label to its corresponding color and stores them in `__label_color_pairs`.
        
        Args:
            value (list): The list of labels to set.
        
        Notes:
            - The color for each label is generated based on its index using a specific HSV color scheme.
            - The generated colors are stored in the internal attributes (`__label_colors`, `__label_color_pairs`).
        """
        def color_from_label_index(index):
            hsv_bin_sizes = (255 - np.array(self.__hsv_offsets)) // self.__n_labels
            h, s, v = map(lambda a, b: a * index + b, hsv_bin_sizes, self.__hsv_offsets)
            return QColor.fromHsv(h, s, v)
        
        self.__labels = value
        self.__n_labels = len(value)
        self.__label_colors = [color_from_label_index(index) for index in range(self.__n_labels)]
        self.__label_color_pairs = dict(zip(self.__labels, self.__label_colors))
    
    @property
    def label_colors(self):
        """Get the list of colors assigned to each label."""
        return self.__label_colors
    
    @property
    def n_labels(self):
        """Get the total number of labels."""
        return self.__n_labels
    
    @property
    def corner_label_attached_to_bounding_box(self):
        """Check if the corner label is attached to the bounding box."""
        return self.__corner_label_attached_to_bounding_box
        
    @property
    def image(self):
        """Get the currently loaded image."""
        return self.__image
    
    @image.setter
    def image(self, value:QPixmap):
        """
        Sets the image and adjusts the internal parameters based on the new image.
        
        This setter method:
        - Sets the internal `__image` attribute to the provided `QPixmap`.
        - Stores the original shape of the image in `__original_array_shape` (height and width).
        - If the provided `QPixmap` is null (doesn't exist in `image_path`), a blank white image is created to ensure a valid image is set.
        - Calculates the `__scale_factor` based on the current widget size and the image width.
        - Scales the image to fit the widget size while maintaining the aspect ratio, using smooth transformation.
        - Resizes the widget to match the scaled image size.
        
        Args:
            value (QPixmap): The QPixmap representing the new image to set.
        """
        self.__image = value
        self.__original_array_shape = [value.height(), value.width()]
        if value.isNull():
            blank_image = QPixmap(self.size())
            blank_image.fill(Qt.white)
            self.__image = blank_image
        self.__scale_factor = self.width() / self.image.width()
        self.__image = value.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.resize(self.__image.size())
    
    @property
    def annotation_overlay(self):
        """Get the current annotation overlay (QPixmap)."""
        return self.__annotation_overlay
    
    @annotation_overlay.setter
    def annotation_overlay(self, value:QPixmap):
        """
        Sets the annotation layer with the provided QPixmap, resizing it to match the size of the image.
        
        This setter method:
        - Initializes the internal `__annotation_overlay` attribute as a transparent QPixmap with the same size as the image.
        - Uses a QPainter to draw the provided `value` (a QPixmap) onto the newly created `__annotation_overlay`.
        - The `value` QPixmap is copied onto the transparent layer at position (0, 0), ensuring the annotation layer is correctly aligned with the image.
        
        Args:
            value (QPixmap): The QPixmap to set as the annotation layer. This is drawn onto a transparent QPixmap with the size matching the image.
        
        Notes:
            - The `annotation` layer is reset to a transparent QPixmap each time this setter is called.
            - The method ensures that the annotation is positioned correctly by using QPainter to render the `value` QPixmap.
        """
        self.initialize_overlay('annotation')
        painter = QPainter(self.__annotation_overlay)
        painter.drawPixmap(0, 0, QPixmap(value))
        painter.end()
    
    @property
    def annotation_path(self):
        """Get the path to the annotation file to be used by the CV model."""
        return self.__annotation_path
    
    @annotation_path.setter
    def annotation_path(self, value:str):
        """
        Sets the annotation path, determines the type of annotations (bounding boxes or segment masks),
        and loads the corresponding annotations.
        
        This setter method:
        - Sets the internal `__annotation_path` to the provided value.
        - Determines whether to use bounding boxes or labelled segment masks based on the file extension (`.txt` for bounding boxes, `.npy` for segment masks).
        - If bounding boxes are used:
            - Attempts to read and parse the `.txt` file into bounding box data, storing it in `__bounding_boxes`.
            - Raises an error if the file is empty or cannot be loaded.
        - If labelled segment masks are used:
            - Loads the corresponding `.npy` file containing the segment masks into `labelled_segment_masks`.
        - In case of errors (e.g., file not found, empty file, etc.), logs the error and clears any existing annotations.
        - Calls the `__annotate_user_interface_update_routine` method to refresh the annotations after setting the path.
        
        Args:
            value (str): The file path to the annotation data, either a `.txt` file for bounding boxes or a `.npy` file for labelled segment masks.
        
        Notes:
            - The method differentiates between bounding box annotations and segment mask annotations based on the file extension.
            - If an error occurs while reading the file, the annotations are cleared and a fresh start is initiated.
        """
        self.__annotation_path = value
        self.__use_bounding_boxes = os.path.splitext(value)[-1].lower().strip() == '.txt'
        try:
            if self.__use_bounding_boxes:
                with open(value) as file:
                    lines = file.readlines()
                table = [line.strip().split() for line in lines if line.strip()]
                assert len(table) > 0, 'Empty annotations file...'
                self.__bounding_boxes = np.int32(table)
            else:
                self.__path_to_labelled_segment_masks = os.path.splitext(value)[0] + '.npy'
                self.labelled_segment_masks = np.load(self.__path_to_labelled_segment_masks)
        except FileNotFoundError:
            self.log('No annotations existing, starting afresh...')
            self.__clear_annotations()
        finally:
            self.__annotate_user_interface_update_routine()
            
    @property
    def use_bounding_boxes(self):
        """Get the flag indicating whether bounding boxes are used for annotations."""
        return self.__use_bounding_boxes
        
    @property
    def bounding_boxes(self):
        """Get the bounding boxes used for annotation."""
        return self.__bounding_boxes
    
    @property
    def labelled_segment_masks(self):
        """Get the labelled segment masks for annotations."""
        return self.__labelled_segment_masks
    
    @labelled_segment_masks.setter
    def labelled_segment_masks(self, value:np.ndarray):
        """
        Sets the labelled segment masks, sorts them by segment area, and updates the overall segment mask.
        
        This setter method:
        - Computes the areas of each segment in the provided `value` array using the `compute_segment_areas` function.
        - Sorts the segments by their areas in ascending order.
        - Combines the sorted segment masks into a single mask.
        
        Args:
            value (np.ndarray): A 3D numpy array containing the labelled segment masks.
        """
        areas = compute_segment_areas(value)
        self.__labelled_segment_masks = value[np.argsort(areas)]
        self.__overall_segment_mask = self.__combine_labelled_segment_masks()
    
    @property
    def overall_segment_mask(self):
        """Get the overall segment mask that combines all labelled segment masks."""
        return self.__overall_segment_mask
    
    @property
    def label_index_accumulator(self):
        """Floating-point accumulator for label scrolling."""
        return self.__label_index_accumulator
    
    @label_index_accumulator.setter
    def label_index_accumulator(self, value:float):
        """
        Sets the label index accumulator and updates the active label index for annotation.
        
        Functionality:
        - Wraps the floating-point accumulator value within the total number of labels using modulo.
        - Calculates the integer label index to annotate, with a safeguard against floating-point 
          quantization errors (e.g., ensuring 31.999999... correctly maps to 31 when flooring, not 32).
        - If label slider mode is enabled, logs the label index and corresponding label name.
        
        Parameters:
            value (float): The new value for the label index accumulator, which can be fractional 
                           to allow smooth scrolling or adjustments.
        """
        self.__label_index_accumulator = value % self.n_labels
        self.label_index_to_annotate = int(value % self.n_labels) % self.n_labels # To avoid quantization error issues when flooring (e.g. 31.99999999999 gives 32 not 31)
        if self.__label_slider_enabled: # Not to depend on the order of initialization
            self.log(f'Label Slider: {self.__label_index_accumulator:.2f}: {self.label_index_to_annotate + 1}/{self.n_labels}, {self.label_to_annotate}')
      
    @property
    def pen_width_multiplier_accumulator(self):
        """Floating-point accumulator for pen width scrolling."""
        return self.__pen_width_multiplier_accumulator
    
    @pen_width_multiplier_accumulator.setter
    def pen_width_multiplier_accumulator(self, value:float):
        """
        Sets the pen width multiplier accumulator and updates the effective pen width.
        
        Functionality:
        - Clamps the accumulator value to the [0.0, 1.0] range.
        - Computes the actual pen width multiplier based on the clamped value and the maximum allowed multiplier.
        - Logs the updated pen width multiplier if the label slider mode is not enabled (to avoid unintended logs during initialization or label adjustments).
        
        Parameters:
            value (float): A normalized value (typically between 0 and 1) representing the percentage of desired maximum pen width multiplier to be applied for pen resizing.
        """
        self.__pen_width_multiplier_accumulator = 0.0 if value < 0.0 else 1.0 if value > 1.0 else value
        self.pen_width_multiplier = 1 + self.__pen_width_multiplier_accumulator * (self.maximum_pen_width_multiplier - 1)
        if not self.__label_slider_enabled: # Not to depend on the order of initialization
            self.log(f'Pen Width Slider: {self.pen_width_multiplier:.2f}')
        
    @property
    def pen_width_multiplier(self):
        """The current multiplier applied to the base pen width."""
        return self.__pen_width_multiplier
    
    @pen_width_multiplier.setter
    def pen_width_multiplier(self, value:float):
        """
        Sets the pen width multiplier and resizes the annotation pen accordingly.
    
        Parameters:
            value (float): The new pen width multiplier to apply.
        """
        self.__pen_width_multiplier = value
        self.__resize_pen()
        
    def save(self):
        """
        Saves the current annotations to disk.
    
        Behavior:
        - If using bounding boxes:
            - Saves annotations as a plain text `.txt` file.
            - Each line represents one bounding box, written in space-separated string format.
        - If using segmentation masks:
            - Saves the raw labelled segment masks as a `.npy` file.
            - Computes the overall segment mask and applies label shifting or void boundary tracing
              using `self.postprocess_overall_segment_mask_for_saving()`.
            - Saves the final processed mask as a `.png` image.
    
        Notes:
            - The save directory is automatically created if it does not exist.
            - The postprocessing step ensures label 0 is reserved for background if `void_background` is False,
              and boundaries around segments are properly traced as void (label 255), otherwise, both 
              the background and segment boundaries are labelled as void.
    
        Raises:
            OSError: If writing to the specified path fails due to permission or filesystem issues.
        """
        directory_path = os.path.dirname(self.annotation_path)
        os.makedirs(directory_path, exist_ok=True)
        if self.use_bounding_boxes:
            lines = [' '.join(row)+'\n' for row in self.bounding_boxes.astype(str)]
            with open(self.annotation_path, 'w') as file:
                file.writelines(lines)
        else:
            np.save(self.__path_to_labelled_segment_masks, self.labelled_segment_masks)
            overall_segment_mask_to_save = self.postprocess_overall_segment_mask_for_saving()
            imsave(self.annotation_path, overall_segment_mask_to_save)
        absolute_file_path = os.path.abspath(self.annotation_path)
        self.log(f'Annotations saved to "{absolute_file_path}"')
    
    def log(self, message:str):
        """
        Print a log message if verbosity is enabled.

        Args:
            message (str): Message to print.
        """
        if self.__verbose:
            print(' ' * len(self.__previous_message), end='\r')
            print(message, end='\r')
            self.__previous_message = message
        
    def __combine_labelled_segment_masks(self):
        """
        Merges all labelled segment masks into a single composite mask.
    
        Behavior:
        - Uses a custom `merge()` function to overlay masks:
            - For each pixel in `mask_a` that is labelled (i.e., not 255),
              its value overwrites the corresponding pixel in `mask_b`.
            - This gives priority to earlier masks in the sequence when overlapping occurs.
        - If no labelled masks are present, returns a blank mask filled with 255 (void label).
    
        Returns:
            np.ndarray: A `uint8` array representing the merged segment mask.
                        Annotated regions retain their original labels; unannotated regions are 255.
        """
        def merge(mask_a, mask_b):
            annotated_portion_in_mask_a = mask_a != 255
            annotated_indices_in_mask_a = np.where(annotated_portion_in_mask_a)
            mask_b[annotated_indices_in_mask_a] = mask_a[annotated_indices_in_mask_a]
            return mask_b
        
        if self.labelled_segment_masks.size:
            masks = self.labelled_segment_masks.copy()
            combined_masks = reduce(merge, masks).astype('uint8')
            return combined_masks
        return np.zeros(self.__original_array_shape, 'uint8') + 255
    
    def __resize_user_interface_update_routine(self):
        """Handle window resize events, rescaling images and updating annotation layers."""
        self.__reload_image()
        self.__retrace_annotations()
        self.__update_drawing_overlay()
        self.__update_pen_tracer_overlay()
        self.__combine_layers_and_update_image_display()
        self.__update_label_displays()
        self.__resize_pen()
        self.__resize_flag = False
        
    def __annotate_user_interface_update_routine(self):
        """Update the annotation overlay and label displays after changes."""
        self.__retrace_annotations()
        self.__combine_layers_and_update_image_display()
        self.__update_contents_of_label_displays()
    
    def __reload_image(self):
        """Reload the original image without affecting current annotations."""
        self.image_path = self.image_path
    
    def __retrace_annotations(self):
        """Clear overlay layer and redraw all annotations (bounding boxes or masks)."""
        self.annotation_overlay = None
        if self.__use_bounding_boxes:
            self.__trace_bounding_boxes()
        else:
            self.__trace_segments()
            
    def __trace_bounding_boxes(self):
        """
        Draws bounding boxes on the image and optionally labels them with the corresponding label names.
        
        The method iterates over all the bounding boxes and draws them on the annotation layer:
        - Each bounding box is drawn with a color corresponding to its label.
        - If the `corner_label_attached_to_bounding_box` flag is set, the label for the bounding box is displayed at its corner.
        
        The bounding box dimensions are scaled according to the current scale factor, and the label text is displayed with a white font on a background matching the label's color.
        """
        painter, pen, brush = QPainter(self.annotation_overlay), QPen(self.__annotation_pen), QBrush(Qt.Dense7Pattern)
        pen.setWidthF(self.__annotation_pen.widthF() / self.__minimum_pen_width)
        if self.corner_label_attached_to_bounding_box:
            font_size = int(self.__label_font_size * self.__scale_factor)
            font = QFont('Arial', font_size)
            painter.setFont(font)
            
        for bounding_box in self.bounding_boxes:
            label_index, dimensions = bounding_box[0], bounding_box[1:]
            dimensions = np.int32(dimensions * self.__scale_factor)
            color = self.label_colors[label_index]
            pen.setColor(color); brush.setColor(color)
            painter.setPen(pen); painter.setBrush(brush)
            painter.drawRect(QRect(*dimensions))
            if self.corner_label_attached_to_bounding_box:
                x_offset, y_offset = dimensions[:2]
                text = f'Label: {self.labels[label_index]}'
                font_metrics = painter.fontMetrics()
                text_width, text_height = round(font_metrics.horizontalAdvance(text) * 1.2), font_metrics.height()
                text_box = QRect(x_offset, y_offset, text_width, text_height)
                painter.fillRect(text_box, self.label_colors[label_index])
                pen.setColor(Qt.white); painter.setPen(pen)
                x_text, y_text = [x_offset, y_offset] + np.int32([0.08 * text_width, 0.77 * text_height])
                painter.drawText(x_text, y_text, text)
    
    def __trace_segments(self):
        """
        Traces and generates the annotation layer for the segmented image, applying colors based on the labels.
        
        This method performs the following steps:
        - Prepares an RGBA lookup table based on the label colors and the opacity setting.
        - Resizes the overall segment mask to match the current image dimensions.
        - Uses the lookup table to map segment mask values to RGBA colors.
        - Converts the resulting RGBA array into a QPixmap and stores it in the `annotation_overlay` attribute.
        
        The resulting `annotation_overlay` is used to display the segmented image with colors corresponding to different labels.
        """
        def prepare_rgba_lookup_table():
            alpha = int(self.__opacity * 255)
            get_rgb_channels = lambda color: [color.red(), color.green(), color.blue()]
            lookup_table = np.zeros([256, 4], 'uint8')
            lookup_table_modification = np.uint8([get_rgb_channels(color) + [alpha] for color in self.label_colors])
            lookup_table[:self.n_labels] += lookup_table_modification
            return lookup_table
        
        current_array_shape = self.height(), self.width()
        scaled_overall_segment_mask = resize(self.overall_segment_mask, current_array_shape, 0)
        lookup_table = prepare_rgba_lookup_table()
        rgba_array = lookup_table[scaled_overall_segment_mask]
        self.annotation_overlay = rgba_array_to_pixmap(rgba_array)
    
    def __combine_layers_and_update_image_display(self):
        """
        Combines the base image, drawing layer, and optional pen tracer overlay into a single QPixmap,
        then updates the image display widget.
        
        This method performs the following steps:
        - Creates a compound QPixmap from the original image.
        - Uses QPainter to draw the current drawing layer onto the compound image.
        - Draws a drawing overlay after it is initialized.
        - Draws an additional pen tracer overlay after it is initialized.
        - Updates the GUI's image display with the resulting composed image.
        """
        compound_layer = QPixmap(self.image)
        painter = QPainter(compound_layer)
        painter.drawPixmap(0, 0, self.annotation_overlay)
        if hasattr(self, f'_{self.__class__.__name__}__drawing_overlay'):
            painter.drawPixmap(0, 0, self.drawing_overlay)
        if hasattr(self, f'_{self.__class__.__name__}__pen_tracer_overlay'):
            painter.drawPixmap(0, 0, self.pen_tracer_overlay)
        painter.end()
        self.__image_display.setPixmap(compound_layer)
        
    @property
    def drawing_overlay(self):
        """Drawing overlay to draw over."""
        return self.__drawing_overlay
        
    @property
    def pen_tracer_overlay(self):
        """Tracer overlay to draw the circle over the pen tip."""
        return self.__pen_tracer_overlay
        
    def __get_mask_for_annotations_hovered_over(self):
        """
        Retrieves a mask indicating which annotations are currently hovered over by the cursor.
        
        The method generates a mask that marks annotations under the cursor’s position:
        
        - If bounding boxes are used, it checks if the cursor is within the bounds of each bounding box.
        - If segment masks are used, it checks if the cursor is within any segment by verifying the pixel value at the cursor’s position.
        
        Returns:
            np.ndarray: A boolean mask where each element corresponds to an annotation, indicating whether it is hovered over by the cursor.
        
        Notes:
            - The method returns a boolean array where `True` indicates that the annotation is hovered over, and `False` otherwise.
            - If no annotations are present or the cursor is not hovering over any annotation, the returned mask will be all `False`.
        """
        annotation_hover_mask = np.zeros(self.bounding_boxes.shape[0] if self.use_bounding_boxes else self.labelled_segment_masks.shape[0], bool)
        annotations_exist = bool(annotation_hover_mask.size)
        if annotations_exist:
            y_cursor, x_cursor = self.__yx_cursor_within_original_image
            if self.use_bounding_boxes:
                for index, (_, x_offset, y_offset, width, height) in enumerate(self.bounding_boxes):
                    annotation_hover_mask[index] = \
                        y_offset <= y_cursor <= y_offset + height and \
                        x_offset <= x_cursor <= x_offset + width
            else:
                annotation_hover_mask = self.labelled_segment_masks[:, y_cursor, x_cursor] != 255
        return annotation_hover_mask
    
    def __get_mask_for_smallest_annotation_hovered_over(self):
        """
        Retrieves the mask for the smallest annotation currently hovered over by the cursor.
        
        This method checks which annotations are under the cursor and determines the smallest one based on its area:
        
        - If bounding boxes are used, the area is calculated as the product of the bounding box dimensions.
        - If segment masks are used, the area is computed using a helper function from `.utils`.
        
        The method returns a mask corresponding to the smallest hovered annotation.
        
        Returns:
            np.ndarray: A boolean mask indicating the smallest annotation hovered over, or an empty mask if no annotation is hovered over.
        
        Notes:
            - The method compares annotations based on their area and returns a mask for the smallest one.
            - If no valid annotation is found under the cursor, it returns an empty mask.
        """
        annotation_hover_mask = self.__get_mask_for_annotations_hovered_over()
        if annotation_hover_mask.sum() < 2:
            return annotation_hover_mask
        annotations = self.bounding_boxes if self.use_bounding_boxes else self.labelled_segment_masks
        annotations_to_inspect = annotations[annotation_hover_mask]
        if self.use_bounding_boxes:
            areas = np.prod(annotations_to_inspect[:,-2:], axis=1)
        else:
            areas = compute_segment_areas(annotations_to_inspect)
        index_of_interest = np.argmin(areas)
        smallest_annotation_hover_mask = (annotations == annotations_to_inspect[index_of_interest]).all(axis=1 if self.use_bounding_boxes else (1,2))
        return smallest_annotation_hover_mask
    
    def __drop_smallest_annotation_hovered_over(self):
        """
        Drops the smallest annotation currently hovered over by the cursor.
    
        This method generates a mask for the smallest annotation under the cursor and removes it from the collection of annotations:
        
        - If bounding boxes are used, it removes the corresponding bounding box from the list.
        - If segment masks are used, it removes the corresponding segment mask from the array.
    
        Returns:
            bool: True if an annotation was successfully removed, False if no annotation was hovered over or removed.
    
        Notes:
            - The method checks for the smallest annotation under the cursor and removes it based on the current configuration (bounding boxes or segment masks).
            - The method returns `True` if an annotation was removed, and `False` if no annotation was found or removed.
        """
        smallest_annotation_hover_mask = self.__get_mask_for_smallest_annotation_hovered_over()
        if smallest_annotation_hover_mask.any():
            if self.use_bounding_boxes:
                self.__bounding_boxes = self.bounding_boxes[~smallest_annotation_hover_mask]
            else:
                self.labelled_segment_masks = self.labelled_segment_masks[~smallest_annotation_hover_mask]
            return True
        return False
    
    def __get_label_index_hovered_over(self):
        """
        Retrieves the label index of the smallest annotation currently hovered over by the cursor.
        
        This method checks for the smallest annotation under the cursor by generating a mask and then determines
        the label index based on whether bounding boxes or segment masks are used:
        
        - If bounding boxes are used, it returns the index of the first label in the smallest hovered bounding box.
        - If segment masks are used, it returns the label index of the smallest hovered segment mask that is not empty (i.e., excluding the background).
        
        Returns:
            int: The index of the label hovered over, or -1 if no annotation is hovered over.
        
        Notes:
            - If no annotation is detected under the cursor, the method returns -1.
            - The method handles both bounding boxes and segment masks based on the current configuration.
        """
        smallest_annotation_hover_mask = self.__get_mask_for_smallest_annotation_hovered_over()
        if smallest_annotation_hover_mask.any():
            if self.use_bounding_boxes:
                smallest_annotation_hovered_over = self.bounding_boxes[smallest_annotation_hover_mask].squeeze()
                return smallest_annotation_hovered_over[0]
            else:
                smallest_annotation_hovered_over = self.labelled_segment_masks[smallest_annotation_hover_mask].squeeze()
                annotated_portion = smallest_annotation_hovered_over != 255
                return np.unique(smallest_annotation_hovered_over[annotated_portion])[0]
        return -1
    
    def __clear_annotations(self):
        """
        Clears all annotations from the drawing, either by resetting bounding boxes or labelled segment masks.
        
        If bounding boxes are used:
            - Resets the bounding boxes array to an empty array with shape (0, 5), which represents no bounding boxes.
        
        If bounding boxes are not used:
            - Resets the labelled segment masks array to an empty array with the same shape as the original array, representing no segment masks.
        
        This method effectively removes all annotations from the image or drawing.
        """
        if self.use_bounding_boxes:
            self.__bounding_boxes = np.empty([0, 5], 'int32')
        else:
            self.labelled_segment_masks = np.empty([0] + self.__original_array_shape, 'int32')
        
    def __draw(self, current_position:QPoint, mode:str):
        """
        Draws either a point or a line on the drawing based on the specified mode.
        
        If the mode is 'point', draws a point at the current position.
        If the mode is 'line', draws a line from the last recorded position to the current position.
        
        The method raises a ValueError if an invalid mode is provided.
        
        Args:
            current_position (QPoint): The current position where the drawing action should take place.
            mode (str): The drawing mode, either 'point' or 'line'. 'point' draws a single point, 'line' draws a line from the last position to the current one.
        
        Raises:
            ValueError: If the mode is not 'point' or 'line'.
        """
        if mode not in {'point', 'line'}:
            raise ValueError("The argument `mode` can either take the value of 'point' or 'line'.")
        
        painter = QPainter(self.drawing_overlay)
        if self.erasing:
            self.__annotation_pen.setColor(Qt.transparent)
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
        else:
            self.__annotation_pen.setColor(self.label_to_annotate_color)
        painter.setPen(self.__annotation_pen)
        
        if mode == 'point' or self.__last_pen_position is None:
            painter.drawPoint(current_position)
        else:
            painter.drawLine(self.__last_pen_position, current_position)
        painter.end()
        
    def __configure_label_display(self, label_display:QLabel, label_index:int, hovering:bool):
        """
        Configures the display of a label in a QLabel widget based on the label index and hovering state.
    
        If the label index is invalid (negative) or erasing is active and not hovering:
            - Sets the label text to 'N/A' and the background to transparent.
    
        Otherwise, it sets the label text to the corresponding label from the list and the background color to the label's color.
    
        The label text is padded to align properly with the maximum text length of all labels.
    
        Args:
            label_display (QLabel): The QLabel widget where the label text and style will be applied.
            label_index (int): The index of the label to display, used to retrieve the label text and color.
            hovering (bool): Indicates whether the mouse is hovering over a label for interaction.
        """
        if label_index < 0 or (self.erasing and not hovering):
            text = 'N/A'
            background_color = 'transparent'
        else:
            text = self.labels[label_index]
            background_color = self.label_colors[label_index].name()
        maximum_text_length = reduce(lambda a, b: max(len(str(a)), len(str(b))), self.labels + ['N/A'])
        label_display.setText(f'Label: {text:<{maximum_text_length}}')
        label_display.setStyleSheet(f'background: {background_color}; border: 1px solid black; padding: 2px;')
        
    def __update_positions_of_label_displays(self):
        """
        Updates the on-screen label display elements, including their positions.
        
        This method orchestrates:
        - Positioning of the floating label displays (annotation target label and hovered label),
          depending on cursor position or fixed layout.
        
        Called during cursor updates, label changes, and redraw events to ensure accurate and
        visually consistent label feedback for the user.
        """
        if self.__last_pen_position and self.is_floating_label:
            x_offset = self.__last_pen_position.x() + self.__floating_label_display_offsets[0]
            y_offset = self.__last_pen_position.y() + self.__floating_label_display_offsets[1]
        else:
            x_offset = self.width() - max(self.__label_to_annotate_display.width(), self.__label_annotated_display.width())
            y_offset = 0
        self.__label_to_annotate_display.move(x_offset, y_offset)
        self.__label_annotated_display.move(x_offset, y_offset + self.__label_to_annotate_display.height())
        
    def __update_contents_of_label_displays(self):
        """
        Updates the on-screen label display element contents.
        
        This method orchestrates:
        - Updating the displayed label names and their formatting based on the current annotation
          label index and the label currently under the cursor.
        - Ensuring that both label displays share a consistent width after initial configuration.
        
        Called during cursor updates, label changes, and redraw events to ensure accurate and
        visually consistent label feedback for the user.
        """
        self.__label_index_hovered_over = self.__get_label_index_hovered_over()
        self.__configure_label_display(self.__label_to_annotate_display, self.label_index_to_annotate, False)
        self.__configure_label_display(self.__label_annotated_display, self.__label_index_hovered_over, True)
        if not self.__label_displays_configuration_complete:
            common_width = max(self.__label_to_annotate_display.width(), self.__label_annotated_display.width()) - 25
            self.__label_to_annotate_display.setFixedWidth(common_width - 1)
            self.__label_annotated_display.setFixedWidth(common_width - 1)
            self.__label_displays_configuration_complete = True
            
    def __update_label_displays(self):
        """
        Updates the on-screen label display elements, including both their content and position.
        
        This method orchestrates:
        - Positioning of the floating label displays (annotation target label and hovered label),
          depending on cursor position or fixed layout.
        - Updating the displayed label names and their formatting based on the current annotation
          label index and the label currently under the cursor.
        - Ensuring that both label displays share a consistent width after initial configuration.
        
        Called during cursor updates, label changes, and redraw events to ensure accurate and
        visually consistent label feedback for the user.
        """
        self.__update_positions_of_label_displays()
        self.__update_contents_of_label_displays()
            
    def __reconfigure_label_annotated_display(self):
        """
        Update only the hovered label display.
        
        - Refreshes the label information under the current mouse position.
        - Does not reposition any floating labels or change layout.
        """
        self.__label_index_hovered_over = self.__get_label_index_hovered_over()
        self.__configure_label_display(self.__label_annotated_display, self.__label_index_hovered_over, True)
    
    def __resize_pen(self):
        """
        Dynamically adjust the drawing pen width based on window size.
        
        - Scales the annotation pen width proportionally relative to the initial minimum widget width and the pen width multiplier.
        - Ensures that the pen stays visually consistent across different window resize events.
        """
        widget_minimum_width = self.minimumWidth()
        if widget_minimum_width:
            ratio = self.width() / widget_minimum_width
            self.__annotation_pen.setWidthF(ratio * self.__minimum_pen_width * self.pen_width_multiplier)
    
    def resizeEvent(self, event):
        """
        Handle window resize events.
        
        - Sets the initial minimum widget size based on the first resize.
        - Rescales the image display to match the new widget size.
        - Starts a timer to schedule an optimized resize update routine.
        
        Args:
            event (QResizeEvent): The resize event object containing new size info.
        """
        self.__resize_flag = True
        if not self.__minimum_widget_size_set:
            self.setMinimumSize(self.size())
            self.__minimum_widget_size_set = True
        self.__image_display.resize(self.size())
        self.__resize_scheduler.start(self.RESIZE_DELAY)
        event.accept()
    
    def wheelEvent(self, event):
        """
        Handles mouse wheel events to modify either label selection or pen width, 
        depending on the current mode.
        
        Behavior:
        - If erasing mode is active, it is disabled.
        - If label slider mode is enabled:
            - Adjusts the label index accumulator based on the wheel direction and sensitivity.
        - Otherwise:
            - Adjusts the pen width accumulator based on the wheel direction and sensitivity.
        
        After handling the wheel input, this method updates the pen tracer overlay, 
        refreshes the image display, and updates the label displays accordingly..
        
        Parameters:
            event (QWheelEvent): The wheel event triggered by user input.
        """
        if self.erasing:
            self.__erasing = False
        delta = event.angleDelta().y()
        if self.__label_slider_enabled:
            delta = self.__label_slider_sensitivity * np.sign(delta)
            self.label_index_accumulator += delta
        else:
            delta = self.__pen_width_slider_sensitivity * np.sign(delta)
            self.pen_width_multiplier_accumulator += delta
        self.__update_pen_tracer_overlay()
        self.__combine_layers_and_update_image_display()
        self.__update_contents_of_label_displays()
    
    def mousePressEvent(self, event):
        """
        Handles mouse press events to manage annotation drawing, erasing, and UI mode toggling.
        
        Behavior depends on the mouse button pressed:
        - Left Button:
            - If in erasing mode, attempts to remove the smallest annotation under the cursor.
              If an annotation is removed:
                - Retraces annotations.
                - Updates the annotated label display.
                - Optionally triggers autosave if enabled.
            - Otherwise, draws a point annotation at the cursor position.
            - In both cases, updates the combined image display.
        
        - Right Button:
            - Toggles the erasing mode.
            - Updates the pen tracer overlay and refreshes the image and the contents of label displays.
        
        - Middle Button:
            - Toggles the label slider mode (used for navigating label indices).
            - Updates the pen tracer overlay and refreshes the image display.
        
        Parameters:
            event (QMouseEvent): The mouse press event containing button and position data.
        """
        self.__update_yx_cursor_within_original_image(event.pos())
        if event.button() == Qt.LeftButton:
            if self.erasing:
                updated = self.__drop_smallest_annotation_hovered_over()
                self.__retrace_annotations()
                if updated:
                    self.__reconfigure_label_annotated_display()
                    if self.__autosave:
                        self.save()
            self.__draw(event.pos(), 'point')
            self.__combine_layers_and_update_image_display()
        elif event.button() == Qt.RightButton:
            self.__erasing ^= True
            self.__update_pen_tracer_overlay()
            self.__combine_layers_and_update_image_display()
            self.__update_contents_of_label_displays()
        elif event.button() == Qt.MiddleButton:
            self.__label_slider_enabled ^= True
            self.__update_pen_tracer_overlay()
            self.__combine_layers_and_update_image_display()
            
    def __update_drawing_overlay(self):
        if hasattr(self, f'_{self.__class__.__name__}__drawing_overlay'):
            self.__drawing_overlay = self.drawing_overlay.scaled(self.image.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
        else:
            self.initialize_overlay('drawing')
            
    def __update_pen_tracer_overlay(self):
        """
        Updates the pen tracer overlay used to visually indicate the pen position and size on the image.
    
        Functionality:
        - If no previous pen position is recorded, the method exits early.
        - Initializes a transparent QPixmap the same size as the image to serve as the overlay.
        - If in erasing mode, the overlay is left blank and the method returns.
        - Otherwise, draws a circle (tracer) at the last pen position to indicate where and how large 
          the next annotation will be.
            - If either of label slider or eraser modes is active, it uses a black pen for the tracer.
            - Otherwise, it uses the current label color.
        - The tracer's size reflects the current pen width adjusted by scaling factors.
        
        This method is called whenever visual feedback about the drawing tool is needed,
        such as when the pen size or position changes.
        """
        if self.__last_pen_position is None:
            return
        self.initialize_overlay('pen_tracer')
        painter = QPainter(self.pen_tracer_overlay)
        if self.__label_slider_enabled or self.__erasing:
            pen = QPen(Qt.black, 1)
        else:
            pen = QPen(self.label_colors[self.label_index_to_annotate], 1)
        painter.setPen(pen)
        pen_width = self.__annotation_pen.widthF()
        width = pen_width - 6 * self.pen_width_multiplier * self.__scale_factor
        painter.drawEllipse(self.__last_pen_position, width, width)
        painter.end()
        
    def initialize_overlay(self, overlay_name:str):
        if overlay_name not in {'drawing', 'annotation', 'pen_tracer'}:
            raise ValueError("`overlay_name` should either be 'drawing' or 'annotation'")
        attribute_name = f'_{self.__class__.__name__}__{overlay_name}_overlay'
        self.__dict__[attribute_name] = QPixmap(self.image.size())
        self.__dict__[attribute_name].fill(Qt.transparent)
        
    def mouseMoveEvent(self, event):
        """
        Handles mouse movement events and updates the image display based on cursor position and button states.
    
        If the left mouse button is held down:
            - If erasing is enabled, it attempts to drop the smallest annotation hovered over and retraces annotations.
            - Otherwise, it draws a line based on the mouse movement.
            - Combines layers and updates the image display.
            
        Additionally, updates the label displays and tracks the last position of the pen.
        
        Args:
            event (QMouseEvent): The event object containing details about the mouse movement.
        
        Note: It is very necessary to apply this routine while the application is not resizing. Otherwise, an IndexError 
        exception could later occur due to the cursor (`self.__yx_cursor_within_original_image`) being mapped to outside 
        the bounds of the original image.
        """
        if self.__resize_flag:
            return
        current_pen_position = event.pos()
        self.__update_yx_cursor_within_original_image(current_pen_position)
        if event.buttons() & Qt.LeftButton:
            self.__draw(current_pen_position, 'line')
            if self.erasing:
                updated = self.__drop_smallest_annotation_hovered_over()
                if updated:
                    self.__retrace_annotations()
                    if self.__autosave:
                        self.save()
        else:
            self.__update_contents_of_label_displays()
        self.last_pen_position = current_pen_position
        self.__update_pen_tracer_overlay()
        self.__combine_layers_and_update_image_display()
        self.__update_positions_of_label_displays()
        
    def __update_yx_cursor_within_original_image(self, position:QPoint):
        if position is None:
            self.__yx_cursor_within_original_image = (0, 0)
        else:
            self.__yx_cursor_within_original_image = (np.array([position.y(), position.x()]) / self.__scale_factor).astype(int)
        
    def mouseDoubleClickEvent(self, event):        
        """
        Handles mouse double-click events, performing different actions based on the button pressed.
        
        If the right mouse button is double-clicked:
            - Prompts the user with a warning message asking for confirmation to clear annotations.
            - If confirmed, clears all annotations and disables erasing mode.
        
        If the left mouse button is double-clicked and erasing is not active:
            - Performs a flood-fill algorithm to locate all connected pixels starting from the double-clicked position.
            - If bounding boxes are used, checks the size of the bounding box and adds it to the list if it meets the size thresholds.
            - If bounding boxes are not used, creates and labels a segment mask, and adds it to the list of labelled segment masks.
        
        After updating annotations or segment masks, triggers the update routine and optionally saves the state if autosave is enabled.
        
        Args:
            event (QMouseEvent): The event object containing details about the mouse double-click.
        """
        updated = False
        if event.button() == Qt.RightButton:
            response = QMessageBox.warning(self, 'Clear Drawing?', 'You are about to clear your annotations for this image!', QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if response == QMessageBox.Ok:
                self.__clear_annotations()
                self.__erasing = False
                updated = True
        elif event.button() == Qt.LeftButton and not self.erasing:
            yx_root = event.y(), event.x()
            rgba_array = pixmap_to_rgba_array(self.drawing_overlay)
            rgb_array = rgba_array[:,:,:-1]
            traversed_pixels_mask = locate_all_pixels_via_floodfill(rgb_array, yx_root)
            if self.use_bounding_boxes:
                bounding_box = mask_to_bounding_box(traversed_pixels_mask)
                x_offset, y_offset, width, height = (bounding_box / self.__scale_factor).astype('int32').tolist()
                minimum_side_length, maximum_side_length = min(width, height), max(width, height)
                lower_side_length_bound, upper_side_length_bound = self.__bounding_box_side_length_thresholds
                if lower_side_length_bound <= minimum_side_length and maximum_side_length <= upper_side_length_bound:
                    self.__bounding_boxes = np.concatenate([
                        self.bounding_boxes,
                        np.array([self.label_index_to_annotate, x_offset, y_offset, width, height])[np.newaxis, ...]
                    ])
                boxes_to_remove_mask = detect_overlapping_boxes_to_clean(self.bounding_boxes, self.__overlap_vs_smallest_area_threshold, self.__overlap_vs_union_area_threshold)
                self.__bounding_boxes = self.bounding_boxes[~boxes_to_remove_mask]
            else:
                segment_mask = resize(traversed_pixels_mask, self.__original_array_shape, 0)
                segment_mask = binary_fill_holes(segment_mask).astype(int)
                labelled_segment_mask = apply_lut_replacement(segment_mask, self.label_index_to_annotate)
                self.labelled_segment_masks = np.concatenate([labelled_segment_mask[np.newaxis, ...], self.labelled_segment_masks])
            updated = True
        if updated:
            self.drawing_overlay.fill(Qt.transparent)
            self.__annotate_user_interface_update_routine()
            if self.__autosave:
                self.save()
                
    def trace_bounds_around_segments(self):
        """
        Detects 1-pixel-wide boundaries around segments using Canny edge detection.
    
        Behavior:
        - Applies the Canny edge detector with low and high thresholds set to 0 and 1, respectively.
        - Operates on `self.overall_segment_mask` (a 2D `uint8` array).
        - Identifies the boundary pixels between segmented regions.
        - Returns the indices of the detected boundary pixels.
    
        Returns:
            tuple of np.ndarray: A tuple (row_indices, col_indices) representing the coordinates
                                 of the boundary pixels.
        """
        overall_mask = self.overall_segment_mask.copy()
        bound_indices = np.where(canny(overall_mask, low_threshold=0, high_threshold=1))
        return bound_indices
                
    def postprocess_overall_segment_mask_for_saving(self):
        """
        Prepares the overall segmentation mask for saving by applying label shifting and boundary tracing.
        
        Behavior:
        - If `void_background` is False:
            - Increments all label values by 1, turning background (255) into 0 and shifting segment labels.
        - If `void_background` is True:
            - Leaves label values unchanged (255 remains as void).
        - Detects boundaries between segments and sets those boundary pixels to 255 (void label).
        
        Returns:
            np.ndarray: The final segmentation mask array with boundaries marked and label values adjusted,
                        suitable for saving as a PNG.
        """
        overall_segment_mask_to_save = self.overall_segment_mask + (not self.void_background)
        bound_indices = self.trace_bounds_around_segments()
        overall_segment_mask_to_save[bound_indices] = 255
        return overall_segment_mask_to_save