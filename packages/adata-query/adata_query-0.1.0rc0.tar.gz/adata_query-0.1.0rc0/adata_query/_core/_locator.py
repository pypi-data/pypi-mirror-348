# -- import packages: ----------------------------------------------------------
import ABCParse
import anndata
import logging
import numpy as np

# -- set type hints: -----------------------------------------------------------
from typing import List, Optional, Dict, Any

# -- configure logger: ---------------------------------------------------------
logger = logging.getLogger(__name__)


# -- operational class: --------------------------------------------------------
class AnnDataLocator(ABCParse.ABCParse):
    """Locates and retrieves attributes from AnnData objects.
    
    This class provides functionality to locate specific keys within an AnnData object's
    various attributes (obsm, layers, etc.). It maintains an internal mapping of available
    attributes and their keys for efficient lookup.
    
    Attributes:
        _ATTRS (Dict[str, Any]): Internal storage of attribute mappings.
        _searchable (List[str]): List of attribute names to search through.
    """

    def __init__(self, searchable: Optional[List[str]] = None, *args, **kwargs) -> None:
        """Initialize the AnnDataLocator.
        
        Args:
            searchable: Optional list of additional attribute names to search through.
                       Defaults to None, which only searches 'X'.
        """
        self._ATTRS = {}
        self._searchable = ['X']
        if not searchable is None:
            self._searchable += searchable
        logger.debug(f"Initialized AnnDataLocator with searchable: {self._searchable}")

    def _stash(self, attr: str, attr_val: Any) -> None:
        """Store an attribute and its value in the internal mapping.
        
        Args:
            attr: Name of the attribute to store.
            attr_val: Value of the attribute to store.
        """
        self._ATTRS[attr] = attr_val
        setattr(self, attr, attr_val)
        logger.debug(f"Stashed attribute: {attr}")

    def _intake(self, adata: anndata.AnnData) -> None:
        """Process and store all relevant attributes from an AnnData object.
        
        This method scans the AnnData object for attributes containing keys (e.g., obsm_keys),
        layers, and other searchable attributes, storing them in the internal mapping.
        
        Args:
            adata: AnnData object to process.
        """
        logger.debug("Starting data intake from AnnData object")
        for attr in adata.__dir__():
            if "key" in attr:
                attr_val = getattr(adata, attr)()
                self._stash(attr, attr_val)
            if attr == "layers":
                attr_val = list(getattr(adata, attr))
                self._stash(attr, attr_val)
            if attr in self._searchable:
                self._stash(attr, attr)
        logger.debug(f"Completed data intake. Available attributes: {list(self._ATTRS.keys())}")

    def _cross_reference(self, passed_key: str) -> List[str]:
        """Find all attributes that contain the given key.
        
        Args:
            passed_key: The key to search for in attribute values.
            
        Returns:
            List of attribute names that contain the passed key.
        """
        matches = [key for key, val in self._ATTRS.items() if passed_key in val]
        logger.debug(f"Cross reference for key '{passed_key}' found matches: {matches}")
        return matches

    def _query_str_vals(self, query_result: List[str]) -> str:
        """Format query results as a comma-separated string.
        
        Args:
            query_result: List of attribute names to format.
            
        Returns:
            Comma-separated string of attribute names.
        """
        return ", ".join(query_result)

    def _format_error_msg(self, key: str, query_result: List[str]) -> str:
        """Format an error message for key lookup failures.
        
        Args:
            key: The key that was not found or had multiple matches.
            query_result: List of matches found (if any).
            
        Returns:
            Formatted error message string.
        """
        if len(query_result) > 1:
            msg = f"Found more than one match: [{self._query_str_vals(query_result)}]"
            logger.warning(msg)
            return msg
        msg = f"{key} NOT FOUND"
        logger.error(msg)
        return msg

    def _format_output_str(self, query_result: List[str]) -> str:
        """Extract the attribute name from a query result.
        
        Args:
            query_result: List containing a single query result.
            
        Returns:
            The attribute name without the '_keys' suffix.
        """
        return query_result[0].split("_keys")[0]

    def _forward(self, adata: anndata.AnnData, key: str) -> str:
        """Main processing method to locate a key in an AnnData object.
        
        Args:
            adata: AnnData object to search in.
            key: Key to locate.
            
        Returns:
            The attribute name containing the key.
            
        Raises:
            KeyError: If the key is not found or has multiple matches.
        """
        logger.debug(f"Locating key '{key}' in AnnData object")
        self._intake(adata)
        query_result = self._cross_reference(passed_key=key)

        if len(query_result) != 1:
            raise KeyError(self._format_error_msg(key, query_result))

        result = self._format_output_str(query_result)
        logger.debug(f"Successfully located key '{key}' in attribute: {result}")
        return result

    def __call__(self, adata: anndata.AnnData, key: str) -> str:
        """Callable interface to locate a key in an AnnData object.
        
        Args:
            adata: AnnData object to search in.
            key: Key to locate.
            
        Returns:
            The attribute name containing the key.
            
        Raises:
            KeyError: If the key is not found or has multiple matches.
        """
        return self._forward(adata, key)


def locate(adata: anndata.AnnData, key: str) -> str:
    """Locate a key within an AnnData object's attributes.
    
    This function provides a convenient interface to find which attribute of an AnnData
    object contains a specific key. For example, if you want to access adata.obsm['X_pca'],
    you would pass "X_pca" as the key, and this function would return "obsm".
    
    Args:
        adata: AnnData object to search in.
        key: Key to locate (e.g., "X_pca" for adata.obsm['X_pca']).
        
    Returns:
        The attribute name containing the key (e.g., "obsm" for adata.obsm['X_pca']).
        
    Raises:
        KeyError: If the key is not found or has multiple matches.
        
    Example:
        >>> import anndata
        >>> adata = anndata.AnnData(X=[[1, 2], [3, 4]])
        >>> adata.obsm['X_pca'] = [[0.1, 0.2], [0.3, 0.4]]
        >>> locate(adata, "X_pca")
        'obsm'
    """
    logger.debug(f"Locate function called for key: {key}")
    locator = AnnDataLocator()
    return locator(adata=adata, key=key)
