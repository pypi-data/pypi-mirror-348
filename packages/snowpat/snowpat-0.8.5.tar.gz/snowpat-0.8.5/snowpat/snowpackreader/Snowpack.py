import math
import pandas as pd
import numpy as np
import warnings
import datetime
from typing import Dict, Optional

special_codes = ["0514", "0530"]
plus_minus = "\u00B1"


class Snowpack:
    def __init__(self):
        """
        Initializes a Snowpack object. Used to handle snow profile data from Snowpack.

        Except for obtaining the original height in the .pro file it is advised to only use the getter methods to access the data.

        Attributes:
            layer_boundaries (np.ndarray): The height of the layer boundaries. (Height as written in the Snowpack output)

        Methods:
            get_param(code:str): Returns a parameter from the Snowpack object for the given data code.
            discard_below_ground(discard:bool): Sets whether to return data below ground level (default: True).
            toDf(integrate:bool): Converts the Snowpack object to a pandas DataFrame. With either integrated weak layer and surface hoar or as metadata accssible as: df.weak_layer; df.surface_hoar

        Args:
            None

        Returns:
            None
        """
        self.layer_boundaries: Optional[np.ndarray] = None
        self.data: Dict[str, np.ndarray] = {}
        self.surface_hoar: Optional[np.ndarray] = None
        self.weak_layer: Optional[np.ndarray] = None
        self.isNewton: Optional[bool] = None
        self.old_hardness: Optional[bool] = None

        # internal variables
        self._height_mask: Optional[np.ndarray] = None
        self._above_ground = False
        self.num_nodes = None
        self._parsed = False
        
    def set_param(self, code: str, values: np.ndarray, boundaries: int):
        if not self.num_nodes:
            self.num_nodes = boundaries
        if code == "0501":
            self.layer_boundaries = values
            self._height_mask = self.layer_boundaries >= 0
        elif code == "0514":
            self.surface_hoar = values
        elif code == "0530":
            self.weak_layer = values
        else:
            self.data[code] = values
        
    def get_param(self, code: str, return_missing: bool = False):
        """
        Retrieves the parameter associated with the given code.

        Args:
            code (str): The code of the parameter to retrieve.
            return_missing (bool): Will return a missing value (-999) instead of showing a warning when a variable is not present

        Returns:
            The parameter associated with the given code.

        Raises:
            KeyError: If the code is not found in the data.

        """
        # need to add these, because they were handled seperately and can also be called through different means
        possible_codes = list(self.data.keys()) + ["0501", "0530", "0514"]
        if not code in possible_codes:
            if return_missing:
                return np.full(len(self.data["layer middle"]),-999.0) # The Snowpack Missing Value
            print(f"{code} is invalid")
            print("available codes are:")
            print(f"{self.data.keys()}")
            return
            
        if code == "0501":
            if self._above_ground:
                mask = np.append(self._height_mask,True)
                return self.layer_boundaries[mask]
            else:
                return self.layer_boundaries

        if code == "0514":
            return self.surface_hoar
        if code == "0530":
            return self.weak_layer

        param = self.data[code]
        if self._above_ground:
            param = param[self._height_mask]
        return param

    def discard_below_ground(self, discard: bool):
        """
        Sets whether to return data below ground level.

        If set to true, only data above ground will be returned, by the getter methods.
        Otherwise all the data will be returned.

        Can be used subsequently.

        Args:
            discard (bool): If True, data below ground level will be discarded. If False, all data will be kept.

        Returns:
            None
        """
        self._above_ground = discard

    def _parse_data(self, old_hardness:bool):
        # snowpack sometimes does not explicitly put a boundary at 0, so we need to append that
        if self.layer_boundaries[0] > 0:
            self.num_nodes += 1
            self.layer_boundaries = np.insert(self.layer_boundaries, 0, 0)
            self._height_mask = np.insert(self._height_mask, 0, True)
        
        # nodes give the boundaries, but values are valid for the whole layer
        n_layers = self.num_nodes -1
        for key, val in self.data.items():
            # grain types has surface hoar as 0, and is specified with a dfferent code
            if key == "0513" and len(val) == n_layers + 1: 
                self.data[key] = np.delete(val, -1)
            # fill missing layers with nans
            if self.data[key].size != n_layers:
                try:
                    self.data[key] = np.insert(
                        self.data[key], 0, [np.nan for _ in range(n_layers - self.data[key].size)]
                    )
                except:
                    print(n_layers)
                    print(self.data[key].size)
                    print(f"{key} has {self.data[key].size} values, but {n_layers} layers")


        # make new fields, so it is clearer, where the layers actually are
        layer_middle = [
            (self.layer_boundaries[i + 1] + self.layer_boundaries[i]) / 2
            for i in range(self.layer_boundaries.size - 1)
        ]
        layer_thicknes = [
            (self.layer_boundaries[i + 1] - self.layer_boundaries[i]) / 2
            for i in range(self.layer_boundaries.size - 1)
        ]

        layer_middle = np.array(layer_middle)
        layer_thicknes = np.array(layer_thicknes)

        self.data["layer middle"] = layer_middle
        self.data["layer thickness"] = layer_thicknes
        if len(self._height_mask) > n_layers:
            self._height_mask = np.delete(self._height_mask, -1)
        
        
        # check how the hardness is specified
        if "0534" in self.data.keys():
            if old_hardness:    
                self.isNewton = all(self.data["0534"] > 0)
                self.old_hardness = True
            else:
                self.isNewton = any(self.data["0534"] > 6) 
                self.old_hardness = False
        else:
            self.old_hardness = True

    def toDf(self, CodesToName: Dict = None, integrate: bool = False):
        """
        Converts the Snowpack object to a pandas DataFrame.

        In the data frame the heights given in the Snowpack output, which essentially are the layer boundaries,
        are converted to the middle of the layers and the thickness of the layers, for a clean data frame.
        The original layer boundaries can easily be computed from that.

        The minimum stability indices (weak_layer) and surface hoar information are available as:
        df.weak_layer and df.surface_hoar. However, this information will not be passed on when merging... the dataframe
        as pandas does not handle this yet.

        Args:
            CodesToName (Dict, optional): A dictionary mapping column data codes to column names.

        Returns:
            DataFrame: The Snowpack data as a pandas DataFrame.
        """
        df = pd.DataFrame(self.data)
        cols = (
            ["layer middle"]
            + ["layer thickness"]
            + [
                col
                for col in df.columns
                if col != "layer middle" and col != "layer thickness"
            ]
        )
        df = df[cols]
        if self._above_ground:
            df = df[self._height_mask]

        if CodesToName:
            df.rename(columns=CodesToName, inplace=True)
        if integrate:
            df.weak_layer = None
            df.surface_hoar = None
            if self.surface_hoar is not None:
                df["surface hoar"] = [
                    np.nan for _ in range(df["layer middle"].size - 1)
                ] + [self.surface_hoar]
            if self.weak_layer is not None:
                df["weak layer"] = [self.weak_layer] + [
                    np.nan for _ in range(df["layer middle"].size - 1)
                ]
        else:
            warnings.filterwarnings('ignore', 'Pandas doesn\'t allow columns to be created via a new attribute name')
            df.weak_layer = self.weak_layer
            df.surface_hoar = self.surface_hoar
        return df

    def write_pro_file(self, filepath: str, station_params: dict = None, profile_date: datetime = None):
        """
        Writes the Snowpack data to a .pro file.

        Args:
            filepath (str): Path to save the .pro file
            station_params (dict, optional): Dictionary containing station parameters.
                Keys should be: StationName, Latitude, Longitude, Altitude, SlopeAngle, SlopeAzi
                If not provided, default values will be used.

        Returns:
            None
        """
        if not self._parsed:
            raise ValueError("Snowpack data has not been parsed yet.")

        # Default station parameters if not provided
        default_params = {
            "StationName": "Unknown",
            "Latitude": 0.0,
            "Longitude": 0.0,
            "Altitude": 0.0,
            "SlopeAngle": 0,
            "SlopeAzi": 0
        }
        station_params = station_params or default_params

        with open(filepath, 'w') as f:
            # Write station parameters
            f.write("[STATION_PARAMETERS]\n")
            for key, value in station_params.items():
                if key == "SlopeAzi" and value == None:
                    value = 0
                f.write(f"{key}= {value}\n")
            f.write("\n")

            # Write header section
            f.write("[HEADER]\n")
            f.write("0500,Date\n")
            f.write("0501,nElems,height [> 0: top, < 0: bottom of elem.] (cm)\n")
            f.write("0502,nElems,element density (kg m-3)\n")
            f.write("0503,nElems,element temperature (degC)\n")
            f.write("0504,nElems,element ID (1)\n")
            f.write("0506,nElems,liquid water content by volume (%)\n")
            f.write("0508,nElems,dendricity (1)\n")
            f.write("0509,nElems,sphericity (1)\n")
            f.write("0510,nElems,coordination number (1)\n")
            f.write("0511,nElems,bond size (mm)\n")
            f.write("0512,nElems,grain size (mm)\n")
            f.write("0513,nElems,grain type (Swiss Code F1F2F3)\n")
            f.write("0514,3,grain type, grain size (mm), and density (kg m-3) of SH at surface\n")
            f.write("0515,nElems,ice volume fraction (%)\n")
            f.write("0516,nElems,air volume fraction (%)\n")
            f.write("0517,nElems,stress in (kPa)\n")
            f.write("0518,nElems,viscosity (GPa s)\n")
            f.write("0519,nElems,soil volume fraction (%)\n")
            f.write("0520,nElems,temperature gradient (K m-1)\n")
            f.write("0521,nElems,thermal conductivity (W K-1 m-1)\n")
            f.write("0522,nElems,absorbed shortwave radiation (W m-2)\n")
            f.write("0523,nElems,viscous deformation rate (1.e-6 s-1)\n")
            f.write("0530,8,position (cm) and minimum stability indices:\n")
            f.write("profile type, stability class, z_Sdef, Sdef, z_Sn38, Sn38, z_Sk38, Sk38\n")
            f.write("0531,nElems,deformation rate stability index Sdef\n")
            f.write("0532,nElems,natural stability index Sn38\n")
            f.write("0533,nElems,stability index Sk38\n")
            f.write("0534,nElems,hand hardness either (N) or index steps (1)\n")
            f.write("0535,nElems,optical equivalent grain size (mm)\n")
            f.write("0601,nElems,snow shear strength (kPa)\n")
            f.write("0602,nElems,grain size difference (mm)\n")
            f.write("0603,nElems,hardness difference (1)\n")
            f.write("0604,nElems,ssi\n")
            f.write("0605,nElems,inverse texture index ITI (Mg m-4)\n")
            f.write("0606,nElems,critical cut length (m)\n")
            f.write("\n")

            # Write data section
            f.write("[DATA]\n")
            
            # Write date
            current_date = profile_date.strftime("%d.%m.%Y %H:%M:%S")
            f.write(f"0500,{current_date}\n")

            # Write layer boundaries
            boundaries = self.get_param("0501")
            f.write(f"0501,{len(boundaries)},{','.join(map(str, boundaries))}\n")

            # Write all other parameters
            param_codes = [code for code in self.data.keys() if code not in ["layer middle", "layer thickness"]]
            for code in sorted(param_codes):
                values = self.get_param(code)
                if values is not None:
                    if code == "0534" and not self.isNewton: # snowpack only gives 0.5 and hand hardness is negative
                        for (i,value) in enumerate(values):
                            if math.isclose(value%1, 1/3) or math.isclose(value%1, 2/3):
                                value = math.floor(value) + 0.5
                            values[i] = -1 * value
                    if code == "0513":
                        values = np.append(values, -999) # for some reason we need surface here
                        if np.any(values <100) and np.any(values >0):
                            out_vals = [f"{val}" if val > 100 or val < 0 else f"000" for val in values]
                            values = out_vals
                    f.write(f"{code},{len(values)},{','.join(map(str, values))}\n")

            # Write special codes (surface hoar and weak layer)
            if self.surface_hoar is not None:
                f.write(f"0514,3,{','.join(map(str, self.surface_hoar))}\n")
            if self.weak_layer is not None:
                f.write(f"0530,8,{','.join(map(str, self.weak_layer))}\n")

    def calculate_stability_indices(self) -> np.ndarray:
        """
        Calculate stability indices (SSI, Sk38, Sn38) for the snowpack.
        Returns array with format: [profile_type, stability_class, z_Sdef, Sdef, z_Sn38, Sn38, z_Sk38, Sk38]
        
        Based on:
        - Schweizer et al. (2006) - A threshold sum approach to stability evaluation of manual profiles
        - Monti et al. (2016) - Snow instability evaluation: calculating the skier-induced stress in a multi-layered snowpack
        - Schweizer and Jamieson (2003) - Snowpack properties for snow profile analysis
        """
        if not self._parsed:
            raise ValueError("Data must be parsed before calculating stability indices")
            
        # Get required layer properties
        heights = self.get_param("layer middle")  # cm
        thicknesses = self.get_param("layer thickness")  # cm
        densities = self.get_param("0502")  # kg/m³
        temps = self.get_param("0503")  # °C
        grain_types = self.get_param("0513")  # Code
        grain_sizes = self.get_param("0512")  # mm
        hardness = self.get_param("0534")  # N if isNewton else hand hardness index
        
        g = 9.81  # m/s²
        skier_load = 1500  # N - represents typical skier load
        
        # Initialize arrays
        n_layers = len(heights)
        # use primary grain type codes (0-9) from swiss F1F2F3 codes
        primary_gt = np.zeros(n_layers, dtype=np.int16)
        for (i,gt) in enumerate(grain_types):
            if gt == -999:
                primary_gt[i] = -999
            elif gt <100 and gt >0:
                primary_gt[i] = 0
            else:
                primary_gt[i] = int(gt // 100)
                
        stress = np.zeros(n_layers)
        strength = np.zeros(n_layers)
        Sn38 = np.zeros(n_layers)
        Sk38 = np.zeros(n_layers)
        # placeholder for SSI between layers
        ssi = np.zeros(n_layers - 1)
        
        # Calculate penetration depth Pk (m) - C++ compPenetrationDepth
        depth_m = np.sum(thicknesses) / 100.0
        rho_Pk_num = 0.0
        dz_Pk = 0.0
        cum_depth = 0.0
        for j in range(n_layers-1, -1, -1):
            if cum_depth >= 30.0: break
            Lm = thicknesses[j] / 100.0
            rho_Pk_num += densities[j] * Lm
            dz_Pk += Lm
            cum_depth += thicknesses[j]
        if dz_Pk > 0.0:
            rho_Pk = rho_Pk_num / dz_Pk
            Pk = min(0.8 * 43.3 / rho_Pk, depth_m)
        else:
            Pk = 0.0

        # Precompute reference slope angle parameters (psi_ref = 38°)
        psi_ref = 38.0
        cos_psi = math.cos(math.radians(psi_ref))
        sin_psi = math.sin(math.radians(psi_ref))
        ski_load = 85.0 * g / 1.7

        # Calculate stress, strength, Sn38 and Sk38 using reduced stresses
        for i in range(n_layers):
            # overburden stress (Pa)
            if densities[i] > 0:
                stress[i] = np.sum(densities[:i+1] * thicknesses[:i+1]) * g / 100.0
            # layer strength (shear strength Sig_c2)
            if self.isNewton:
                strength[i] = hardness[i]
            else:
                strength[i] = 2.91 * np.exp(2.91 * hardness[i])
            if temps[i] is not None:
                tf = max(0.5, 1.0 - 0.01 * abs(temps[i]))
                strength[i] *= tf
            if primary_gt[i] in [5, 6]:
                strength[i] *= 0.7
            # reduced stresses
            sig_n = -stress[i] / 1000.0
            sig_s = sig_n * sin_psi / cos_psi
            # natural stability index (getNaturalStability)
            if sig_s > 0.0:
                Sn38[i] = max(0.05, min(6.0, strength[i] / sig_s))
            else:
                Sn38[i] = 6.0
            # skier stability index (getLayerSkierStability)
            depth_lay = np.sum(thicknesses[:i+1]) / 100.0
            layer_depth = depth_lay - Pk
            if layer_depth > 1e-6:
                delta_sig = 2.0 * ski_load * math.cos(math.radians(psi_ref)) * (math.sin(math.radians(psi_ref))**2) * math.sin(math.radians(2*psi_ref))
                delta_sig /= math.pi * layer_depth * cos_psi
                delta_sig /= 1000.0
                Sk38[i] = max(0.05, min(6.0, strength[i] / (sig_s + delta_sig)))
            else:
                Sk38[i] = 6.0

        # Compute SSI and record lemon counts per interface (C++ initStructuralStabilityIndex)
        max_stab = 6.0
        nmax_lemon = 2
        lemons_arr = np.zeros(n_layers - 1, dtype=int)
        for i in range(n_layers - 1):
            lemons = 0
            if abs(hardness[i] - hardness[i+1]) > 1.5:
                lemons += 1
            if grain_sizes is not None and 2 * abs(grain_sizes[i] - grain_sizes[i+1]) > 0.5:
                lemons += 1
            lemons_arr[i] = lemons
            val = nmax_lemon - lemons + Sk38[i+1]
            ssi[i] = max(0.05, min(max_stab, val))
        
        # Determine weak-layer location and values
        min_Sn38_idx = np.argmin(Sn38)
        min_Sk38_idx = np.argmin(Sk38)
        min_ssi_idx = np.argmin(ssi)
        Swl_ssi = ssi[min_ssi_idx]
        Swl_lemon = int(lemons_arr[min_ssi_idx])
        Swl_Sk38 = Sk38[min_ssi_idx+1]
        # Profile type: apply surface hoar flag, fallback on error
        if not (Swl_ssi > 0 and Swl_ssi < 100):
            profile_type = -1
        else:
            profile_type = 2 if np.any(primary_gt == 6) else 1
        # Stability class via SchweizerBellaire2
        if Swl_ssi > 0 and Swl_ssi < 100:
            if Swl_lemon >= 2:
                stability_class = 1
            elif Swl_lemon == 1:
                if Swl_Sk38 < 0.48:
                    stability_class = 1
                elif Swl_Sk38 < 0.71:
                    stability_class = 3
                else:
                    stability_class = 5
            else:
                stability_class = 3
        else:
            stability_class = -1
        # Format output according to 0530 code spec
        result = np.array([
            profile_type,
            stability_class,
            heights[min_ssi_idx],   # z_Sdef
            ssi[min_ssi_idx],       # Sdef (SSI)
            heights[min_Sn38_idx],  # z_Sn38
            Sn38[min_Sn38_idx],     # Sn38
            heights[min_Sk38_idx],  # z_Sk38
            Sk38[min_Sk38_idx]      # Sk38
        ])
        
        # Store result in weak_layer property
        self.weak_layer = result
        self.set_param("0530", result, len(result))
        self.set_param("0604", ssi, len(ssi))
        
        return result
