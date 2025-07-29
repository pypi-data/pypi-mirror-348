from typing import Dict, Optional, Tuple
import datetime
import json
import numpy as np
from .Snowpack import Snowpack
import warnings
import math

def read_json_profile(json_file: str, max_layer_size: Optional[float] = None) -> Tuple[Snowpack, Dict, datetime.datetime]:
    """
    Read a snowpack profile from a JSON file and convert it to a Snowpack object.
    
    Args:
        json_file (str): Path to the JSON file containing the snowpack profile
        max_layer_size (Optional[float]): Maximum allowed layer size. Layers exceeding this will be split.
        
    Returns:
        Tuple[Snowpack, Dict, datetime.datetime]: A tuple containing:
            - Snowpack object with the profile data
            - Dictionary with station metadata
            - Profile date
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract station metadata
    metadata = {
        "StationName": data["name"],
        "Latitude": data["position"]["latitude"],
        "Longitude": data["position"]["longitude"],
        "Altitude": data["position"]["altitude"],
        "SlopeAngle": data["position"]["angle"],
        "SlopeAzi": data["position"]["_azimuth"]
    }
    
    # Create Snowpack object
    snowpack = Snowpack()
    
    # Get the first profile (assuming single date)
    profile = data["profiles"][0]
    
    # Get profile date
    profile_date = datetime.datetime.fromisoformat(profile["date"])
    
    # Process layer data
    layers = []
    
    # Extract layers from hardness data (which contains the layer structure)
    hardness_data = profile["hardness"]["elements"][0]["layers"]
    
    # Sort layers by bottom height to ensure correct ordering
    hardness_data.sort(key=lambda x: x["bottom"])
    
    duplicate_layers = []
        
    # Convert layer boundaries to format needed by Snowpack
    boundaries = []
    for layer in hardness_data:
        if not boundaries:  # First layer
            boundaries.append(layer["bottom"])
        boundaries.append(layer["top"])
    
    # Convert hardness values to Newton scale if needed (assuming values > 6 indicate Newton scale)
    hardness_values = []
    is_newton = any(layer["value"] > 6 for layer in hardness_data)
    snowpack.isNewton = is_newton
    for layer in hardness_data:
        hardness_values.append(layer["value"])
    
    n_duplications = []
    if max_layer_size is not None:
        new_boundaries = []
        for i in range(len(boundaries) - 1):
            layer_size = boundaries[i+1] - boundaries[i]
            if layer_size > max_layer_size:
                # Calculate splits using numpy for better numerical precision
                n_splits = math.ceil(layer_size / max_layer_size)
                split_points = np.linspace(boundaries[i], boundaries[i+1], n_splits + 1, dtype=np.float64)
                
                # Add all points except the last one (it will be added in the next iteration)
                new_boundaries.extend(split_points[:-1])
            else:
                n_splits = 1
                new_boundaries.append(boundaries[i])
            n_duplications.append(n_splits)
            
        # Add final boundary
        new_boundaries.append(boundaries[-1])
        
        # Convert to numpy arrays
        boundaries = np.array(new_boundaries, dtype=np.float64)
    else:
        boundaries = np.array(boundaries, dtype=np.float64)
    
    hardness_values = np.array(hardness_values, dtype=np.float64)
    if n_duplications:
        assert len(n_duplications) == len(hardness_values), "Number of duplications does not match number of hardness values"
        hardness_values = np.repeat(hardness_values, n_duplications)
    # Set layer boundaries and hardness
    snowpack.set_param("0501", boundaries, len(boundaries))
    snowpack.set_param("0534", hardness_values, len(hardness_values))

    # make new fields, so it is clearer, where the layers actually are
    layer_middle = [
        (snowpack.layer_boundaries[i + 1] + snowpack.layer_boundaries[i]) / 2
        for i in range(snowpack.layer_boundaries.size - 1)
    ]
    layer_thicknes = [
        (snowpack.layer_boundaries[i + 1] - snowpack.layer_boundaries[i]) / 2
        for i in range(snowpack.layer_boundaries.size - 1)
    ]

    layer_middle = np.array(layer_middle)
    layer_thicknes = np.array(layer_thicknes)

    snowpack.data["layer middle"] = layer_middle
    snowpack.data["layer thickness"] = layer_thicknes
    if len(snowpack._height_mask) > len(layer_middle):
        snowpack._height_mask = np.delete(snowpack._height_mask, -1)

    # Process temperature data - the only property that should be interpolated
    if "temperature" in profile:
        temp_data = profile["temperature"]["elements"][0]["layers"]
        temp_values = []
        temp_pos = []
        for layer in temp_data:
            temp_values.append(layer["value"])
            temp_pos.append(layer["bottom"])
        
        # Convert to numpy arrays for efficient interpolation
        temp_pos = np.array(temp_pos, dtype=np.float64)
        temp_values = np.array(temp_values, dtype=np.float64)
        
        # Interpolate temperatures to layer midpoints
        temp_values = np.interp(layer_middle, temp_pos, temp_values)
        snowpack.set_param("0503", temp_values, len(temp_values))

    # Process density data - replicate values for split layers
    if "density" in profile:
        density_data = profile["density"]["elements"][0]["layers"]
        density_top = []
        density_bottom = []
        density_values = []
        for layer in density_data:
            if "value" in layer and layer["value"] is not None:
                density_values.append(layer["value"])
                density_top.append(layer["top"])
                density_bottom.append(layer["bottom"])
            else:
                density_values.append(0.0)  # Default value for missing data

        if density_values:
            # Convert to numpy array
            density_values = np.array(density_values, dtype=np.float64)
            density_top = np.array(density_top, dtype=np.float64)
            density_bottom = np.array(density_bottom, dtype=np.float64)
            density_boundaries = np.unique(np.concatenate([density_top, density_bottom]))
            density_boundaries.sort()
            if len(density_values) != len(layer_middle) or not all(density_boundaries == snowpack.layer_boundaries):
                print("Computing Mean densities for layers, provided density layers do not match layer boundaries")
                new_density_values = np.zeros(len(layer_middle))
                last_density_pos = 0
                for i in range(len(layer_middle)):
                    midpoint = layer_middle[i]
                    thickness = layer_thicknes[i]
                    layer_bottom = midpoint - thickness / 2
                    layer_top = midpoint + thickness / 2
                    # Weighted mean: compute overlap of density intervals with this layer
                    total_weight = 0.0
                    weighted_sum = 0.0
                    d_top = density_top[last_density_pos]
                    d_bottom = density_bottom[last_density_pos]
                    if d_top < layer_bottom:
                        last_density_pos = np.where(density_top >= layer_bottom)[0][0]
                        if not (last_density_pos > 0):
                            raise ValueError("Could not match density layers with layer boundaries")
                        d_top = density_top[last_density_pos]
                        d_bottom = density_bottom[last_density_pos]
                    if d_bottom > layer_top:
                        continue
                    
                    while d_bottom < layer_top:
                        layer_overlap = d_top - d_bottom if d_top < layer_top else layer_top - d_bottom
                        total_weight += layer_overlap
                        weighted_sum += layer_overlap * density_values[last_density_pos]
                        d_bottom = d_top
                        if d_bottom > layer_top:
                            break
                        last_density_pos += 1
                        if last_density_pos >= len(density_values):
                            warnings.warn("Not enough density layers to match with layer boundaries")
                            break
                        d_top = density_top[last_density_pos]
                        d_bottom = density_bottom[last_density_pos]
                    
                    if total_weight > 0:
                        new_density_values[i] = weighted_sum / total_weight
                    else:
                        new_density_values[i] = 0.0
                density_values = new_density_values
            elif n_duplications:
                assert len(density_values) == len(n_duplications), "Density values and duplications do not match, something went wrong when assigning layer splits"
                density_values = np.repeat(density_values, n_duplications)
            snowpack.set_param("0502", density_values, len(density_values))

    # Process grain shape data - replicate values for split layers
    if "grainshape" in profile:
        grain_data = profile["grainshape"]["elements"][0]["layers"]
        grain_codes = []
        for layer in grain_data:
            # Convert grain shape codes to Swiss Code format
            if isinstance(layer["value"], dict):
                primary = layer["value"]["primary"]
                secondary = layer["value"].get("secondary", "")
                tertiary_code = 0
                # Special case for MFcr
                if primary == "MFcr":
                    primary_code = 7
                    secondary_code = TYPES_TO_CODE.get(secondary, primary_code)
                    tertiary_code = 2
                else:
                    primary_code = TYPES_TO_CODE.get(primary, -1)
                    secondary_code = TYPES_TO_CODE.get(secondary, primary_code)
                    if primary_code == -1:
                        primary_code = -9
                        secondary_code = 9
                        tertiary_code = 9
                code = int(f"{primary_code}{secondary_code}{tertiary_code}")
            else:
                code = TYPES_TO_CODE.get(layer["value"], -999)
            
            grain_codes.append(code)
        
        if grain_codes:
            # Convert to numpy array
            grain_codes = np.array(grain_codes, dtype=np.int16)
            if n_duplications:
                assert len(grain_codes) == len(n_duplications), "Grain codes and duplications do not match, something went wrong when assigning layer splits"
                grain_codes = np.repeat(grain_codes, n_duplications)
            snowpack.set_param("0513", grain_codes, len(grain_codes))

    # Process grain size data - replicate values for split layers
    if "grainsize" in profile:
        size_data = profile["grainsize"]["elements"][0]["layers"]
        size_values = []
        for layer in size_data:
            if "value" in layer and layer["value"] is not None:
                size_values.append(layer["value"]["avg"])
            else:
                size_values.append(0.0)  # Default value for missing data
        if size_values:
            # Convert to numpy array
            size_values = np.array(size_values, dtype=np.float64)
            if n_duplications:
                assert len(size_values) == len(n_duplications), "Grain sizes and duplications do not match, something went wrong when assigning layer splits"
                size_values = np.repeat(size_values, n_duplications)
            snowpack.set_param("0512", size_values, len(size_values))

    # Process wetness data - replicate values for split layers
    if "wetness" in profile:
        wetness_data = profile["wetness"]["elements"][0]["layers"]
        wetness_values = []
        for layer in wetness_data:
            if "value" in layer and layer["value"] is not None:
                wetness_values.append(layer["value"])
            else:
                wetness_values.append(0.0)  # Default value for missing data
        if wetness_values:
            # Convert to numpy array
            wetness_values = np.array(wetness_values, dtype=np.float64)
            if n_duplications:
                assert len(wetness_values) == len(n_duplications), "Wetness values and duplications do not match, something went wrong when assigning layer splits"
                wetness_values = np.repeat(wetness_values, n_duplications)
            snowpack.set_param("0506", wetness_values, len(wetness_values))

    # stability index  

    
    snowpack._parsed = True
    
    # Calculate stability indices
    try:
        print("Calculating stability indices...")
        stability_indices = snowpack.calculate_stability_indices()
        snowpack.weak_layer = stability_indices
    except Exception as e:
        warnings.warn(f"Could not calculate stability indices: {str(e)}")
    
    return snowpack, metadata, profile_date

TYPES_TO_CODE: Dict[str, int] = {
    "PPgp": 0,
    "PP" : 1,
    "DF" : 2,
    "RG" : 3,
    "FC" : 4,
    "DH" : 5,
    "SH" : 6,
    "MF" : 7,
    "IF" : 8,
    "FCxr" : 9}