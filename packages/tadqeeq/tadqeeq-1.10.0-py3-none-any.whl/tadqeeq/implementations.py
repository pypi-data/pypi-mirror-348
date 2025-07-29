""" 
Tadqeeq - Image Annotator Tool
An interactive image annotation tool for efficient labeling.
Developed by Mohamed Behery @ RTR Software Development (2025-04-27).
Licensed under the MIT License.
"""

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QTimer
import os
from collections.abc import Iterable
from .widgets import ImageAnnotator
from .utils import get_pixmap_compatible_image_filepaths

class ImageAnnotatorWindow(QMainWindow):
    """
    Main application window for the Tadqeeq image annotation tool.
    
    This window embeds an ImageAnnotator widget and provides navigation, resizing, 
    and directory management functionality for image annotation tasks.
    
    Args:
        images_directory_path (str): Directory containing images to annotate.
        annotations_directory_path (str): Directory to read/write annotations.
        use_bounding_boxes (bool): If True, uses bounding boxes (.txt files). If False, uses segmentation masks (.png/.npy).
        image_navigation_keys (Iterable): Iterable of two Qt.Key values used for navigating between images (e.g., [Qt.Key_A, Qt.Key_D]).
        **image_annotator_kwargs: Additional keyword arguments passed directly to the ImageAnnotator.
    
    Features:
        - Automatically detects compatible images in the specified directory.
        - Maintains synchronized navigation and annotation file lists.
        - Supports switching between bounding box and segmentation modes.
        - Handles delayed UI resizing for smoother layout adjustments.
        - Embeds the ImageAnnotator as the central widget and updates it when navigating between files.
        - Prevents window maximization for consistent sizing behavior.
    
    Example:
        app = QApplication([])
        window = MainWindow("images/", "annotations/", use_bounding_boxes=False)
        window.show()
        app.exec_()
    """
    def __init__(self,
                 images_directory_path,
                 annotations_directory_path,
                 use_bounding_boxes=False,
                 image_navigation_keys=(Qt.Key_A, Qt.Key_D),
                 **image_annotator_kwargs):
        """
        Initializes the main window of the Tadqeeq image annotation tool.
        
        This constructor sets up the image annotation environment, including:
        - Loading image and annotation file paths.
        - Embedding the `ImageAnnotator` widget for interactive labeling.
        - Setting up navigation, window behavior, and UI resizing.
        
        Args:
            images_directory_path (str): Path to the directory containing images to be annotated.
            annotations_directory_path (str): Path to the directory for saving/loading annotation files.
            use_bounding_boxes (bool, optional): Whether to use bounding box annotations (.txt files). 
                                                 If False, uses segmentation masks (.png/.npy). Default is False.
            image_navigation_keys (list of Qt.Key, optional): Two keys used to navigate between images 
                                                              (e.g., [Qt.Key_A, Qt.Key_D]). Default is A and D.
            **image_annotator_kwargs: Additional keyword arguments passed to the `ImageAnnotator` widget.
        
        Raises:
            ValueError: If `images_directory_path` is not a valid directory, or if 
                        `image_navigation_keys` does not contain exactly two elements.
        """
        def initialize_image_filepaths():
            self.images_directory_path = images_directory_path
            
        def initialize_annotation_filepaths():
            self.__annotations_directory_path = annotations_directory_path
            self.use_bounding_boxes = use_bounding_boxes
            
        def initialize_image_annotator_widget():
            self.__image_annotator_kwargs = image_annotator_kwargs
            self.image_index = 0
            self.__resize_user_interface_update_routine()
        
        def disable_maximize_button():
            self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
        def configure_resize_scheduler():
            self.__resize_scheduler = QTimer(self)
            self.__resize_scheduler.setSingleShot(True)
            self.__resize_scheduler.timeout.connect(self.__resize_user_interface_update_routine)
            
        def configure_image_navigation_keys():
            if len(image_navigation_keys) != 2:
                raise ValueError('`image_navigation_keys` must exactly be two keys.')
            self.__image_navigation_keys = image_navigation_keys
        
        super().__init__()
        
        initialize_image_filepaths()
        initialize_annotation_filepaths()
        initialize_image_annotator_widget()
        
        disable_maximize_button()
        configure_resize_scheduler()
        configure_image_navigation_keys()
        
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowTitle('Tadqeeq - a Minimalist Image Annotator')
        self.setCentralWidget(self.__image_annotator)
    
    def keyPressEvent(self, event):
        """
        Handles keyboard input for image navigation.
    
        Navigates backward or forward in the image list based on the keys set 
        in `image_navigation_keys`.
    
        Args:
            event (QKeyEvent): The key press event.
    
        Behavior:
            - If the first key is pressed and not at the first image, decrements the image index.
            - If the second key is pressed and not at the last image, increments the image index.
        """
        if event.key() == self.image_navigation_keys[0] and self.image_index > 0:
            self.image_index -= 1
        elif event.key() == self.image_navigation_keys[1] and self.image_index < len(self.image_filepaths) - 1:
            self.image_index += 1
        
    @property
    def images_directory_path(self):
        """
        str: The path to the directory containing input images.

        This property returns the current directory path used to load images
        for annotation.
        """
        return self.__images_directory_path
    
    @images_directory_path.setter
    def images_directory_path(self, value:str):
        """
        Sets the directory path containing images and updates the image file list.
    
        This setter:
        - Validates that the provided path is a directory.
        - Stores the path internally.
        - Populates the list of compatible image files using `Helper.get_pixmap_compatible_image_filepaths`.
    
        Args:
            value (str): A path to a directory containing image files.
    
        Raises:
            ValueError: If the provided path is not a valid directory.
        """
        if not os.path.isdir(value):
            raise ValueError('`images_directory_path` should refer to a directory.')
        self.__images_directory_path = value
        self.__image_filepaths = get_pixmap_compatible_image_filepaths(value)
        
    @property
    def annotations_directory_path(self):
        """
        str: The path to the directory where annotation files are stored.
    
        This is a read-only property that returns the path configured for saving or loading 
        annotation files (either as .txt for bounding boxes or .png/.npy for masks).
        """
        return self.__annotations_directory_path
    
    @property
    def use_bounding_boxes(self):
        """
        bool: Whether the annotation format is bounding boxes.

        If True, annotation files are expected to be in `.txt` format, containing bounding box data.
        If False, annotation files are assumed to be `.png` images (e.g., segmentation masks).
        """
        return self.__use_bounding_boxes
    
    @use_bounding_boxes.setter
    def use_bounding_boxes(self, value:bool):
        """
        Sets the annotation mode and updates annotation file paths accordingly.
        
        Args:
            value (bool): True to use bounding box annotations (`.txt`), 
                          False to use segmentation masks (`.png`).
        
        Side Effects:
            - Updates the list of annotation file paths using the selected file extension.
        """
        self.__use_bounding_boxes = value
        self.__annotation_filepaths = list(map(self.image_filepath_to_annotation_filepath, self.image_filepaths))
    
    def image_filepath_to_annotation_filepath(self, image_filepath):
        """
        Generates the corresponding annotation file path for a given image file.
        
        Depending on the `use_bounding_boxes` setting, this will generate:
        - a `.txt` filename (for bounding boxes), or
        - a `.png` filename (for masks).
        
        Args:
            image_filepath (str): The full path to the image file.
        
        Returns:
            str: The full path to the corresponding annotation file.
        """
        filename = os.path.basename(image_filepath)
        file_extension = '.txt' if self.use_bounding_boxes else '.png'
        annotation_filename = os.path.splitext(filename)[0] + file_extension
        annotation_filepath = os.path.join(self.annotations_directory_path, annotation_filename)
        return annotation_filepath
    
    @property
    def image_filepaths(self):
        """
        List of str objects: Absolute paths to all valid image files in the image directory.
        
        This list is populated when `images_directory_path` is set and includes only files 
        with extensions compatible with QPixmap (e.g., .png, .jpg, .bmp, etc.).
        """
        return self.__image_filepaths
    
    @property
    def annotation_filepaths(self):
        """
        List of str objects: Absolute paths to the corresponding annotation files for each image.
        
        This list is automatically updated based on the current `image_filepaths` and the 
        annotation format selected by `use_bounding_boxes`.
        """
        return self.__annotation_filepaths
    
    @property
    def image_navigation_keys(self):
        """
        List of QKey objects: Keyboard keys used to navigate between images.
        
        By default, this is set to [Qt.Key_A, Qt.Key_D], which maps to left and right navigation.
        """
        return self.__image_navigation_keys
    
    @image_navigation_keys.setter
    def image_navigation_keys(self, value:Iterable):
        """
        Sets the keys used to navigate through the image filepath list.
    
        Args:
            value (Iterable): An iterable containing exactly two `Qt.Key` values 
                              for backward and forward navigation, respectively.
    
        Raises:
            ValueError: If `value` does not contain exactly two items.
        """
        if len(value) != 2:
            raise ValueError('`image_navigation_keys` should be an `Iterable` of two items.')
        self.__image_navigation_keys = list(value)
    
    @property
    def image_index(self):
        """
        int: The index of the currently selected image in the list of filepaths.
        
        Changing this index will also update the `current_image_filepath`, 
        `current_annotation_filepath`, and refresh the embedded `ImageAnnotator`.
        """
        return self.__image_index
    
    @image_index.setter
    def image_index(self, value:int):
        """
        Sets the current image index and updates relevant filepaths and annotator state.
    
        Args:
            value (int): Index of the image to load.
    
        Side Effects:
            - Updates current image and annotation file paths.
            - Triggers update of the image annotator widget.
        """
        self.__image_index = value
        self.__current_image_filepath = self.image_filepaths[value]
        self.__current_annotation_filepath = self.annotation_filepaths[value]
        self.__update_image_annotator()
            
    def __update_image_annotator(self):
        """
        Updates the internal `ImageAnnotator` widget with the current image and annotation paths.
        
        If the annotator widget has already been created, it updates its properties in-place.
        Otherwise, it creates a new instance of the annotator with the appropriate paths and arguments.
        """
        if hasattr(self, f'_{self.__class__.__name__}__image_annotator'):
            self.__image_annotator.image_path = self.current_image_filepath
            self.__image_annotator.annotation_path = self.current_annotation_filepath
        else:
            self.__image_annotator = ImageAnnotator(
                self.current_image_filepath, 
                self.current_annotation_filepath, 
                **self.__image_annotator_kwargs
            )
    
    @property
    def current_image_filepath(self):
        """
        str: The full path to the currently selected image file.
        """
        return self.__current_image_filepath
    
    @property
    def current_annotation_filepath(self):
        """
        str: The full path to the annotation file corresponding to the current image.
        """
        return self.__current_annotation_filepath
    
    def resizeEvent(self, event):
        """
        Handles window resize events by scheduling a delayed UI update.
        
        This ensures that the interface adjusts itself smoothly after the resize, 
        rather than responding to every intermediate size change.
        
        Args:
            event (QResizeEvent): The resize event object.
        """
        self.__resize_scheduler.start(
            self.__image_annotator.RESIZE_DELAY
        )
        event.accept()
        
    def __resize_user_interface_update_routine(self):
        """
        Resizes the main window to match the size of the `ImageAnnotator` widget.
        
        This is triggered after a delay to avoid performance issues during continuous resizing.
        """
        self.resize(self.__image_annotator.size())
    
    
    
    