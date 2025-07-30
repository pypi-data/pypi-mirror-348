import numpy as np

from pyCFS.data.extras.cgns_types import cgns_element_type
from pyCFS.data.io.cfs_types import cfs_element_type
from pyCFS.data.util import apply_dict_vectorized

type_link_cgns_cfs = {
    cgns_element_type.NODE: cfs_element_type.POINT,
    cgns_element_type.BAR_2: cfs_element_type.LINE2,
    cgns_element_type.BAR_3: cfs_element_type.LINE3,
    cgns_element_type.TRI_3: cfs_element_type.TRIA3,
    cgns_element_type.TRI_6: cfs_element_type.TRIA6,
    cgns_element_type.QUAD_4: cfs_element_type.QUAD4,
    cgns_element_type.QUAD_8: cfs_element_type.QUAD8,
    cgns_element_type.QUAD_9: cfs_element_type.QUAD9,
    cgns_element_type.TETRA_4: cfs_element_type.TET4,
    cgns_element_type.TETRA_10: cfs_element_type.TET10,
    cgns_element_type.PYRA_5: cfs_element_type.PYRA5,
    cgns_element_type.PYRA_14: cfs_element_type.PYRA14,
    cgns_element_type.PENTA_6: cfs_element_type.WEDGE6,
    cgns_element_type.PENTA_15: cfs_element_type.WEDGE15,
    cgns_element_type.PENTA_18: cfs_element_type.WEDGE18,
    cgns_element_type.HEXA_8: cfs_element_type.HEXA8,
    cgns_element_type.HEXA_20: cfs_element_type.HEXA20,
    cgns_element_type.HEXA_27: cfs_element_type.HEXA27,
    # cgns_element_type.MIXED : cfs_element_type.MIXED,
    cgns_element_type.PYRA_13: cfs_element_type.PYRA13,
    # cgns_element_type.NGON_n : cfs_element_type.NGONn,
    # cgns_element_type.NFACE_n : cfs_element_type.NFACEn,
    # cgns_element_type.BAR_4: cfs_element_type.LINE4,
    # cgns_element_type.TRI_9: cfs_element_type.TRIA9,
    # cgns_element_type.TRI_10: cfs_element_type.TRIA10,
    # cgns_element_type.QUAD_12: cfs_element_type.QUAD12,
    # cgns_element_type.QUAD_16: cfs_element_type.QUAD16,
    # cgns_element_type.TETRA_16: cfs_element_type.TET16,
    # cgns_element_type.TETRA_20: cfs_element_type.TET20,
    # cgns_element_type.PYRA_21: cfs_element_type.PYRA21,
    # cgns_element_type.PYRA_29: cfs_element_type.PYRA29,
    # cgns_element_type.PYRA_30: cfs_element_type.PYRA30,
    # cgns_element_type.PENTA_24: cfs_element_type.WEDGE24,
    # cgns_element_type.PENTA_38: cfs_element_type.WEDGE38,
    # cgns_element_type.PENTA_40: cfs_element_type.WEDGE40,
    # cgns_element_type.HEXA_32: cfs_element_type.HEXA32,
    # cgns_element_type.HEXA_56: cfs_element_type.HEXA56,
    # cgns_element_type.HEXA_64: cfs_element_type.HEXA64,
    # cgns_element_type.BAR_5: cfs_element_type.LINE5,
    # cgns_element_type.TRI_12: cfs_element_type.TRIA12,
    # cgns_element_type.TRI_15: cfs_element_type.TRIA15,
    # cgns_element_type.QUAD_P4_16 : cfs_element_type.QUAD_P4_16,
    # cgns_element_type.QUAD_25: cfs_element_type.QUAD25,
    # cgns_element_type.TETRA_22: cfs_element_type.TET22,
    # cgns_element_type.TETRA_34: cfs_element_type.TET34,
    # cgns_element_type.TETRA_35: cfs_element_type.TET35,
    # cgns_element_type.PYRA_P4_29 : cfs_element_type.PYRA_P4_29,
    # cgns_element_type.PYRA_50: cfs_element_type.PYRA50,
    # cgns_element_type.PYRA_55: cfs_element_type.PYRA55,
    # cgns_element_type.PENTA_33: cfs_element_type.WEDGE33,
    # cgns_element_type.PENTA_66: cfs_element_type.WEDGE66,
    # cgns_element_type.PENTA_75: cfs_element_type.WEDGE75,
    # cgns_element_type.HEXA_44: cfs_element_type.HEXA44,
    # cgns_element_type.HEXA_98: cfs_element_type.HEXA98,
    # cgns_element_type.HEXA_125: cfs_element_type.HEXA125,
}


# mapping cgns element types array to cfs element types array
def cgns_to_cfs_elem_type(cgns_elem_types: np.ndarray):
    return apply_dict_vectorized(dictionary=type_link_cgns_cfs, data=cgns_elem_types, val_no_key=cfs_element_type.UNDEF)
