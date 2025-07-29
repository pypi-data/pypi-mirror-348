from dataclasses import dataclass as dat
from typing import List

from ..Utils.ACDD import ACDDMetadata
from .utility import is_number


# TODO: implement support for application profiles
class MetaDataSection:
    """
    A class used to represent the metadata section of an iCSV file.

    Attributes:
        required_attributes (dict): Attributes that are required to be present in the metadata.
        recommended_attributes (dict): Attributes that are recommended to be present in the metadata.
        acdd_metadata (dict): Metadata that is part of the ACDD standard.
        other_metadata (dict): Metadata that is not part of the ACDD standard.

    Methods:
        check_validity():
            Performs a sanity check.
        __str__():
            Returns a string representation of the metadata.
        set_attribute(attribute_name: str, value: any):
            Sets an attribute.
        get_attribute(attribute_name: str):
            Returns an attribute.
        metadata:
            Returns all metadata.
        join(other: MetaDataSection):
            Joins two metadata sections.
    """
    def __init__(self):
        self.required_attributes = {
            "field_delimiter": None,
            "geometry": None,
            "srid": None,
        }
        self.recommended_attributes = {
            "station_id": None,
            "nodata": None,
            "timezone": None,
            "doi": None,
            "timestamp_meaning": None,
        }
        self.acdd_metadata = ACDDMetadata()
        self.other_metadata = {}

    def __str__(self):
        required_attribute_string = "\n".join(
            f"{key} : {value}"
            for key, value in self.required_attributes.items()
            if value is not None
        )
        recommended_attribute_string = "\n".join(
            f"{key} : {value}"
            for key, value in self.recommended_attributes.items()
            if value is not None
        )
        other_metadata_string = "\n".join(
            f"{key} : {value}"
            for key, value in self.other_metadata.items()
            if value is not None
        )
        return f"METADATA:\nRequired:\n{required_attribute_string}\nRecommended:\n{recommended_attribute_string}\n{self.acdd_metadata}\nOther Metadata:\n{other_metadata_string}"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, MetaDataSection):
            return False

        for attr in ["required_attributes", "recommended_attributes", "other_metadata"]:
            self_dict = getattr(self, attr)
            value_dict = getattr(value, attr)

            common_keys = self_dict.keys() & value_dict.keys()

            for key in common_keys:
                if self_dict[key] is not None and value_dict[key] is not None:
                    if self_dict[key] != value_dict[key]:
                        return False

        return self.acdd_metadata == value.acdd_metadata

    def init_application(self, application_profile):
        pass

    def check_validity(self):
        for key, value in self.required_attributes.items():
            if value is None:
                raise ValueError(f"Required attribute {key} is missing")

    def set_attribute(self, attribute_name, value):
        if is_number(value):
            value = float(value)

        if attribute_name in self.required_attributes:
            self.required_attributes[attribute_name] = value
        elif attribute_name in self.recommended_attributes:
            self.recommended_attributes[attribute_name] = value

        if not self.acdd_metadata.set_attribute(attribute_name, value):
            self.other_metadata[attribute_name] = value

    def get_attribute(self, attribute_name):
        if attribute_name in self.required_attributes:
            return self.required_attributes[attribute_name]
        elif attribute_name in self.recommended_attributes:
            return self.recommended_attributes[attribute_name]
        else:
            if self.acdd_metadata.get_attribute(attribute_name):
                return self.acdd_metadata.get_attribute(attribute_name)
            if attribute_name in self.other_metadata:
                return self.other_metadata[attribute_name]
            return None

    def join(self, other: "MetaDataSection"):
        for attr_dict in [
            other.required_attributes,
            other.recommended_attributes,
            other.other_metadata,
        ]:
            for attribute, value in attr_dict.items():
                self_value = self.get_attribute(attribute)
                if value and not self_value:
                    self.set_attribute(attribute, value)
                elif value and self_value != value:
                    print(
                        f"Attribute {attribute} is different in both MetaDataSection objects"
                    )

        self.acdd_metadata.join(other.acdd_metadata)

    @property
    def metadata(self) -> dict:
        return {
            **self.required_attributes,
            **{k: v for k, v in self.recommended_attributes.items() if v},
            **{k: v for k, v in self.other_metadata.items() if v},
            **self.acdd_metadata.adjusted_dict,
        }


