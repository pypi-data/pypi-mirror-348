import xarray as xr
from .icsv_file import iCSVFile, VERSIONS
from typing_extensions import override
import pandas as pd
import datetime
from typing import Optional

FIRSTLINES_SNOWPROFILE = [f"# iCSV {version} UTF-8 SNOWPROFILE" for version in VERSIONS]

class iCSVSnowprofile(iCSVFile):
    """
    Class to represent an iCSV file containing snow profile data.
    
    The iCSVSnowprofile extends the iCSVFile class to handle the specific structure
    and requirements of snow profile data, which includes multiple timestamped
    profile measurements and point measurements.
    
    Attributes (additional to iCSVFile):
        dates (list): List of datetime objects representing measurement dates in the file.
        date_lines (list): List of line numbers where date entries begin in the file.
        data (dict): Dictionary mapping datetime objects to pandas DataFrames containing
                    the profile data for that timestamp.
        
    Key Features:
        - Handles multiple time-stamped profiles in a single file
        - Separates point measurements from profile measurements
        - Provides methods to extract and filter point and profile values
        - Can convert to xarray Dataset for multi-dimensional data analysis
    
    The snowprofile format follows the iCSV specification with the addition of
    [DATE=timestamp] markers in the data section to separate measurements from
    different dates. Each profile must include a 'layer_number' field to identify
    profile layers versus point measurements.
    """
    def __init__(self, filename: str = None):
        self.dates = []
        self.date_lines = []
        super().__init__(filename)
        
    @override
    def _parse_comment_line(self, line, section, line_number):
        if line == "[METADATA]":
            return "metadata"
        elif line == "[FIELDS]":
            self.metadata.check_validity()  # to parse fields we need valid metadata
            return "fields"
        elif line == "[DATA]":
            return "data"
        else:
            return self._parse_section_line(line, section, line_number)
    
    @override
    def _parse_section_line(self, line, section, line_number):
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
            if "[DATE=" in line:
                date_str = line.split('[DATE=')[1].split(']')[0].strip()
                self.dates.append(datetime.datetime.fromisoformat(date_str))
                self.date_lines.append(line_number)
            else:   
                raise ValueError(f"Invalid data line: {line}")
        
        return section
    
    @override
    def load_file(self, filename: str = None):
        """Loads an iCSV file and parses its contents, extracting the dates and data lines for a snow profile.

        Args:
            filename (str, optional): The path to the iCSV file. If not provided, the previously set filename will be used.

        Raises:
            ValueError: If the file is not a valid iCSV file or if the data section is not specified.

        Returns:
            None
        """
        self.data = dict()
        if filename:
            self.filename = filename
            
        section = ""
        with open(self.filename, 'r') as file:
            first_line = file.readline().rstrip()  # rstrip() is used to remove the trailing newline
            if first_line not in FIRSTLINES_SNOWPROFILE:
                raise ValueError("Not an iCSV file with the snowprofile application profile")
        
            line_number = 1 # need to find the line number where the data starts
            for line in file:
                line_number += 1
                if line.startswith("#"):
                    line = line[1:].strip()
                    section = self._parse_comment_line(line.strip(), section, line_number)
                else:
                    if section != "data":
                        raise ValueError("Data section was not specified")
                
        
        for (i, date) in enumerate(self.dates):
            first_data_line = self.date_lines[i]
            last_data_line = self.date_lines[i+1] if i+1 < len(self.dates) else line_number + 1
            self.data[date] = pd.read_csv(self.filename, skiprows=first_data_line, nrows=last_data_line-first_data_line-1, header=None, sep=self.metadata.get_attribute("field_delimiter"))
            self.data[date].columns = self.fields.fields
            
        self.fields.check_validity(self.data[self.dates[0]].shape[1]) # check if the number of fields match the number of columns
        self.parse_geometry()
        
    @override
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
        print("\nDates:")
        print(self.dates)
        print("\nFirst Profile:")
        print(self.data[self.dates[0]].head())
        
    @override
    def to_xarray(self):
        """
        Converts the data to a single 3D xarray Dataset with 'time' as one dimension.

        Returns:
            xarray.Dataset: The combined xarray dataset.
        """

        # Convert each DataFrame to xarray DataArray
        arrays = []
        for date in self.dates:
            df = self.data[date].copy()
            df.set_index("layer_number", inplace=True)
            arrays.append(df.to_xarray())
        # Concatenate along new time dimension
        ds = xr.concat(arrays, dim="time")
        ds = ds.assign_coords(time=self.dates)
        # Optionally add metadata
        ds.attrs = self.metadata.metadata
        return ds

    @override
    def setData(self, timestamp: datetime.datetime, data: pd.DataFrame, colnames: Optional[list] = None):
        if not self.data:
            self.data = dict()
        
        self.data[timestamp] = data
    
    @override
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
        if "model" not in self.metadata.metadata:
            raise ValueError("model is a required metadata for the Snowprofile application profile")
        self.fields.check_validity(self.data[self.dates[0]].shape[1])
        if "layer_number" not in self.fields.fields:
            raise ValueError("layer_number is a required field for the Snowprofile application profile")
        
        with open(self.filename, 'w') as file:
            file.write(f"{FIRSTLINES_SNOWPROFILE[-1]}\n")
            file.write("# [METADATA]\n")
            for key, val in self.metadata.metadata.items():
                file.write(f"# {key} = {val}\n")
            file.write("# [FIELDS]\n")
            for key, val in self.fields.all_fields.items():
                fields_string = self.metadata.get_attribute("field_delimiter").join(str(value) for value in val)
                file.write(f"# {key} = {fields_string}\n")
            file.write("# [DATA]\n")
            for date in self.dates:
                file.write(f"# [DATE={date.isoformat()}]\n")
                self.data[date].to_csv(file, mode='a', index=False, header=False, sep=self.metadata.get_attribute("field_delimiter") )
                
    def get_point_values(self):
        """
        Extracts point measurements from the snow profile data.
        
        Retrieves all data rows where 'layer_number' equals 'point' across all dates,
        combining them into a single DataFrame with timestamps. Automatically filters
        out columns that contain only nodata values.
        
        Returns:
            pandas.DataFrame: DataFrame containing all point measurements with timestamps,
                             with columns filtered to include only those with valid data.
                             Returns an empty DataFrame if no point measurements are found.
        """

        nodata = self.metadata.get_attribute("nodata")
        point_rows = []
        for date in self.dates:
            data_at_date = self.data[date]
            if "point" not in data_at_date["layer_number"].values:
                continue
            point_df = data_at_date[data_at_date["layer_number"] == "point"].copy()
            point_df.insert(0, "timestamp", date)
            point_rows.append(point_df)
        if not point_rows:
            return pd.DataFrame(), []  # Empty DataFrame and empty list if no points found

        all_points = pd.concat(point_rows, ignore_index=True)
        # Exclude the 'timestamp' and 'layer_number' columns from nodata filtering
        cols_to_check = [col for col in all_points.columns if col not in ["timestamp", "layer_number"]]
        # Find columns where not all values are -999
        valid_cols = [col for col in cols_to_check if not (all_points[col] == nodata).all()]
        # Always keep 'timestamp' and 'layer_number'
        final_cols = ["timestamp"] + valid_cols
        filtered_points = all_points[final_cols]
        return filtered_points

    def get_profile_values(self, as_xarray=False):
        """
        Extracts profile measurements from the snow profile data.
        
        Retrieves all data rows where 'layer_number' is not 'point' across all dates,
        organizing them by timestamp. Automatically filters out columns containing only
        nodata values for each profile.
        
        Args:
            as_xarray (bool, optional): If True, returns data as an xarray Dataset with
                                       dimensions (time, layer) instead of a dictionary.
                                       Default is False.
        
        Returns:
            dict or xarray.Dataset: If as_xarray=False (default), returns a dictionary mapping
                                   datetime objects to pandas DataFrames with layer_number as index.
                                   If as_xarray=True, returns a multi-dimensional xarray Dataset with
                                   dimensions of time and layer, and variables for each measurement type.
        """

        NODATA = self.metadata.get_attribute("nodata")
        profiles_dict = {}
        for date in self.dates:
            data_at_date = self.data[date]
            profile_df = data_at_date[data_at_date["layer_number"] != "point"].copy()
            colnames = profile_df.columns
            # Remove columns where all values are -999 (except 'layer_number')
            valid_cols = [col for col in colnames if not (profile_df[col] == NODATA).all()]
            filtered_df = profile_df[valid_cols]
            profiles_dict[date] = filtered_df.set_index("layer_number")
        if as_xarray and profiles_dict:
            # Convert to xarray Dataset: dims=time, layer, variables=fields
            # Find union of all columns
            all_vars = set()
            for df in profiles_dict.values():
                all_vars.update(df.columns)
            all_vars = sorted(all_vars)
            # Build a 3D array: (time, layer, variable)
            times = list(profiles_dict.keys())
            max_layers = max(len(df) for df in profiles_dict.values())
            data = {var: [] for var in all_vars}
            layer_numbers = []
            for date in times:
                df = profiles_dict[date]
                layer_numbers.append(df.index.tolist() + [None]*(max_layers - len(df)))
                for var in all_vars:
                    col_data = df[var].tolist() if var in df.columns else [NODATA]*len(df)
                    col_data += [NODATA]*(max_layers - len(col_data))
                    data[var].append(col_data)
            ds = xr.Dataset(
                {var: (['time', 'layer'], data[var]) for var in all_vars},
                coords={
                    'time': times,
                    'layer': range(max_layers),
                    'layer_number': (['time', 'layer'], layer_numbers)
                }
            )
            return ds
        return profiles_dict

def append_timepoint(filename: str, timestamp: datetime.datetime, data: pd.DataFrame, field_delimiter: str = ","):
    """
    Appends a new timepoint to the iCSV file.

    Args:
        filename (str): The name of the file to append to.
        timestamp (datetime.datetime): The timestamp of the new timepoint.
        data (pd.DataFrame): The data to append.

    Returns:
        None
    """
    with open(filename, 'a') as file:
        file.write(f"# [DATE={timestamp.isoformat()}]\n")
        data.to_csv(file, mode='a', index=False, header=False, sep=field_delimiter)
    