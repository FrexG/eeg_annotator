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

2. Load your EEG data by clicking on the "Load Data" button.
3. Use the "Bounding Rect Annotation" feature to annotate your data.
4. Save your annotations by clicking on the "Save Annotations" button.

You can change the bipolar montage type or add/remove labels in the `config.py` file

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
