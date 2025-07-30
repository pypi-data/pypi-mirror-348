import scipy.io
import numpy as np
import h5py
from scipy.signal import hilbert
from math import ceil, floor
import os
from kwave.kgrid import kWaveGrid
from kwave.kmedium import kWaveMedium
from kwave.ksource import kSource
from kwave.ksensor import kSensor
from kwave.kspaceFirstOrder3D import kspaceFirstOrder3D
from kwave.kspaceFirstOrder2D import kspaceFirstOrder2D
from kwave.utils.signals import tone_burst
from kwave.options.simulation_options import SimulationOptions
from kwave.options.simulation_execution_options import SimulationExecutionOptions
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from tempfile import gettempdir
from .config import config
import AOT_biomaps.Settings
from concurrent.futures import ThreadPoolExecutor

if config.get_process()  == 'gpu':
    import cupy as cp
    from cupyx.scipy.signal import hilbert as cp_hilbert
else:
    import numpy as np
    from scipy.signal import hilbert as cp_hilbert

from abc import ABC, abstractmethod
from enum import Enum

class TypeSim(Enum):
    """
    Enum for the type of simulation to be performed.

    Selection of simulation types:
    - KWAVE: k-Wave simulation.
    - FIELD2: Field II simulation.
    - HYDRO: Hydrophone acquisition.
    """
    KWAVE = 'k-wave'
    """k-Wave simulation."""

    FIELD2 = 'Field2'
    """Field II simulation."""

    HYDRO = 'Hydrophone'
    """Hydrophone acquisition."""

class Dim(Enum):
    """
    Enum for the dimension of the acoustic field.

    Selection of dimensions:
    - D2: 2D field.
    - D3: 3D field.
    """
    D2 = '2D'
    """2D field."""
    D3 = '3D'
    """3D field."""

class FormatSave(Enum):
    """
    Enum for different file formats to save the acoustic field.

    Selection of file formats:
    - HDR_IMG: Interfile format (.hdr and .img).
    - H5: HDF5 format (.h5).
    - NPY: NumPy format (.npy).
    """
    HDR_IMG = '.hdr'
    """Interfile format (.hdr and .img)."""
    H5 = '.h5'
    """HDF5 format (.h5)."""
    NPY = '.npy'
    """NumPy format (.npy)."""

class WaveType(Enum):
    """
    Enum for different types of acoustic waves.

    Selection of wave types:
    - FocusedWave: A wave type where the energy is focused at a specific point.
    - StructuredWave: A wave type characterized by a specific pattern or structure.
    - PlaneWave: A wave type where the wavefronts are parallel and travel in a single direction.
    """
    FocusedWave = 'focus'
    """A wave type where the energy is focused at a specific point."""
    StructuredWave = 'structured'
    """A wave type characterized by a specific pattern or structure."""
    PlaneWave = 'plane'
    """A wave type where the wavefronts are parallel and travel in a single direction."""

####### ABSTRACT CLASS #######

