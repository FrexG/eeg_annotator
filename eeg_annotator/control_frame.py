from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtWidgets import QToolBar, QPushButton, QSpinBox, QLabel, QLineEdit


class ControlToolBar(QToolBar):
    def __init__(self, controller):
        super(ControlToolBar, self).__init__()

        self.controller = controller

        self.open_file = QPushButton("Open")
        self.open_file.setIcon(QIcon("./icons/folder.png"))
        self.open_file.clicked.connect(self.on_open_clicked)

        self.save_btn = QPushButton("Save Annotation")
        self.save_btn.setIcon(QIcon("./icons/diskette.png"))
        self.save_btn.clicked.connect(self.on_save_clicked)
        self.save_btn.setEnabled(False)

        self.undo_btn = QPushButton("Undo")
        self.undo_btn.setIcon(QIcon("./icons/undo.png"))
        self.undo_btn.setEnabled(False)
        self.undo_btn.clicked.connect(self.on_undo_clicked)
        # draw box btn
        self.draw_selection_btn = QPushButton("Label")
        self.draw_selection_btn.setIcon(QIcon("./icons/add-selection.png"))
        self.draw_selection_btn.setEnabled(False)
        self.draw_selection_btn.clicked.connect(self.on_selection_box_clicked)

        self.toggle_guide_btn = QPushButton("Grid")
        self.toggle_guide_btn.clicked.connect(self.on_enable_grid)

        # display time(x-limit) controll
        self.spinner_label = QLabel("Max display samples: ")
        self.x_lim_spinner = QSpinBox()

        # Goto a given seconds to a signal
        self.goto_input = QLineEdit()
        self.goto_input.setMaxLength(10)
        self.goto_input.setFixedWidth(100)
        self.goto_input.setPlaceholderText("Goto in seconds")
        # add signal,(detect Enter/return key presses)
        self.goto_input.returnPressed.connect(self.on_return_pressed)
        # create a validotr property for QLineEdit
        int_validator = QIntValidator()
        self.goto_input.setValidator(int_validator)

        self.signal_duration_lbl = QLabel()
        self.sampling_freq_lbl = QLabel()

        self.addWidget(self.open_file)
        self.addWidget(self.save_btn)
        self.addWidget(self.undo_btn)
        self.addWidget(self.draw_selection_btn)
        self.addWidget(self.toggle_guide_btn)
        self.addWidget(self.spinner_label)
        self.addWidget(self.x_lim_spinner)
        self.addWidget(self.goto_input)
        self.addWidget(self.signal_duration_lbl)
        self.addWidget(self.sampling_freq_lbl)
        self.show()

    def show_controls(self, signal_duration, s_freq):
        self.signal_duration = signal_duration
        self.s_freq = s_freq

        self.x_lim_spinner.setMinimum(5)
        self.x_lim_spinner.setMaximum(signal_duration // 2)
        self.x_lim_spinner.setValue(10)
        self.x_lim_spinner.setSingleStep(5)
        self.x_lim_spinner.setSuffix(" Seconds")
        self.x_lim_spinner.valueChanged.connect(self.on_spinner_value_changed)

        self.signal_duration_lbl.setText(f"Duration = {signal_duration}s")
        self.sampling_freq_lbl.setText(f"Sampling Freq = {s_freq}hz")
        self.show()

    def on_open_clicked(self):
        self.controller.open_file()

    def on_save_clicked(self):
        self.controller.eeg_plot_widget.save_annotation()

    def on_selection_box_clicked(self):
        self.controller.eeg_plot_widget.box_select()

    def on_spinner_value_changed(self, v):
        self.controller.eeg_plot_widget.change_initial_x_lim(v)

    def on_return_pressed(self):
        # Get the entered number
        entered_number = int(self.goto_input.text())
        self.controller.eeg_plot_widget.goto_duration(
            entered_number, self.signal_duration
        )

    def on_undo_clicked(self):
        if not self.controller.eeg_plot_widget.get_num_selectors():
            self.undo_btn.setEnabled(False)
            return
        self.controller.eeg_plot_widget.undo_selection()

    def on_enable_grid(self):
        self.controller.eeg_plot_widget.clear_v_lines()
