# ------------------ Factory functions ------------------        
from .icsv_file import iCSVFile, FIRSTLINES
from .application_profile import iCSVSnowprofile, FIRSTLINES_SNOWPROFILE
from ..pysmet import SMETFile

def read(filename: str) -> iCSVFile:
    """
    Reads an iCSV file and returns an iCSVFile object (or the respective application profile specific object).

    Args:
        filename (str): The path to the iCSV file.

    Returns:
        iCSVFile/ApplicationProfile: An iCSVFile or subclass object representing the contents of the file.
        
    The iCSVFile object has the following attributes:
        - metadata: The metadata section of the iCSV file.
            access attributes via metadata.get_attribute("key")
        - fields: The fields section of the iCSV file.
            access attributes via fields.get_attribute("key")
        - geometry: The geometry section of the iCSV file.
            get the location via geometry.get_location()
        - data: The data section of the iCSV file.
            As a pandas DataFrame.
        - filename: The name of the iCSV file.
        - skip_lines: The number of lines to skip when reading the file.
    """
    firstline = open(filename).readline().rstrip()
    if firstline in FIRSTLINES_SNOWPROFILE:
        return iCSVSnowprofile(filename)
    elif firstline in FIRSTLINES:
        return iCSVFile(filename)
    else:
        raise ValueError("Not an iCSV file")
    
                
def from_smet(smet: SMETFile) -> iCSVFile:
    """
    Converts an SMETFile object to an iCSVFile object.

    Args:
        smet (SMETFile): The SMETFile object to convert.

    Returns:
        iCSVFile: The converted iCSVFile object.
    """
    icsv = iCSVFile()
    _set_fields_and_location(icsv, smet)
    _set_metadata(icsv, smet)
    icsv.data = smet.data
    _check_validity_and_parse_geometry(icsv, icsv.data.shape[1])
    return icsv

def _set_fields_and_location(icsv, smet):
    icsv.fields.set_attribute("fields", smet.meta_data.fields)
    loc = smet.meta_data.location
    _set_location_attributes(icsv, loc)

def _set_location_attributes(icsv, loc):
    if not loc.epsg and not loc.is_latlon():
        raise ValueError("EPSG code not provided")
    elif loc.is_latlon():
        loc.epsg = 4326
        x = loc.longitude
        y = loc.latitude
    else:
        x = loc.easting
        y = loc.northing
    z = loc.altitude
    geometry = f"POINTZ({x} {y} {z})"
    icsv.metadata.set_attribute("geometry", geometry)
    srid = f"EPSG:{loc.epsg}"
    icsv.metadata.set_attribute("srid", srid)
    icsv.metadata.set_attribute("field_delimiter", ",")

def _set_metadata(icsv:iCSVFile, smet:SMETFile):
    icsv.metadata.set_attribute("nodata", smet.meta_data.nodata)
    icsv.metadata.set_attribute("station_id", smet.meta_data.station_id)
    _set_meta_data_attributes(icsv, smet.optional_meta_data.adjusted_dict)
    _set_meta_data_attributes(icsv, smet.other_meta_data)
    for key, value in smet.acdd_meta_data.adjusted_dict:
        icsv.metadata.set_attribute(key, value)

def _set_meta_data_attributes(icsv:iCSVFile, meta_data):
    for key, value in meta_data.items():
        if value:
            if isinstance(value, list) and len(value) == len(icsv.fields.fields):
                icsv.fields.set_attribute(key, value)
            elif isinstance(value, str) and len(value.split(" ")) == len(icsv.fields.fields):
                icsv.fields.set_attribute(key, value.split(" "))
            else:
                icsv.metadata.set_attribute(key, value)

def _check_validity_and_parse_geometry(icsv, ncols:int):
    icsv.metadata.check_validity()
    icsv.fields.check_validity(ncols)
    icsv.parse_geometry()