class AcousticField(ABC):
    """
    Abstract class to generate and manipulate acoustic fields for ultrasound imaging.
    Provides methods to initialize parameters, generate fields, save and load data, and calculate envelopes.

    Principal parameters:
    - field: Acoustic field data.
    - enveloppe: Analytic envelope squared of the acoustic field.
    - burst: Burst signal used for generating the field for each piezo elements.
    - delayedSignal: Delayed burst signal for each piezo element.
    - medium: Medium properties for k-Wave simulation. Because field2 and Hydrophone simulation are not implemented yet, this attribute is set to None for these types of simulation.
    """

    def __init__(self, params):
        """
        Initialize global properties of the AcousticField object.

        Parameters:
        - typeSim (TypeSim): Type of simulation to be performed. Options include KWAVE, FIELD2, and HYDRO. Default is TypeSim.KWAVE.
        - dim (Dim): Dimension of the acoustic field. Can be 2D or 3D. Default is Dim.D2.
        - c0 (float): Speed of sound in the medium, specified in meters per second (m/s). Default is 1540 m/s.
        - f_US (float): Frequency of the ultrasound signal, specified in Hertz (Hz). Default is 6 MHz.
        - f_AQ (float): Frequency of data acquisition, specified in Hertz (Hz). Default is 180 MHz.
        - f_saving (float): Frequency at which the acoustic field data is saved, specified in Hertz (Hz). Default is 10 MHz.
        - num_cycles (int): Number of cycles in the burst signal. Default is 4 cycles.
        - num_elements (int): Number of elements in the transducer array. Default is 192 elements.
        - element_width (float): Width of each transducer element, specified in meters (m). Default is 0.2 mm.
        - element_height (float): Height of each transducer element, specified in meters (m). Default is 6 mm.
        - Xrange (list of float): Range of X coordinates for the acoustic field, specified in meters (m). Default is from -20 mm to 20 mm.
        - Yrange (list of float, optional): Range of Y coordinates for the acoustic field, specified in meters (m). Default is None, indicating no specific Y range.
        - Zrange (list of float): Range of Z coordinates for the acoustic field, specified in meters (m). Default is from 0 m to 37 mm.
        """
        required_keys = [
            'c0', 'f_US', 'f_AQ', 'f_saving', 'num_cycles', 'num_elements',
            'element_width', 'element_height', 'Xrange', 'Zrange', 'dim',
            'typeSim', 'dx', 'dz'
        ]

        # Verify required keys
        try:
            if params != None:
                for key in required_keys:
                    if key not in params.acoustic and key not in params.general:
                        raise ValueError(f"{key} must be provided in the parameters.")
        except ValueError as e:
            print(f"Initialization error: {e}")
            raise
        if params != None:
            if type(params) != AOT_biomaps.Settings.Params:
                raise TypeError("params must be an instance of the Params class")
            
            self.params = {
                'c0': params.acoustic['c0'],
                'f_US': int(float(params.acoustic['f_US'])),
                'f_AQ': int(float(params.acoustic['f_AQ'])),
                'f_saving': int(float(params.acoustic['f_saving'])),
                'num_cycles': params.acoustic['num_cycles'],
                'num_elements': params.acoustic['num_elements'],
                'element_width': params.acoustic['element_width'],
                'element_height': params.acoustic['element_height'],
                'Xrange': params.general['Xrange'],
                'Yrange': params.general['Yrange'],
                'Zrange': params.general['Zrange'],
                'dim': params.acoustic['dim'],
                'typeSim': params.acoustic['typeSim'],
                'dx': params.general['dx'],
                'dy': params.general['dy'] if params.general['Yrange'] is not None else None,
                'dz': params.general['dz'],
                'Nx': int(np.round((params.general['Xrange'][1] - params.general['Xrange'][0])/params.general['dx'])),
                'Ny': int(np.round((params.general['Yrange'][1] - params.general['Yrange'][0])/params.general['dy']))  if params.general['Yrange'] is not None else 1,
                'Nz': int(np.round((params.general['Zrange'][1] - params.general['Zrange'][0])/params.general['dz'])),
                'probeWidth': params.acoustic['num_elements'] * params.acoustic['element_width'],
                'IsAbsorbingMedium': params.acoustic['isAbsorbingMedium'],
            }
            self.burst = self._generate_burst_signal()
            if self.params["dim"] == Dim.D3 and self.params["Yrange"] is None:
                raise ValueError("Yrange must be provided for 3D fields.")
            if self.params["typeSim"] == TypeSim.KWAVE.value:
                if self.params ['IsAbsorbingMedium'] == True:
                        self.medium = kWaveMedium(
                        sound_speed=self.params['c0'],
                        density=1000,    
                        alpha_coeff=0.0022,  # dB/(MHz·cm)
                        alpha_power=2,
                        absorbing=True
                    )
                else:
                    self.medium = kWaveMedium(sound_speed=self.params['c0'])
            elif self.params["typeSim"] == TypeSim.FIELD2.value:
                self.medium = None
        else:
            self.medium = None

        self.waveType = None
        self.field = None
        self.enveloppe = None    

    def __str__(self):
        """
        Returns a string representation of the AcousticField object, including its parameters and attributes.
        The string is formatted in a table-like structure for better readability.
        """
        try:
            # Get all attributes of the instance
            attrs = {**self.params, **{k: v for k, v in vars(self).items() if k not in self.params}}

            # Base attributes of AcousticField
            base_attrs_keys = ['c0', 'f_US', 'f_AQ', 'f_saving', 'num_cycles', 'num_elements',
                            'element_width', 'element_height',
                            'Xrange', 'Yrange', 'Zrange', 'dim', 'typeSim', 'Nx', 'Ny', 'Nz',
                            'dx', 'dy', 'dz', 'probeWidth']
            base_attrs = {key: value for key, value in attrs.items() if key in base_attrs_keys}

            # Attributes specific to the derived class, excluding 'params'
            derived_attrs = {key: value for key, value in attrs.items() if key not in base_attrs_keys and key != 'params'}

            # Create lines for base and derived attributes
            base_attr_lines = [f"  {key}: {value}" for key, value in base_attrs.items()]

            derived_attr_lines = []
            for key, value in derived_attrs.items():
                if key in {'burst', 'delayedSignal'}:
                    continue
                elif key == 'pattern':
                    # Inspect the pattern object
                    try:
                        pattern_attrs = vars(value)
                        pattern_str = ", ".join([f"{k}={v}" for k, v in pattern_attrs.items()])
                        derived_attr_lines.append(f"  pattern: {{{pattern_str}}}")
                    except Exception as e:
                        derived_attr_lines.append(f"  pattern: <unreadable: {e}>")
                else:
                    try:
                        derived_attr_lines.append(f"  {key}: {value}")
                    except Exception as e:
                        derived_attr_lines.append(f"  {key}: <unprintable: {e}>")

            # Add shapes for burst and delayedSignal
            if 'burst' in derived_attrs:
                derived_attr_lines.append(f"  burst: shape={self.burst.shape}")
            if 'delayedSignal' in derived_attrs:
                derived_attr_lines.append(f"  delayedSignal: shape={self.delayedSignal.shape}")

            # Define borders and titles
            border = "+" + "-" * 40 + "+"
            title = f"|Type : {self.__class__.__name__} wave |"
            base_title = "| AcousticField Attributes |"
            derived_title = f"| {self.__class__.__name__} Specific Attributes |" if derived_attrs else ""

            # Convert attributes to strings
            base_attr_str = "\n".join(base_attr_lines)
            derived_attr_str = "\n".join(derived_attr_lines)

            # Assemble the final result
            result = f"{border}\n{title}\n{border}\n{base_title}\n{border}\n{base_attr_str}\n"
            if derived_attrs:
                result += f"\n{border}\n{derived_title}\n{border}\n{derived_attr_str}\n"
            result += border

            return result
        except Exception as e:
            print(f"Error in __str__ method: {e}")
            raise


    def __del__(self):
        """
        Destructor for the AcousticField class. Cleans up the field and envelope attributes.
        """
        try:
            self.field = None
            self.enveloppe = None
            self.burst = None
            self.delayedSignal = None
            if config.get_process() == 'gpu':
                cp.cuda.Device(config.bestGPU).synchronize()
        except Exception as e:
            print(f"Error in __del__ method: {e}")
            raise

    ## TOOLS METHODS ##

    def generate_field(self, isGpu=config.get_process() == 'gpu'):
        """
        Generate the acoustic field based on the specified simulation type and parameters.
        """
        try:
            if self.params["typeSim"] == TypeSim.FIELD2.value:
                raise NotImplementedError("FIELD2 simulation is not implemented yet.")
            elif self.params["typeSim"] == TypeSim.KWAVE.value:
                if self.params["dim"] == Dim.D2.value:
                    self.field = self._generate_2Dacoustic_field_KWAVE(isGpu)
                elif self.params["dim"] == Dim.D3.value:
                    self.field = self._generate_3Dacoustic_field_KWAVE(isGpu)
            elif self.params["typeSim"] == TypeSim.HYDRO.value:
                raise ValueError("Cannot generate field for Hydrophone simulation, load exciting acquisitions.")
            else:
                raise ValueError("Invalid simulation type. Supported types are: FIELD2, KWAVE, HYDRO.")
        except Exception as e:
            print(f"Error in generate_field method: {e}")
            raise

    def calculate_envelope_squared(self, isGPU=True if config.get_process() == 'gpu' else False):
        """
        Calculate the analytic envelope of the acoustic field using either CPU or GPU.

        Parameters:
        - use_gpu (bool): If True, use GPU for computation. Otherwise, use CPU.

        Returns:
        - envelope (numpy.ndarray or cupy.ndarray): The squared analytic envelope of the acoustic field.
        """
        try:
            if self.field is None:
                raise ValueError("Acoustic field is not generated. Please generate the field first.")

            if isGPU:
                print("Using GPU for envelope calculation.")
                acoustic_field = cp.asarray(self.field)
            else:
                print("Using CPU for envelope calculation.")
                acoustic_field = np.asarray(self.field)

            if len(acoustic_field.shape) not in [3, 4]:
                raise ValueError("Input acoustic field must be a 3D or 4D array.")

            def process_slice(slice_index, isGPU):
                """Calculate the envelope for a given slice of the acoustic field."""

                if len(acoustic_field.shape) == 3:
                    return np.abs(cp_hilbert(acoustic_field[slice_index], axis=0))**2
                elif len(acoustic_field.shape) == 4:
                    envelope_slice = np.zeros_like(acoustic_field[slice_index])
                    for y in range(acoustic_field.shape[2]):
                        for z in range(acoustic_field.shape[1]):
                            envelope_slice[:, z, y, :] = np.abs(cp_hilbert(acoustic_field[slice_index][:, z, y, :], axis=0))**2
                    return envelope_slice

            # Determine the number of slices to process in parallel
            num_slices = acoustic_field.shape[0]
            slice_indices = [(i,) for i in range(num_slices)]

            if isGPU:
                # Use GPU directly without multithreading
                envelopes = [process_slice(slice_index, isGPU=True) for slice_index in slice_indices]
            else:
                # Use ThreadPoolExecutor to parallelize the computation on CPU
                with ThreadPoolExecutor() as executor:
                    envelopes = list(executor.map(lambda index: process_slice(index, isGPU=False), slice_indices))

            # Combine the results into a single array
            if isGPU:
                self.enveloppe = cp.stack(envelopes, axis=0).get()
            else:
                self.enveloppe = np.stack(envelopes, axis=0)

        except Exception as e:
            print(f"Error in calculate_envelope_squared method: {e}")
            raise

    def save_field(self, filePath, formatSave=FormatSave.HDR_IMG):
        """
        Save the acoustic field to a file in the specified format.

        Parameters:
        - filePath (str): The path where the file will be saved.
        """
        try:
            if formatSave.value == FormatSave.HDR_IMG.value:
                self._save2D_HDR_IMG(filePath)
            elif formatSave.value == FormatSave.H5.value:
                self._save2D_H5(filePath)
            elif formatSave.value == FormatSave.NPY.value:
                self._save2D_NPY(filePath)
            else:
                raise ValueError("Unsupported format. Supported formats are: HDR_IMG, H5, NPY.")
        except Exception as e:
            print(f"Error in save_field method: {e}")
            raise

    def load_field(self, filePath, formatSave=FormatSave.HDR_IMG):
        """
        Load the acoustic field from a file in the specified format.

        Parameters:
        - filePath (str): The path from which to load the file.
        """
        try:
            extension = os.path.splitext(filePath)[1]
            print(f"extension: {extension}")
            if extension != None:
                if extension == FormatSave.HDR_IMG.value:
                    formatSave = FormatSave.HDR_IMG
                elif extension == FormatSave.H5.value:
                    formatSave = FormatSave.H5
                elif extension == FormatSave.NPY.value:
                    formatSave = FormatSave.NPY
                elif extension == '':
                    pass
                else:
                    raise ValueError(f"Unsupported file format: {extension}. Supported formats are: HDR_IMG, H5, NPY.")
            if self.params["typeSim"] == TypeSim.FIELD2.value:
                raise NotImplementedError("FIELD2 simulation is not implemented yet.")
            elif self.params["typeSim"] == TypeSim.KWAVE.value:
                print("Loading KWAVE field...")
                if formatSave.value == FormatSave.HDR_IMG.value:
                    if self.params["dim"] == Dim.D2.value:
                        self._load_fieldKWAVE_XZ(os.path.join(filePath,self.getName_field()+formatSave.value))
                        self.calculate_envelope_squared()
                    elif self.params["dim"] == Dim.D3.value:
                        raise NotImplementedError("3D KWAVE field loading is not implemented yet.")
                elif formatSave.value == FormatSave.H5.value:
                    if self.params["dim"] == Dim.D2.value:
                        raise NotImplementedError("H5 KWAVE field loading is not implemented yet.")
                    elif self.params["dim"] == Dim.D3.value:
                        raise NotImplementedError("H5 KWAVE field loading is not implemented yet.")
                elif formatSave.value == FormatSave.NPY.value:
                    if self.params["dim"] == Dim.D2.value:
                        self.field = np.load(os.path.join(filePath,self.getName_field()+formatSave.value))
                    elif self.params["dim"] == Dim.D3.value:
                        raise NotImplementedError("3D NPY KWAVE field loading is not implemented yet.")
            elif self.params["typeSim"] == TypeSim.HYDRO.value:
                print("Loading Hydrophone field...")
                if formatSave.value == FormatSave.HDR_IMG.value:
                    raise ValueError("HDR_IMG format is not supported for Hydrophone acquisition.")
                if formatSave.value == FormatSave.H5.value:
                    if os.path.splitext(filePath)[1] != '.h5':
                            raise ValueError("The file must be in .h5 format.")
                    if self.params["dim"] == Dim.D2.value:
                        self.field, self.params['Xrange'], self.params['Zrange'] = self._load_fieldHYDRO_XZ(filePath,os.path.join(os.path.dirname(filePath), "PARAMS_" + os.path.basename(filePath.replace('.h5', '.mat'))))
                    elif self.params["dim"] == Dim.D3.value: 
                        self._load_fieldHYDRO_XYZ(filePath,  os.path.join(os.path.dirname(filePath), "PARAMS_" + os.path.basename(filePath.replace('.h5', '.mat'))))
                elif formatSave.value == FormatSave.NPY.value:
                    if self.params["dim"] == Dim.D2.value:
                        self.field = np.load(filePath)
                    elif self.params["dim"] == Dim.D3.value:
                        raise NotImplementedError("3D NPY Hydrophone field loading is not implemented yet.")
            else:
                raise ValueError("Invalid simulation type. Supported types are: FIELD2, KWAVE, HYDRO.")
           
        except Exception as e:
            print(f"Error in load_field method: {e}")
            raise

    def iSFieldInFolder(self, folderPath,formatSave=FormatSave.HDR_IMG):
        """
        Check if the field is already in the specified folder.

        Parameters:
        - filePath (str): The path to check.

        Returns:
        - bool: True if the field is in the folder, False otherwise.
        """
        try:
            if type(folderPath) != str:
                raise TypeError("folderPath must be a string")
            if not os.path.exists(folderPath):
                raise FileNotFoundError(f"The specified folder does not exist: {folderPath}")
            if type(formatSave) != FormatSave:
                raise TypeError("formatSave must be an instance of FormatSave Enum")
            if os.path.exists(os.path.join(folderPath, self.getName_field())+formatSave.value):
                return True
            else:
                return False
        except Exception as e:
            print(f"Error in iSFieldInFolder method: {e}")
            raise
    
    @abstractmethod
    def getName_field(self):
        pass

    ## DISPLAY METHODS ##

    def plot_burst_signal(self):
        """
        Plot the burst signal used for generating the acoustic field.
        """
        try:
            time2plot = np.arange(0, len(self.burst)) / self.params['f_AQ'] * 1000000  # Convert to microseconds
            plt.figure(figsize=(8, 8))
            plt.plot(time2plot, self.burst)
            plt.title('Excitation burst signal')
            plt.xlabel('Time (µs)')
            plt.ylabel('Amplitude')
            plt.grid()
            plt.show()
        except Exception as e:
            print(f"Error in plot_burst_signal method: {e}")
            raise

    def animated_plot_AcousticField(self, step=10, save_dir=None):
        """
        Plot synchronized animations of A_matrix slices for selected angles.

        Args:
            step (int): Time step between frames (default is every 10 frames).
            save_dir (str): Directory to save the animation gif; if None, animation will not be saved.

        Returns:
            ani: Matplotlib FuncAnimation object.
        """
        try:

            maxF = np.max(self.enveloppe[:,20:,:])
            minF = np.min(self.enveloppe[:,20:,:])
            # Set the maximum embedded animation size to 100 MB
            plt.rcParams['animation.embed_limit'] = 100

            if save_dir is not None:
                os.makedirs(save_dir, exist_ok=True)

            # Create a figure and axis
            fig, ax = plt.subplots()

            # Set main title
            if self.waveType.value == WaveType.FocusedWave.value:
                fig.suptitle("[System Matrix Animation] Focused Wave", fontsize=12, y=0.98)
            elif self.waveType.value == WaveType.PlaneWave.value:
                fig.suptitle(f"[System Matrix Animation] Plane Wave | Angles {self.params['angle']}°", fontsize=12, y=0.98)
            elif self.waveType.value == WaveType.StructuredWave.value:
                fig.suptitle(f"[System Matrix Animation] Structured Wave | Pattern structure: {self.pattern.activeList} | Angles {self.params['angle']}°", fontsize=12, y=0.98)
            else:

                raise ValueError("Invalid wave type. Supported types are: FocusedWave, PlaneWave, StructuredWave.")

            # Initial plot
            im = ax.imshow(
                self.enveloppe[0, :, :],
                extent=(self.params['Xrange'][0] * 1000, self.params['Xrange'][-1] * 1000, self.params['Zrange'][-1] * 1000, self.params['Zrange'][0] * 1000),
                vmin = 1.2*minF,
                vmax=0.8*maxF,
                aspect='equal',
                cmap='jet',
                animated=True
            )
            ax.set_title(f"t = 0 ms", fontsize=10)
            ax.set_xlabel("x (mm)", fontsize=8)
            ax.set_ylabel("z (mm)", fontsize=8)


            # Unified update function for all subplots
            def update(frame):
                im.set_data(self.enveloppe[frame, :, :])
                ax.set_title(f"t = {frame / self.params['f_AQ'] * 1000:.2f} ms", fontsize=10)
                return [im]  # Return a list of artists that were modified

            # Create animation
            ani = animation.FuncAnimation(
                fig, update,
                frames=range(0, self.enveloppe.shape[0], step),
                interval=50, blit=True
            )

            # Save animation if needed
            if save_dir is not None:
                if self.waveType == WaveType.FocusedWave:
                    save_filename = f"Focused_Wave_.gif"
                elif self.waveType == WaveType.PlaneWave:
                    save_filename = f"Plane_Wave_{self._format_angle()}.gif"
                else:
                    save_filename = f"Structured_Wave_PatternStructure_{self.pattern.activeList}_{self._format_angle()}.gif"
                save_path = os.path.join(save_dir, save_filename)
                ani.save(save_path, writer='pillow', fps=20)
                print(f"Saved: {save_path}")

            plt.close(fig)

            return ani
        except Exception as e:
            print(f"Error creating animation: {e}")
            return None


    ## PRIVATE METHODS ##

    def _generate_burst_signal(self):
        """
        Private method to generate a burst signal based on the specified parameters.
        """
        try:
            return tone_burst(self.params["f_AQ"], self.params["f_US"], self.params["num_cycles"]).squeeze()
        except Exception as e:
            print(f"Error in __generate_burst_signal method: {e}")
            raise

    @abstractmethod
    def _generate_2Dacoustic_field_KWAVE(self, isGpu):
        """
        Generate a 2D acoustic field using k-Wave simulation.
        Must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def _generate_3Dacoustic_field_KWAVE(self, isGpu):
        """
        Generate a 3D acoustic field using k-Wave simulation.
        Must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def _save2D_HDR_IMG(self, filePath):
        """
        Save the 2D acoustic field as an HDR_IMG file.
        Must be implemented in subclasses.
        """
        pass

    def _save2D_H5(self, filePath):
        """
        Save the 2D acoustic field as an H5 file.

        Parameters:
        - filePath (str): The path where the file will be saved.
        """
        try:
            with h5py.File(filePath+self.getName_field()+"h5", 'w') as f:
                for key, value in self.__dict__.items():
                    if key != 'enveloppe':
                        f.create_dataset(key, data=value)
                f.create_dataset('data', data=self.enveloppe, compression='gzip')
        except Exception as e:
            print(f"Error in _save2D_H5 method: {e}")
            raise

    def _save2D_NPY(self, filePath):
        """
        Save the 2D acoustic field as a NPY file.

        Parameters:
        - filePath (str): The path where the file will be saved.
        """
        try:
            np.save(filePath+self.getName_field()+"npy", self.enveloppe)
        except Exception as e:
            print(f"Error in _save2D_NPY method: {e}")
            raise

    def _load_fieldKWAVE_XZ(self, hdr_path):
        """
        Read an Interfile (.hdr) and its binary file (.img) to reconstruct an acoustic field.

        Parameters:
        - hdr_path (str): The path to the .hdr file.

        Returns:
        - field (numpy.ndarray): The reconstructed acoustic field with dimensions reordered to (X, Z, time).
        - header (dict): A dictionary containing the metadata from the .hdr file.
        """
        try:
            header = {}
            # Read the .hdr file
            with open(hdr_path, 'r') as f:
                for line in f:
                    if ':=' in line:
                        key, value = line.split(':=', 1)
                        key = key.strip().lower().replace('!', '')
                        value = value.strip()
                        header[key] = value

            # Get the associated .img file name
            data_file = header.get('name of data file') or header.get('name of date file')
            if data_file is None:
                raise ValueError(f"Cannot find the data file associated with the header file {hdr_path}")
            img_path = os.path.join(os.path.dirname(hdr_path), os.path.basename(data_file))

            # Determine the field size from metadata
            shape = [int(header[f'matrix size [{i}]']) for i in range(1, 3) if f'matrix size [{i}]' in header]
            if not shape:
                raise ValueError("Cannot determine the shape of the acoustic field from metadata.")

            # Data type
            data_type = header.get('number format', 'short float').lower()
            dtype_map = {
                'short float': np.float32,
                'float': np.float32,
                'int16': np.int16,
                'int32': np.int32,
                'uint16': np.uint16,
                'uint8': np.uint8
            }
            dtype = dtype_map.get(data_type)
            if dtype is None:
                raise ValueError(f"Unsupported data type: {data_type}")

            # Byte order (endianness)
            byte_order = header.get('imagedata byte order', 'LITTLEENDIAN').lower()
            endianess = '<' if 'little' in byte_order else '>'

            # Verify the actual size of the .img file
            fileSize = os.path.getsize(img_path)
            timeDim = int(fileSize / (np.dtype(dtype).itemsize * np.prod(shape)))
            shape = shape + [timeDim]

            # Read binary data
            with open(img_path, 'rb') as f:
                data = np.fromfile(f, dtype=endianess + np.dtype(dtype).char)

            # Reshape data to (time, Z, X)
            field = data.reshape(shape[::-1])  # NumPy interprets in C order (opposite of MATLAB)

            # Apply scaling factors if available
            rescale_slope = float(header.get('data rescale slope', 1))
            rescale_offset = float(header.get('data rescale offset', 0))
            field = field * rescale_slope + rescale_offset

            self.field = field
        except Exception as e:
            print(f"Error in _load_fieldKWAVE_XZ method: {e}")
            raise

    def _load_fieldHYDRO_XZ(self, file_path_h5, param_path_mat):
        """
        Load the 2D acoustic field for Hydrophone simulation from H5 and MAT files.

        Parameters:
        - file_path_h5 (str): The path to the H5 file.
        - param_path_mat (str): The path to the MAT file.

        Returns:
        - envelope_transposed (numpy.ndarray): The transposed envelope of the acoustic field.
        """
        try:
            # Load parameters from the .mat file
            param = scipy.io.loadmat(param_path_mat)

            # Load the ranges for x and z
            x_test = param['x'].flatten()
            z_test = param['z'].flatten()

            x_range = np.arange(-23, 21.2, 0.2)
            z_range = np.arange(0, 37.2, 0.2)
            X, Z = np.meshgrid(x_range, z_range)

            # Load the data from the .h5 file
            with h5py.File(file_path_h5, 'r') as file:
                data = file['data'][:]

            # Initialize a matrix to store the acoustic data
            acoustic_field = np.zeros((len(z_range), len(x_range), data.shape[1]))

            # Fill the grid with acoustic data
            index = 0
            for i in range(len(z_range)):
                if i % 2 == 0:
                    # Traverse left to right
                    for j in range(len(x_range)):
                        acoustic_field[i, j, :] = data[index]
                        index += 1
                else:
                    # Traverse right to left
                    for j in range(len(x_range) - 1, -1, -1):
                        acoustic_field[i, j, :] = data[index]
                        index += 1

            self.field =np.transpose(acoustic_field, (2, 0, 1)).T
            # Calculate the analytic envelope
            envelope = np.abs(hilbert(acoustic_field, axis=2))
            # Reorganize the array to have the shape (Times, Z, X)
            envelope_transposed = np.transpose(envelope, (2, 0, 1)).T

            self.enveloppe = envelope_transposed
            self.params['Xrange'] = x_range
            self.params['Zrange'] = z_range

        except Exception as e:
            print(f"Error in _load_fieldHYDRO_XZ method: {e}")
            raise

    def _load_fieldHYDRO_YZ(self, file_path_h5, param_path_mat):
        """
        Load the 2D acoustic field for Hydrophone simulation from H5 and MAT files.

        Parameters:
        - file_path_h5 (str): The path to the H5 file.
        - param_path_mat (str): The path to the MAT file.

        Returns:
        - envelope_transposed (numpy.ndarray): The transposed envelope of the acoustic field.
        - y_range (numpy.ndarray): The range of y values.
        - z_range (numpy.ndarray): The range of z values.
        """
        try:
            # Load parameters from the .mat file
            param = scipy.io.loadmat(param_path_mat)

            # Extract the ranges for y and z
            y_range = param['y'].flatten()
            z_range = param['z'].flatten()

            # Load the data from the .h5 file
            with h5py.File(file_path_h5, 'r') as file:
                data = file['data'][:]

            # Calculate the number of scans
            Ny = len(y_range)
            Nz = len(z_range)
            Nscans = Ny * Nz

            # Create the scan positions
            positions_y = []
            positions_z = []

            for i in range(Nz):
                if i % 2 == 0:
                    # Traverse top to bottom for even rows
                    positions_y.extend(y_range)
                else:
                    # Traverse bottom to top for odd rows
                    positions_y.extend(y_range[::-1])
                positions_z.extend([z_range[i]] * Ny)

            Positions = np.column_stack((positions_y, positions_z))

            # Initialize a matrix to store the reorganized data
            reorganized_data = np.zeros((Ny, Nz, data.shape[1]))

            # Reorganize the data according to the scan positions
            for index, (j, k) in enumerate(Positions):
                y_idx = np.where(y_range == j)[0][0]
                z_idx = np.where(z_range == k)[0][0]
                reorganized_data[y_idx, z_idx, :] = data[index, :]

            # Calculate the analytic envelope
            envelope = np.abs(hilbert(reorganized_data, axis=2))
            # Reorganize the array to have the shape (Times, Z, Y)
            envelope_transposed = np.transpose(envelope, (2, 0, 1))
            return envelope_transposed, y_range, z_range
        except Exception as e:
            print(f"Error in _load_fieldHYDRO_YZ method: {e}")
            raise

    def _load_fieldHYDRO_XYZ(self, file_path_h5, param_path_mat):
        """
        Load the 3D acoustic field for Hydrophone simulation from H5 and MAT files.

        Parameters:
        - file_path_h5 (str): The path to the H5 file.
        - param_path_mat (str): The path to the MAT file.

        Returns:
        - EnveloppeField (numpy.ndarray): The envelope of the acoustic field.
        - x_range (numpy.ndarray): The range of x values.
        - y_range (numpy.ndarray): The range of y values.
        - z_range (numpy.ndarray): The range of z values.
        """
        try:
            # Load parameters from the .mat file
            param = scipy.io.loadmat(param_path_mat)

            # Extract the ranges for x, y, and z
            x_range = param['x'].flatten()
            y_range = param['y'].flatten()
            z_range = param['z'].flatten()

            # Create a meshgrid for x, y, and z
            X, Y, Z = np.meshgrid(x_range, y_range, z_range, indexing='ij')

            # Load the data from the .h5 file
            with h5py.File(file_path_h5, 'r') as file:
                data = file['data'][:]

            # Calculate the number of scans
            Nx = len(x_range)
            Ny = len(y_range)
            Nz = len(z_range)
            Nscans = Nx * Ny * Nz

            # Create the scan positions
            if Ny % 2 == 0:
                X = np.tile(np.concatenate([x_range[:, np.newaxis], x_range[::-1, np.newaxis]]), (Ny // 2, 1))
                Y = np.repeat(y_range, Nx)
            else:
                X = np.concatenate([x_range[:, np.newaxis], np.tile(np.concatenate([x_range[::-1, np.newaxis], x_range[:, np.newaxis]]), ((Ny - 1) // 2, 1))])
                Y = np.repeat(y_range, Nx)

            XY = np.column_stack((X.flatten(), Y))

            if Nz % 2 == 0:
                XYZ = np.tile(np.concatenate([XY, np.flipud(XY)]), (Nz // 2, 1))
                Z = np.repeat(z_range, Nx * Ny)
            else:
                XYZ = np.concatenate([XY, np.tile(np.concatenate([np.flipud(XY), XY]), ((Nz - 1) // 2, 1))])
                Z = np.repeat(z_range, Nx * Ny)

            Positions = np.column_stack((XYZ, Z))

            # Initialize a matrix to store the reorganized data
            reorganized_data = np.zeros((Nx, Ny, Nz, data.shape[1]))

            # Reorganize the data according to the scan positions
            for index, (i, j, k) in enumerate(Positions):
                x_idx = np.where(x_range == i)[0][0]
                y_idx = np.where(y_range == j)[0][0]
                z_idx = np.where(z_range == k)[0][0]
                reorganized_data[x_idx, y_idx, z_idx, :] = data[index, :]

            self.field = np.transpose(reorganized_data, (3, 2, 1, 0))
            print("Field shape:", self.field.shape)
            print('reorganized_data shape:', reorganized_data.shape)
            EnveloppeField = np.zeros_like(reorganized_data)

            for y in range(reorganized_data.shape[1]):
                for z in range(reorganized_data.shape[2]):
                    EnveloppeField[:, y, z, :] = np.abs(hilbert(reorganized_data[:, y, z, :], axis=1))
            self.enveloppe = np.transpose(EnveloppeField,  (3, 2, 1, 0))
            self.params['Xrange'] = [x_range[0], x_range[-1]]
            self.params['Yrange'] = [y_range[0], y_range[-1]]
            self.params['Zrange'] = [z_range[0], z_range[-1]]
            self.params['Nx'] = Nx
            self.params['Ny'] = Ny
            self.params['Nz'] = Nz
        except Exception as e:
            print(f"Error in _load_fieldHYDRO_XYZ method: {e}")
            raise

####### SUBCLASS #######

class StructuredWave(AcousticField):

    class PatternParams:
        def __init__(self, space_0, space_1, move_head_0_2tail, move_tail_1_2head):
            """
            Initialize the PatternParams object with given parameters.

            Args:
                space_0 (int): Number of zeros in the pattern.
                space_1 (int): Number of ones in the pattern.
                move_head_0_2tail (int): Number of zeros to move from head to tail.
                move_tail_1_2head (int): Number of ones to move from tail to head.
            """
            self.space_0 = space_0
            self.space_1 = space_1
            self.move_head_0_2tail = move_head_0_2tail
            self.move_tail_1_2head = move_tail_1_2head
            self.activeList = None
            self.len_hex = None

        def __str__(self):
            """Return a string representation of the PatternParams object."""
            pass

        def generate_pattern(self):
            """
            Generate a binary pattern and return it as a hex string.

            Returns:
                str: Hexadecimal representation of the binary pattern.
            """
            try:
                total_bits = self.len_hex * 4
                unit = "0" * self.space_0 + "1" * self.space_1
                repeat_time = (total_bits + len(unit) - 1) // len(unit)
                pattern = (unit * repeat_time)[:total_bits]

                # Move 0s from head to tail
                if self.move_head_0_2tail > 0:
                    head_zeros = '0' * self.move_head_0_2tail
                    pattern = pattern[self.move_head_0_2tail:] + head_zeros

                # Move 1s from tail to head
                if self.move_tail_1_2head > 0:
                    tail_ones = '1' * self.move_tail_1_2head
                    pattern = tail_ones + pattern[:-self.move_tail_1_2head]

                # Convert to hex
                hex_output = hex(int(pattern, 2))[2:]
                hex_output = hex_output.zfill(self.len_hex)

                return hex_output
            except Exception as e:
                print(f"Error generating pattern: {e}")
                return None

        def to_string(self):
            """
            Format the pattern parameters into a string like '0_48_0_0'.

            Returns:
                str: Formatted string of pattern parameters.
            """
            return f"{self.space_0}_{self.space_1}_{self.move_head_0_2tail}_{self.move_tail_1_2head}"

        def describe(self):
            """
            Return a readable description of the pattern parameters.

            Returns:
                str: Description of the pattern parameters.
            """
            return f"Pattern structure: {self.to_string()}"

    def __init__(self, angle_deg, space_0, space_1, move_head_0_2tail, move_tail_1_2head, **kwargs):
        """
        Initialize the StructuredWave object.

        Args:
            angle_deg (float): Angle in degrees.
            space_0 (int): Number of zeros in the pattern.
            space_1 (int): Number of ones in the pattern.
            move_head_0_2tail (int): Number of zeros to move from head to tail.
            move_tail_1_2head (int): Number of ones to move from tail to head.
            **kwargs: Additional keyword arguments.
        """
        try:
            super().__init__(**kwargs)
            self.waveType = WaveType.StructuredWave
            self.pattern = self.PatternParams(space_0, space_1, move_head_0_2tail, move_tail_1_2head)
            self.pattern.len_hex = self.params['num_elements'] // 4
            self.pattern.activeList = self.pattern.generate_pattern()
            self.params['angle'] = angle_deg
            self.params['t0'] = floor(self.params["Zrange"][0] / self.params["f_AQ"])
            self.params['tmax'] = ceil((self.params["Zrange"][1] - self.params["Zrange"][0] + self.params["probeWidth"] * np.tan(np.radians(abs(angle_deg)))) * self.params["f_AQ"] / self.params["c0"])
            self.params['Nt'] = round(1.20 * (self.params['tmax'] - self.params['t0']))

            self.params['t0'] = int(self.params['t0'] * self.params['f_AQ'])

            if self.params["angle"] < -20 or self.params["angle"] > 20:
                raise ValueError("Angle must be between -20 and 20 degrees.")

            if len(self.pattern.activeList) != self.params["num_elements"] // 4:
                raise ValueError(f"Active list string must be {self.params['num_elements'] // 4} characters long.")

            self.delayedSignal = self._apply_delay()
        except Exception as e:
            print(f"Error initializing StructuredWave: {e}")

    def getName_field(self):
        """
        Generate the list of system matrix .hdr file paths for this wave.

        Returns:
            str: File path for the system matrix .hdr file.
        """
        try:
            pattern_str = self.pattern.activeList
            angle_str = self._format_angle()
            return f"field_{pattern_str}_{angle_str}"
        except Exception as e:
            print(f"Error generating file path: {e}")
            return None

    ## PRIVATE METHODS ##

    def _format_angle(self):
        """
        Format an angle into a 3-digit code like '120' for -20°, '020' for +20°.

        Args:
            angle (float): Angle in degrees.

        Returns:
            str: Formatted angle string.
        """
        return f"{'1' if self.params['angle'] < 0 else '0'}{abs(self.params['angle']):02d}"

    def _apply_delay(self):
        """
        Apply a temporal delay to the signal for each transducer element.

        Returns:
            ndarray: Array of delayed signals.
        """
        try:
            is_positive = self.params['angle'] >= 0
            delays = np.zeros(self.params['num_elements'])

            for i in range(self.params['num_elements']):
                delays[i] = (i * self.params['element_width'] * np.tan(np.deg2rad(abs(self.params['angle'] )))) / self.params['c0']  # Delay in seconds

            delay_samples = np.round(delays * self.params['f_AQ']).astype(int)
            max_delay = np.max(np.abs(delay_samples))

            delayed_signals = np.zeros((self.params['num_elements'], len(self.burst) + max_delay))
            for i in range(self.params['num_elements']):
                shift = delay_samples[i]

                if is_positive:
                    delayed_signals[i, shift:shift + len(self.burst)] = self.burst  # Right shift
                else:
                    delayed_signals[i, max_delay - shift:max_delay - shift + len(self.burst)] = self.burst  # Left shift

            return delayed_signals
        except Exception as e:
            print(f"Error applying delay: {e}")
            return None

    def _save2D_HDR_IMG(self, pathFolder):
        """
        Save the acoustic field to .img and .hdr files.

        Args:
            pathFolder (str): Path to the folder where files will be saved.
        """
        try:
            t_ex = 1 / self.params['f_US']
            angle_sign = '1' if self.params['angle'] < 0 else '0'
            formatted_angle = f"{angle_sign}{abs(self.params['angle']):02d}"

            # Define file names (img and hdr)
            file_name = f"field_{self.pattern.activeList}_{formatted_angle}"

            img_path = os.path.join(pathFolder, file_name + ".img")
            hdr_path = os.path.join(pathFolder, file_name + ".hdr")

            # Save the acoustic field to the .img file
            with open(img_path, "wb") as f_img:
                self.field.astype('float32').tofile(f_img)  # Save in float32 format (equivalent to "single" in MATLAB)

            # Generate headerFieldGlob
            headerFieldGlob = (
                f"!INTERFILE :=\n"
                f"modality : AOT\n"
                f"voxels number transaxial: {self.field.shape[2]}\n"
                f"voxels number transaxial 2: {self.field.shape[1]}\n"
                f"voxels number axial: {1}\n"
                f"field of view transaxial: {(self.params['Xrange'][1] - self.params['Xrange'][0]) * 1000}\n"
                f"field of view transaxial 2: {(self.params['Zrange'][1] - self.params['Zrange'][0]) * 1000}\n"
                f"field of view axial: {1}\n"
            )

            # Generate header
            header = (
                f"!INTERFILE :=\n"
                f"!imaging modality := AOT\n\n"
                f"!GENERAL DATA :=\n"
                f"!data offset in bytes := 0\n"
                f"!name of data file := system_matrix/{file_name}.img\n\n"
                f"!GENERAL IMAGE DATA\n"
                f"!total number of images := {self.field.shape[0]}\n"
                f"imagedata byte order := LITTLEENDIAN\n"
                f"!number of frame groups := 1\n\n"
                f"!STATIC STUDY (General) :=\n"
                f"number of dimensions := 3\n"
                f"!matrix size [1] := {self.field.shape[2]}\n"
                f"!matrix size [2] := {self.field.shape[1]}\n"
                f"!matrix size [3] := {self.field.shape[0]}\n"
                f"!number format := short float\n"
                f"!number of bytes per pixel := 4\n"
                f"scaling factor (mm/pixel) [1] := {self.params['dx'] * 1000}\n"
                f"scaling factor (mm/pixel) [2] := {self.params['dx'] * 1000}\n"
                f"scaling factor (s/pixel) [3] := {1 / self.params['f_AQ']}\n"
                f"first pixel offset (mm) [1] := {self.params['Xrange'][0] * 1e3}\n"
                f"first pixel offset (mm) [2] := {self.params['Zrange'][0] * 1e3}\n"
                f"first pixel offset (s) [3] := 0\n"
                f"data rescale offset := 0\n"
                f"data rescale slope := 1\n"
                f"quantification units := 1\n\n"
                f"!SPECIFIC PARAMETERS :=\n"
                f"angle (degree) := {self.params['angle']}\n"
                f"activation list := {''.join(f'{int(self.pattern.activeList[i:i+2], 16):08b}' for i in range(0, len(self.pattern.activeList), 2))}\n"
                f"number of US transducers := {self.params['num_elements']}\n"
                f"delay (s) := 0\n"
                f"us frequency (Hz) := {self.params['f_US']}\n"
                f"excitation duration (s) := {t_ex}\n"
                f"!END OF INTERFILE :=\n"
            )
            # Save the .hdr file
            with open(hdr_path, "w") as f_hdr:
                f_hdr.write(header)

            with open(os.path.join(pathFolder, "field.hdr"), "w") as f_hdr2:
                f_hdr2.write(headerFieldGlob)
        except Exception as e:
            print(f"Error saving HDR/IMG files: {e}")

    def _generate_2Dacoustic_field_KWAVE(self, isGPU = True if config.get_process() == 'gpu' else False):
        """
        Generate a 2D acoustic field using k-Wave.

        Args:
            isGpu (bool): Flag indicating whether to use GPU for simulation.

        Returns:
            ndarray: Simulated acoustic field data.
        """
        try:
            active_list = np.array([int(char) for char in ''.join(f"{int(self.pattern.activeList[i:i+2], 16):08b}" for i in range(0, len(self.pattern.activeList), 2))])

            kgrid = kWaveGrid([self.params["Nx"], self.params["Nz"]], [self.params["dx"], self.params["dz"]])
            kgrid.setTime(Nt=self.params['Nt'], dt=1 / self.params['f_AQ'])

            # Probe mask: aligned in the XZ plane
            source = kSource()
            source.p_mask = np.zeros((self.params['Nx'], self.params['Nz']))  # Create an empty grid for the source mask

            # Place active transducers in the mask
            for i in range(self.params['num_elements']):
                if active_list[i] == 1:  # Check if the element is active
                    x_pos = i  # Position of elements on the X-axis
                    source.p_mask[x_pos, 0] = 1  # Position in the XZ plane

            source.p_mask = source.p_mask.astype(int)
            source.p = self.delayedSignal[active_list == 1, :]

            # Define sensors to observe acoustic fields
            sensor = kSensor()
            sensor.mask = np.ones((self.params['Nx'], self.params['Nz']))  # Sensor covering the entire domain

            # Simulation options
            simulation_options = SimulationOptions(
                pml_inside=False,  # Prevent PML from being added inside the grid
                pml_x_size=20,  # PML size on the X-axis
                pml_z_size=20,  # PML size on the Z-axis
                use_sg=False,
                save_to_disk=True,
                input_filename=os.path.join(gettempdir(), "KwaveIN.h5"),
                output_filename=os.path.join(gettempdir(), "KwaveOUT.h5")
            )

            execution_options = SimulationExecutionOptions(
                is_gpu_simulation=config.get_process() == 'gpu' and isGPU,
                device_num=config.bestGPU
            )

            # Run the simulation
            print("Starting simulation...")
            sensor_data = kspaceFirstOrder2D(
                kgrid=kgrid,
                medium=self.medium,
                source=source,
                sensor=sensor,
                simulation_options=simulation_options,
                execution_options=execution_options,
            )
            print("Simulation completed successfully.")

            return sensor_data['p'].reshape(kgrid.Nt, self.params['Nz'], self.params['Nx'])
        except Exception as e:
            print(f"Error generating 2D acoustic field: {e}")
            return None

    def _generate_3Dacoustic_field_KWAVE(self):
        """
        Generate a 3D acoustic field using k-Wave.

        Returns:
            ndarray: Simulated acoustic field data.
        """
        try:
            active_list = np.array([int(char) for char in ''.join(f"{int(self.pattern.activeList[i:i+2], 16):08b}" for i in range(0, len(self.pattern.activeList), 2))])

            # Initialize grid and medium
            kgrid = kWaveGrid([self.params['Nx'], self.params['Ny'], self.params['Nz']], [self.params['dx'], self.params['dy'], self.params['dz']])
            kgrid.setTime(Nt=self.params['Nt'], dt=1 / self.params['f_AQ'])

            # Probe mask: aligned in the XZ plane
            source = kSource()
            source.p_mask = np.zeros((self.params['Nx'], self.params['Ny'], self.params['Nz']))  # Create an empty grid for the source mask

            # Place active transducers in the mask
            for i in range(self.params['num_elements']):
                if active_list[i] == 1:  # Check if the element is active
                    x_pos = i + self.params['Nx'] // 2 - self.params['num_elements'] // 2  # Position of elements on the X-axis
                    source.p_mask[x_pos, self.params['Ny'] // 2, 0] = 1  # Position in the XZ plane

            source.p_mask = source.p_mask.astype(int)
            source.p = self.delayedSignal[active_list == 1, :]

            # Define sensors to observe acoustic fields
            sensor = kSensor()
            sensor.mask = np.ones((self.params['Nx'], self.params['Ny'], self.params['Nz']))  # Sensor covering the entire domain

            # Simulation options
            simulation_options = SimulationOptions(
                pml_inside=False,  # Prevent PML from being added inside the grid
                pml_auto=True,
                use_sg=False,
                save_to_disk=True,
                input_filename=os.path.join(gettempdir(), "KwaveIN.h5"),
                output_filename=os.path.join(gettempdir(), "KwaveOUT.h5")
            )

            execution_options = SimulationExecutionOptions(
                is_gpu_simulation=config.get_process() == 'gpu',
                device_num=config.bestGPU() if config.get_process() == 'gpu' else None
            )

            # Run the simulation
            print("Starting simulation...")
            sensor_data = kspaceFirstOrder3D(
                kgrid=kgrid,
                medium=self.medium,
                source=source,
                sensor=sensor,
                simulation_options=simulation_options,
                execution_options=execution_options,
            )
            print("Simulation completed successfully.")

            return sensor_data['p'].reshape(kgrid.Nt, (self.params['Nz'], self.params['Ny'], self.params['Nx']))
        except Exception as e:
            print(f"Error generating 3D acoustic field: {e}")
            return None
    
class PlaneWave(StructuredWave):
    def __init__(self, angle, space_0 = 0, space_1 = 192, move_head_0_2tail = 0, move_tail_1_2head = 0, **kwargs):
        """
        Initialize the PlaneWave object.

        Args:
            angle_deg (float): Angle in degrees.
            **kwargs: Additional keyword arguments.
        """
        try:
            super().__init__(angle, space_0, space_1, move_head_0_2tail, move_tail_1_2head, **kwargs)
            self.waveType = WaveType.PlaneWave
        except Exception as e:
            print(f"Error initializing PlaneWave: {e}")
            raise 

    def _check_angle(self):
        """
        Check if the angle is within the valid range.

        Raises:
            ValueError: If the angle is not between -20 and 20 degrees.
        """
        if self.angle < -20 or self.angle > 20:
            raise ValueError("Angle must be between -20 and 20 degrees.")

    def getName_field(self):
        """
        Generate the list of system matrix .hdr file paths for this wave.

        Returns:
            str: File path for the system matrix .hdr file.
        """
        try:
            angle_str = self._format_angle()
            return f"field_{self.pattern.activeList}_{angle_str}"
        except Exception as e:
            print(f"Error generating file path: {e}")
            return None

class FocusedWave(AcousticField):

    def __init__(self, **kwargs):
        pass

    def getName_field(self):
        raise NotImplementedError("getName_field method not implemented for FocusedWave.")
    pass

class HydroWave(AcousticField):

    def __init__(self, waveType, dim=Dim.D3,**kwargs):
        super().__init__(**kwargs)
        if type(dim) != Dim:
            raise TypeError("dim must be an instance of the Dim Enum")
        if type(waveType) != WaveType:
            raise TypeError("waveType must be an instance of the WaveType Enum")
        self.waveType = waveType
        self.params = { 
            'typeSim': TypeSim.HYDRO.value,
            'dim': dim.value,
        }


    def getName_field(self):
        raise NotImplementedError("getName_field method not implemented for HydroWave.")
    pass

    def _generate_2Dacoustic_field_KWAVE(self):
        raise NotImplementedError("2D acoustic field generation not implemented for HydroWave.")

    def _generate_3Dacoustic_field_KWAVE(self):
        raise NotImplementedError("3D acoustic field generation not implemented for HydroWave.")
    
    def _save2D_HDR_IMG(sel):
        raise NotImplementedError("HDR/IMG saving not implemented for HydroWave.")
 
