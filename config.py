from dataclasses import dataclass


@dataclass()
class Config:
    app_name = " Annotate"
    # diagnosis options
    diagnosis = ["BCKG", "SCZ"]
    montage_pairs = {
        "Fp1-F7": ("Fp1", "F7"),
        "F7-T3": ("F7", "T3"),
        "T3-T5": ("T3", "T5"),
        "T5-O1": ("T5", "O1"),
        "Fp2-F8": ("Fp2", "F8"),
        "F8-T4": ("F8", "T4"),
        "T4-T6": ("T4", "T6"),
        "T6-O2": ("T6", "O2"),
        "A1-T3": ("A1", "T3"),
        "T3-C3": ("T3", "C3"),
        "C3-Cz": ("C3", "Cz"),
        "Cz-C4": ("Cz", "C4"),
        "C4-T4": ("C4", "T4"),
        "T4-A2": ("T4", "A2"),
        "Fp1-F3": ("Fp1", "F3"),
        "F3-C3": ("F3", "C3"),
        "C3-P3": ("C3", "P3"),
        "P3-O1": ("P3", "O1"),
        "Fp2-F4": ("Fp2", "F4"),
        "F4-C4": ("F4", "C4"),
        "C4-P4": ("C4", "P4"),
        "P4-O2": ("P4", "O2"),
    }
    num_channels = len(montage_pairs)
