# -- import packages: ----------------------------------------------------------
import ABCParse
import autodevice
import anndata
import logging
import torch as _torch
import numpy as np

# -- import local dependencies: ------------------------------------------------
from ._locator import locate
from ._formatter import format_data

# -- set typing: ---------------------------------------------------------------
from typing import Dict, List, Optional, Union, Any, Generator, Tuple

# -- configure logger: ---------------------------------------------------------
logger = logging.getLogger(__name__)


class AnnDataFetcher(ABCParse.ABCParse):
    """Fetches and formats data from AnnData objects.
    
    This class provides functionality to retrieve data from AnnData objects, with options
    for grouping, tensor conversion, and device placement. It handles both direct data
    access and grouped data retrieval.
    
    Attributes:
        _GROUPED: Property that returns a pandas GroupBy object when groupby is specified.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the AnnDataFetcher."""
        self.__parse__(locals(), public=[None])
        logger.debug("Initialized AnnDataFetcher")

    @property
    def _GROUPED(self):
        """Get the grouped data from AnnData.obs.
        
        Returns:
            pandas GroupBy object for the specified groupby column.
        """
        logger.debug(f"Grouping data by: {self._groupby}")
        return self._adata.obs.groupby(self._groupby)

    def _forward(self, adata: anndata.AnnData, key: str) -> Union[_torch.Tensor, np.ndarray]:
        """Retrieve and format data for a single key.
        
        Args:
            adata: AnnData object to fetch data from.
            key: Key to fetch data for.
            
        Returns:
            Formatted data as either torch.Tensor or np.ndarray.
        """
        logger.debug(f"Fetching data for key: {key}")
        if key == "X":
            data = getattr(adata, "X")
            logger.debug("Retrieved data from adata.X")
        else:
            attr = locate(adata, key)
            data = getattr(adata, attr)[key]
            logger.debug(f"Retrieved data from adata.{attr}['{key}']")
        return format_data(data=data, torch=self._torch, device=self._device)

    def _grouped_subroutine(
        self, 
        adata: anndata.AnnData, 
        key: str
    ) -> Generator[Union[Tuple[str, Union[_torch.Tensor, np.ndarray]], Union[_torch.Tensor, np.ndarray]], None, None]:
        """Process data for each group when groupby is specified.
        
        Args:
            adata: AnnData object to fetch data from.
            key: Key to fetch data for.
            
        Yields:
            If as_dict is True: Tuples of (group_name, formatted_data)
            If as_dict is False: Formatted data for each group
        """
        logger.debug(f"Processing grouped data for key: {key}")
        if self._as_dict:
            for group, group_df in self._GROUPED:
                logger.debug(f"Processing group: {group}")
                yield group, self._forward(adata[group_df.index], key)
        else:
            for group, group_df in self._GROUPED:
                logger.debug(f"Processing group: {group}")
                yield self._forward(adata[group_df.index], key)

    def __call__(
        self,
        adata: anndata.AnnData,
        key: str,
        groupby: Optional[str] = None,
        torch: bool = False,
        device: _torch.device = autodevice.AutoDevice(),
        as_dict: bool = True,
    ) -> Union[
        _torch.Tensor,
        np.ndarray,
        List[Union[_torch.Tensor, np.ndarray]],
        Dict[str, Union[_torch.Tensor, np.ndarray]]
    ]:
        """Fetch and format data from an AnnData object.
        
        Args:
            adata: AnnData object to fetch data from.
            key: Key to fetch data for (e.g., "X_pca" for adata.obsm['X_pca']).
            groupby: Optional column name in adata.obs to group data by.
            torch: Whether to return data as torch.Tensor (True) or np.ndarray (False).
            device: Device to place tensor on if torch=True.
            as_dict: When groupby is specified, whether to return data as a dictionary
                    with group names as keys (True) or as a list (False).
                    
        Returns:
            If groupby is None:
                Single array/tensor for the specified key
            If groupby is specified and as_dict is True:
                Dictionary mapping group names to arrays/tensors
            If groupby is specified and as_dict is False:
                List of arrays/tensors for each group
                
        Example:
            >>> import anndata
            >>> adata = anndata.AnnData(X=[[1, 2], [3, 4]])
            >>> adata.obs['cell_type'] = ['A', 'B']
            >>> adata.obsm['X_pca'] = [[0.1, 0.2], [0.3, 0.4]]
            >>> fetcher = AnnDataFetcher()
            >>> # Get single array
            >>> data = fetcher(adata, "X_pca")
            >>> # Get grouped data as dictionary
            >>> grouped_data = fetcher(adata, "X_pca", groupby="cell_type")
        """
        logger.debug(
            f"Fetch called for key: {key}"
            + (f" with groupby: {groupby}" if groupby else "")
        )
        self.__update__(locals(), public=[None])

        if hasattr(self, "_groupby"):
            logger.debug(
                f"Returning grouped data as {'dictionary' if self._as_dict else 'list'}"
            )
            if self._as_dict:
                return dict(self._grouped_subroutine(adata, key))
            return list(self._grouped_subroutine(adata, key))
        return self._forward(adata, key)


def fetch(
    adata: anndata.AnnData,
    key: str,
    groupby: Optional[str] = None,
    torch: bool = False,
    device: _torch.device = autodevice.AutoDevice(),
    as_dict: bool = True,
    *args,
    **kwargs,
) -> Union[
    _torch.Tensor,
    np.ndarray,
    List[Union[_torch.Tensor, np.ndarray]],
    Dict[str, Union[_torch.Tensor, np.ndarray]]
]:
    """Fetch and format data from an AnnData object.
    
    This function provides a convenient interface to retrieve and format data from AnnData
    objects. It supports both direct data access and grouped data retrieval, with options
    for tensor conversion and device placement.
    
    Args:
        adata: AnnData object to fetch data from.
        key: Key to fetch data for (e.g., "X_pca" for adata.obsm['X_pca']).
        groupby: Optional column name in adata.obs to group data by.
        torch: Whether to return data as torch.Tensor (True) or np.ndarray (False).
        device: Device to place tensor on if torch=True.
        as_dict: When groupby is specified, whether to return data as a dictionary
                with group names as keys (True) or as a list (False).
                
    Returns:
        If groupby is None:
            Single array/tensor for the specified key
        If groupby is specified and as_dict is True:
            Dictionary mapping group names to arrays/tensors
        If groupby is specified and as_dict is False:
            List of arrays/tensors for each group
            
    Example:
        >>> import anndata
        >>> adata = anndata.AnnData(X=[[1, 2], [3, 4]])
        >>> adata.obs['cell_type'] = ['A', 'B']
        >>> adata.obsm['X_pca'] = [[0.1, 0.2], [0.3, 0.4]]
        >>> # Get single array
        >>> data = fetch(adata, "X_pca")
        >>> # Get grouped data as dictionary
        >>> grouped_data = fetch(adata, "X_pca", groupby="cell_type")
        >>> # Get tensor on GPU
        >>> tensor_data = fetch(adata, "X_pca", torch=True)
    """
    logger.debug(
        f"Fetch function called for key: {key}"
        + (f" with groupby: {groupby}" if groupby else "")
    )
    fetcher = AnnDataFetcher()
    return fetcher(
        adata=adata,
        key=key,
        groupby=groupby,
        torch=torch,
        device=device,
        as_dict=as_dict,
        *args,
        **kwargs,
    )
