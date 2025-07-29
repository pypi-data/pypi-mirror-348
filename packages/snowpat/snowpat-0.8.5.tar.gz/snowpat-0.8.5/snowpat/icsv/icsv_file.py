import pandas as pd
import xarray as xr
from typing import Optional

from .header import MetaDataSection, FieldsSection, Geometry


VERSIONS = ["1.0"]
FIRSTLINES = [f"# iCSV {version} UTF-8" for version in VERSIONS]

class iCSVFile:
    """
    Class to represent an iCSV file.
    
    Attributes:
        metadata (MetadataSection): Metadata section of the iCSV file.
        fields (FieldsSection): Fields section of the iCSV file.
        geometry (Representation class): Geometry section of the iCSV file.
        data (pd.Dataframe): Data section of the iCSV file.
        filename: The name of the iCSV file.
        skip_lines: The number of lines to skip when reading the file.
        
    Methods:
        load_file(filename: str = None): Load an iCSV file.
        parse_geometry(): Parse the geometry section of the iCSV file.
        info(): Print a summary of the iCSV file.
        to_xarray(): Convert the iCSV file to an xarray dataset.
        setData(data: pd.DataFrame, colnames: Optional[list] = None): Set the data of the iCSV file.
        write(filename: str = None): Write the iCSV file to a file.
    """
    def __init__(self, filename:str = None):
        self.metadata = MetaDataSection()
        self.fields = FieldsSection()
        self.geometry = Geometry()
        self.data = None
        self.filename = filename
        self.skip_lines = 0
        
        if self.filename:
            self.load_file()
            
    
    def __str__(self) -> str:
        return f"File: {self.filename}\n{self.metadata}\n{self.fields}\n{self.geometry}"
    
    def __eq__(self, value: object) -> bool:
        try:
            for attr in ['metadata', 'fields', 'geometry']:
                self_value = getattr(self, attr)
                value_value = getattr(value, attr)
                
                if self_value != value_value:
                    return False
            return True
        except AttributeError:
            return False
    
    def _parse_comment_line(self, line, section):
        if line == "[METADATA]":
            return "metadata"
        elif line == "[FIELDS]":
            self.metadata.check_validity()  # to parse fields we need valid metadata
            return "fields"
        elif line == "[DATA]":
            return "data"
        else:
            return self._parse_section_line(line, section)

    def _parse_section_line(self, line, section):
        if not section:
            raise ValueError("No section specified")
        line_vals = line.split("=")
        if len(line_vals) != 2:
            raise ValueError(f"Invalid {section} line: {line}, got 2 assignment operators \"=\"")

        if section == "metadata":
            self.metadata.set_attribute(line_vals[0].strip(), line_vals[1].strip())
        elif section == "fields":
            fields_vec = [field.strip() for field in line_vals[1].split(self.metadata.get_attribute("field_delimiter"))]
            self.fields.set_attribute(line_vals[0].strip(), fields_vec)
        elif section == "data":
            raise TypeError("Data section should not contain any comments")

        return section

    def _update_columns(self):
        self.data.columns = self.fields.fields
        for field in ["time", "timestamp"]:
            if field in self.fields.fields:
                self.data[field] = pd.to_datetime(self.data[field])          
    
    def load_file(self, filename: str = None):
        """Loads an iCSV file and parses its contents.

        Args:
            filename (str, optional): The path to the iCSV file. If not provided, the previously set filename will be used.

        Raises:
            ValueError: If the file is not a valid iCSV file or if the data section is not specified.

        Returns:
            None
        """
        if filename:
            self.filename = filename
            
        section = ""
        with open(self.filename, 'r') as file:
            first_line = file.readline().rstrip()  # rstrip() is used to remove the trailing newline
            if first_line not in FIRSTLINES:
                raise ValueError("Not an iCSV file")
        
            line_number = 1 # need to find the line number where the data starts
            for line in file:
                if line.startswith("#"):
                    line_number += 1
                    line = line[1:].strip()
                    section = self._parse_comment_line(line.strip(), section)
                else:
                    if section != "data":
                        raise ValueError("Data section was not specified")
                    self.skip_lines = line_number
                    break
        
        self.data = pd.read_csv(self.filename, skiprows=self.skip_lines, header=None, sep=self.metadata.get_attribute("field_delimiter"))
        self.fields.check_validity(self.data.shape[1]) # check if the number of fields match the number of columns
        self._update_columns()           
        self.parse_geometry()
        
    def parse_geometry(self):
        if self.metadata.get_attribute("geometry") in self.fields.get_attribute("fields"):
            self.geometry.geometry = self.metadata.get_attribute("geometry")
            self.geometry.srid = self.metadata.get_attribute("srid")
            self.geometry.column_name = self.metadata.get_attribute("column_name")
        else:
            self.geometry.geometry = self.metadata.get_attribute("geometry")
            self.geometry.srid = self.metadata.get_attribute("srid")
            self.geometry.set_location()    
            
    def info(self):
        """
        Prints information about the object and its data.

        This method prints the object itself and the head of its data.

        Args:
            None

        Returns:
            None
        """
        print(self)
        print("\nData:")
        print(self.data.head())
    
    def to_xarray(self) -> xr.Dataset:
        """
        Converts the data to an xarray dataset.

        Returns:
            xarray.Dataset: The converted xarray dataset.
        """
        arr = self.data.to_xarray()
        arr.attrs = self.metadata.metadata
        for i,var in enumerate(arr.data_vars):
            for _, vec in self.fields.miscalleneous_fields.items():
                arr[var].attrs = vec[i]
                
    def setData(self, data: pd.DataFrame, colnames: Optional[list] = None):
        """
        Sets the data of the iCSV file.

        Args:
            data (pd.DataFrame): The data to set.
            colnames (list): The names of the columns in the data.

        Returns:
            None
        """
        self.data = data
        if colnames:
            if len(colnames) != self.data.shape[1]:
                raise ValueError("Number of columns in data does not match the number of column names")
            self.fields.set_attribute("fields", colnames)
        else:
            colnames = self.data.columns.to_list()
            if colnames[0] == "0" or colnames[0] == 0:
                raise ValueError("Column names are not provided")
            self.fields.set_attribute("fields", colnames)
                # Ensure 'timestamp' is the first column if it exists
        if 'timestamp' in self.data.columns:
            cols = self.data.columns.tolist()
            if cols[0] != 'timestamp':
                cols.insert(0, cols.pop(cols.index('timestamp')))
                self.data = self.data[cols]
            self.fields.set_attribute("fields", self.data.columns)

            
        
                
    def write(self, filename: str = None):
        """
        Writes the metadata, fields, and data to a CSV file.

        Args:
            filename (str, optional): The name of the file to write. If not provided, the current filename will be used.

        Returns:
            None
        """
        
        if filename:
            self.filename = filename
            
        self.metadata.check_validity()
        self.fields.check_validity(self.data.shape[1])
        
            

        
        with open(self.filename, 'w') as file:
            file.write(f"{FIRSTLINES[-1]}\n")
            file.write("# [METADATA]\n")
            for key, val in self.metadata.metadata.items():
                file.write(f"# {key} = {val}\n")
            file.write("# [FIELDS]\n")
            for key, val in self.fields.all_fields.items():
                fields_string = self.metadata.get_attribute("field_delimiter").join(str(value) for value in val)
                file.write(f"# {key} = {fields_string}\n")
            file.write("# [DATA]\n")
            
        self.data.to_csv(self.filename, mode='a', index=False, header=False, sep=self.metadata.get_attribute("field_delimiter"))
    
        
