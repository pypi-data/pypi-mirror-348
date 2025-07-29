""" 
Tadqeeq - Image Annotator Tool
An interactive image annotation tool for efficient labeling.
Developed by Mohamed Behery @ RTR Software Development (2025-04-27).
Licensed under the MIT License.
"""

from PyQt5.QtWidgets import QApplication
import sys
import os
from .implementations import ImageAnnotatorWindow

def main():
    
    def print_help_message():
        print("Usage: tadqeeq [--void_background|--verbose|--autosave|--use_bounding_boxes]* <images_directory_path> <annotations_directory_path> <class_names_filepath>")
        
    if len(sys.argv) < 4:
        print_help_message()
        sys.exit(1)
    
    images_directory_path, annotations_directory_path = sys.argv[-3:-1]
    if not os.path.isdir(images_directory_path):
        print(f'Error: The directory "{images_directory_path}" does not exist.')
        print_help_message()
        sys.exit(2)
        
    class_names_filepath = sys.argv[-1]
    if not os.path.isfile(class_names_filepath):
        print(f'Error: The file "{class_names_filepath}" does not exist.')
        print_help_message()
        sys.exit(3)
    
    with open(class_names_filepath) as file:
        class_names = [line.strip() for line in file.readlines() if line.strip()]
    
    app = QApplication(sys.argv)
    window = ImageAnnotatorWindow(
        images_directory_path, annotations_directory_path,
        label_color_pairs=class_names,
        void_background='--void_background' in sys.argv,
        use_bounding_boxes='--use_bounding_boxes' in sys.argv,
        autosave='--autosave' in sys.argv,
        verbose='--verbose' in sys.argv
    )
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()