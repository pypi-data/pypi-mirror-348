# -- import packages: ----------------------------------------------------------
import ABCParse
import autodevice
import anndata
import logging
import numpy as np
import torch as _torch


# -- set typing: ---------------------------------------------------------------
from typing import Union, Optional

# -- configure logger: ---------------------------------------------------------
logger = logging.getLogger(__name__)


# -- operational class: --------------------------------------------------------
class DataFormatter(ABCParse.ABCParse):
    """Format data to interface with numpy or torch, on a specified device.
    
    This class provides functionality to convert data between numpy arrays and torch tensors,
    with support for device placement and various input types (numpy arrays, torch tensors,
    and AnnData ArrayViews).
    
    Attributes:
        _data: The input data to be formatted.
    """

    def __init__(self, data: Union[_torch.Tensor, np.ndarray], *args, **kwargs):
        """Initialize the DataFormatter.
        
        Args:
            data: Input data to format (numpy array, torch tensor, or ArrayView).
        """
        self.__parse__(locals())
        logger.debug(f"Initialized DataFormatter with data type: {type(data)}")

    @property
    def device_type(self) -> str:
        """Get the device type of the data.
        
        Returns:
            Device type string ('cpu', 'cuda', or 'mps').
        """
        if hasattr(self._data, "device"):
            return self._data.device.type
        return "cpu"

    @property
    def is_ArrayView(self) -> bool:
        """Check if data is an AnnData ArrayView.
        
        Returns:
            True if data is an ArrayView, False otherwise.
        """
        return isinstance(self._data, anndata._core.views.ArrayView)

    @property
    def is_numpy_array(self) -> bool:
        """Check if data is a numpy array.
        
        Returns:
            True if data is a numpy array, False otherwise.
        """
        return isinstance(self._data, np.ndarray)

    @property
    def is_torch_Tensor(self) -> bool:
        """Check if data is a torch tensor.
        
        Returns:
            True if data is a torch tensor, False otherwise.
        """
        return isinstance(self._data, _torch.Tensor)

    @property
    def on_cpu(self) -> bool:
        """Check if data is on CPU.
        
        Returns:
            True if data is on CPU, False otherwise.
        """
        return self.device_type == "cpu"

    @property
    def on_gpu(self) -> bool:
        """Check if data is on GPU (CUDA or MPS).
        
        Returns:
            True if data is on GPU, False otherwise.
        """
        return self.device_type in ["cuda", "mps"]

    def to_numpy(self) -> np.ndarray:
        """Convert data to numpy array.
        
        This method handles conversion from various input types (torch tensor, ArrayView)
        to numpy array, including proper handling of GPU tensors.
        
        Returns:
            Data as numpy array.
            
        Example:
            >>> import torch
            >>> formatter = DataFormatter(torch.tensor([[1, 2], [3, 4]]))
            >>> numpy_data = formatter.to_numpy()
            >>> type(numpy_data)
            <class 'numpy.ndarray'>
        """
        logger.debug("Converting data to numpy array")
        if self.is_torch_Tensor:
            if self.on_gpu:
                logger.debug("Converting GPU tensor to numpy array")
                return self._data.detach().cpu().numpy()
            logger.debug("Converting CPU tensor to numpy array")
            return self._data.numpy()
        elif self.is_ArrayView:
            logger.debug("Converting ArrayView to numpy array")
            return self._data.toarray()
        logger.debug("Data already in numpy format")
        return self._data

    def to_torch(self, device: Optional[_torch.device] = None) -> _torch.Tensor:
        """Convert data to torch tensor on specified device.
        
        This method handles conversion from various input types (numpy array, ArrayView)
        to torch tensor, with proper device placement.
        
        Args:
            device: Device to place tensor on. If None, uses autodevice.AutoDevice().
            
        Returns:
            Data as torch tensor on specified device.
            
        Example:
            >>> import numpy as np
            >>> formatter = DataFormatter(np.array([[1, 2], [3, 4]]))
            >>> tensor_data = formatter.to_torch(device='cuda')
            >>> tensor_data.device
            device(type='cuda', index=0)
        """
        if device is None:
            device = autodevice.AutoDevice()
        logger.debug(f"Converting data to torch tensor on device: {device}")
        self.__update__(locals())

        if self.is_torch_Tensor:
            logger.debug(f"Moving existing tensor to device: {device}")
            return self._data.to(self._device)
        elif self.is_ArrayView:
            logger.debug("Converting ArrayView to numpy before torch conversion")
            self._data = self._data.toarray()
        logger.debug("Converting numpy array to torch tensor")
        return _torch.Tensor(self._data).to(self._device)


# -- functional wrap: ----------------------------------------------------------
def format_data(
    data: Union[np.ndarray, _torch.Tensor], 
    torch: bool = False, 
    device: Optional[_torch.device] = None,
) -> Union[np.ndarray, _torch.Tensor]:
    """Format data as either numpy array or torch tensor.
    
    This function provides a convenient interface to convert data between numpy arrays
    and torch tensors, with support for device placement.
    
    Args:
        data: Input data to format (numpy array, torch tensor, or ArrayView).
        torch: Whether to return data as torch tensor (True) or numpy array (False).
        device: Device to place tensor on if torch=True. If None, uses autodevice.AutoDevice().
        
    Returns:
        Formatted data as either numpy array or torch tensor.
        
    Example:
        >>> import numpy as np
        >>> data = np.array([[1, 2], [3, 4]])
        >>> # Get numpy array
        >>> numpy_data = format_data(data, torch=False)
        >>> # Get tensor on GPU
        >>> tensor_data = format_data(data, torch=True, device='cuda')
    """
    if device is None:
        device = autodevice.AutoDevice()
    logger.debug(
        f"Formatting data as {'torch tensor' if torch else 'numpy array'}"
        + (f" on device: {device}" if torch else "")
    )
    formatter = DataFormatter(data=data)
    if torch:
        return formatter.to_torch(device=device)
    return formatter.to_numpy()
