"""Module for the Reference class"""
from enum import Enum
from constants import NUMBER_KEYS, INPROCEEDINGS_KEYS, INPROCEEDINGS_MANDATORY_KEYS


class ReferenceType(Enum):
    """Enum for supported reference types.
    
    The enum value for each type is the bibtex literal for that type.
    """
    INPROCEEDINGS = "inproceedings"

    def get_keys(self):
        """Get field keys for this enum instance."""
        match self.name:
            case "INPROCEEDINGS":
                return INPROCEEDINGS_KEYS

    def get_mandatory_keys(self):
        """Get mandatory field keys for this enum instance."""
        match self.name:
            case "INPROCEEDINGS":
                return INPROCEEDINGS_MANDATORY_KEYS


class Reference:
    """Class for references.
    
    Args:
        reference_type (ReferenceType): type of reference
        key (str): unique identifier for reference
        fields (dict): field-value pairs for reference
    """
    def __init__(self, reference_type: ReferenceType, key: str, fields: dict):
        self.reference_type = reference_type
        self.key = key
        self.fields = fields

    def __str__(self):
        bibtex_fields = []
        for key, value in self.fields.items():

            printable_value = ""

            if key in NUMBER_KEYS:
                printable_value = value
            else:
                printable_value = "{" + str(value) + "}"

            bibtex_fields.append(f"    {key:<13}= {printable_value}")

        return f"@{self.reference_type.value}{{{self.key},\n" + ",\n".join(bibtex_fields) + "\n}\n"
