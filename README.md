# EEG Annotation Tool

EEG annotation tool written in Python and PyQt6. It uses MNE Python for EEG signal reading and processing.

![demo](icons/demo.gif)

## Installation

1. Clone the repository.
2. Install the required packages using the following command:

   ``` bash
   pip3 install -r requirements.txt
   ```

## Usage

1. Run the following command to start the application:

   ``` bash
   python3 main.py
   ```

2. Load your EEG data by clicking on the "Open" button.
3. Use the "Bounding Rect Annotation" feature to annotate your data by pressing the `Select` button, left click and drag your mouse on the canvas to draw a rectangle selection.
4. You can move and resize the rectangle as you wish. When finish press the `Select` button again to provide annotation to the selected region.
5. Save your annotations by clicking on the "Save Annotations" button.
6. Use the left/right arrow keys to move through the EEG signal in time.

You can also change the bipolar montage type or add/remove labels in the `config.py` file

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
