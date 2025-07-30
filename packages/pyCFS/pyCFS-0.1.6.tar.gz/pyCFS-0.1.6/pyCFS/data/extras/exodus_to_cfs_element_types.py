import numpy as np
from pyCFS.data.io.cfs_types import cfs_element_type
from pyCFS.data.util import apply_dict_vectorized

# define mapping between exodus and cfs element types
type_link = {
    "BAR2": cfs_element_type.LINE2,
    "BAR3": cfs_element_type.LINE3,
    "TRI3": cfs_element_type.TRIA3,
    "TRI6": cfs_element_type.TRIA6,
    "QUAD4": cfs_element_type.QUAD4,
    "QUAD8": cfs_element_type.QUAD8,
    "QUAD9": cfs_element_type.QUAD9,
    "TETRA4": cfs_element_type.TET4,
    "TETRA10": cfs_element_type.TET10,
    "HEX8": cfs_element_type.HEXA8,
    "HEX20": cfs_element_type.HEXA20,
    "HEX27": cfs_element_type.HEXA27,
    "PYRA5": cfs_element_type.PYRA5,
    "PYRA13": cfs_element_type.PYRA13,
    "PYRA14": cfs_element_type.PYRA14,
    "WEDGE6": cfs_element_type.WEDGE6,
    "WEDGE15": cfs_element_type.WEDGE15,
    "WEDGE18": cfs_element_type.WEDGE18,
}


def exodus_to_cfs_elem_type(exodus_elem_types: np.ndarray) -> np.ndarray:
    """
    Maps Exodus element types to CFS element types.

    This function takes an array of Exodus element types and maps them to the corresponding
    CFS element types using a predefined dictionary. If any element types are not defined
    in the dictionary, they are mapped to `cfs_element_type.UNDEF`.

    Parameters
    ----------
    exodus_elem_types : np.ndarray
        An array of Exodus element types.

    Returns
    -------
    np.ndarray
        An array of CFS element types corresponding to the input Exodus element types.

    Warns
    -----
    UserWarning
        If any element types in the input array are not implemented in the mapping dictionary.
    """
    undefined_elem_types = {elem for elem in exodus_elem_types if elem not in type_link}
    if undefined_elem_types:
        print(f"Warning: Elements of type {', '.join(undefined_elem_types)} are not implemented yet.")
    return apply_dict_vectorized(dictionary=type_link, data=exodus_elem_types, val_no_key=cfs_element_type.UNDEF)