class FieldsSection:
    """
    A class used to represent the fields section of an iCSV file.

    Attributes:
        fields (list): List of fields.
        recommended_fields (list): Fields that are recommended to be present in the fields section.
        other_fields (list): Fields that are not recommended to be present in the fields section.

    Methods:
        check_validity(n_cols: int):
            Performs a sanity check.
        __str__():
            Returns a string representation of the fields.
        set_attribute(attribute_name: str, value: list):
            Sets an attribute.
        get_attribute(attribute_name: str):
            Returns an attribute.
        all_fields:
            Returns all fields.
        miscellaneous_fields:
            Returns all fields that are not required.
    """
    def __init__(self):
        self.fields = []
        self.recommended_fields = {
            "units_multiplier": [],
            "units": [],
            "long_name": [],
            "standard_name": [],
        }
        self.other_fields = {}

    def __str__(self):
        recommended_fields_string = "\n".join(
            f"{key} : {value}"
            for key, value in self.recommended_fields.items()
            if value
        )
        other_fields_string = "\n".join(
            f"{key} : {value}" for key, value in self.other_fields.items() if value
        )
        return f"Fields: {self.fields}\nRecommended Fields:\n{recommended_fields_string}\nOther Fields:\n{other_fields_string}"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, FieldsSection):
            return False
        for attr in ["fields", "recommended_fields", "other_fields"]:
            self_dict = getattr(self, attr)
            value_dict = getattr(value, attr)

            if self_dict != value_dict:
                return False
        return True

    def check_validity(self, n_cols: int):
        if not self.fields:
            raise ValueError("No fields provided")

        if len(self.fields) != n_cols:
            raise ValueError("Number of fields does not match the number of columns")
        for key, val in self.recommended_fields.items():
            if val and len(self.recommended_fields[key]) != n_cols:
                raise ValueError(
                    f"Number of {key} does not match the number of columns"
                )

        for key, val in self.other_fields.items():
            if val and len(self.other_fields[key]) != n_cols:
                raise ValueError(
                    f"Number of {key} does not match the number of columns"
                )

    def set_attribute(self, attribute_name, value: list):
        value = [float(val) if is_number(val) else val for val in value]
        if attribute_name == "fields":
            self.fields = value
        elif attribute_name in self.recommended_fields:
            self.recommended_fields[attribute_name] = value
        else:
            self.other_fields[attribute_name] = value

    def get_attribute(self, attribute_name):
        if attribute_name == "fields":
            return self.fields
        elif attribute_name in self.recommended_fields:
            return self.recommended_fields[attribute_name]
        else:
            if attribute_name in self.other_fields:
                return self.other_fields[attribute_name]
            return None

    @property
    def all_fields(self):
        return {
            "fields": self.fields,
            **{k: v for k, v in self.recommended_fields.items() if v},
            **{k: v for k, v in self.other_fields.items() if v},
        }

    @property
    def miscalleneous_fields(self):
        return {
            **{k: v for k, v in self.recommended_fields.items() if v},
            **{k: v for k, v in self.other_fields.items() if v},
        }


@dat
class Loc:
    x: float = None
    y: float = None
    z: float = None
    epsg: int = None

    def __str__(self):
        return f"X: {self.x}\nY: {self.y}\nZ: {self.z}\nEPSG: {self.epsg}"

    def is_valid(self):
        return self.x is not None and self.y is not None and self.epsg is not None


class Geometry:
    """
    Represents the location information in an icsv file.

    Attributes:
        geometry (str): The original geometry string.
        srid (str): The SRID of the geometry.
        column_name (str): The name of the column where the geometry is stored (if applicable).
        location (Loc): The location information in a dataclass with x, y, z, and epsg attributes.

    Methods:
        __str__:
            Returns a string representation of the geometry.
        __eq__(value: object):
            Returns True if the value is equal to the geometry.
        set_location:
            Sets the location information based on the geometry string.
    """
    def __init__(self):
        self.geometry = None
        self.srid = None
        self.column_name = None
        self.location = Loc()

    def __str__(self):
        if self.column_name:
            return f"SRID: {self.srid}\nin column: {self.column_name}"
        return (
            f"Geometry: {self.geometry}\nSRID: {self.srid}\nLocation: {self.location}"
        )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Geometry):
            return False
        return self.geometry == value.geometry and self.srid == value.srid

    def set_location(self):
        if "POINTZ" in self.geometry:
            content = self.geometry.split("(")[1].split(")")[0]
            vals = content.split(" ")
            if len(vals) != 3:
                raise ValueError("Invalid POINTZ geometry")
            self.location.x = float(vals[0])
            self.location.y = float(vals[1])
            self.location.z = float(vals[2])
        elif "POINT" in self.geometry:
            content = self.geometry.split("(")[1].split(")")[0]
            vals = content.split(" ")
            if len(vals) != 2:
                raise ValueError("Invalid POINT geometry")
            self.location.x = float(vals[0])
            self.location.y = float(vals[1])
        else:
            print("Unsupported geometry type")
        self.location.epsg = self.srid.split(":")[1]
    
    def get_location(self):
        if self.location.is_valid():
            return self.location
        return self.geometry
