"""
Module containing data processing utilities for writing HDF5 files in openCFS format
"""

import copy

import h5py
import numpy as np
from pyCFS.data import io, v_def
from pyCFS.data.io import CFSResultContainer
from pyCFS.data.io.cfs_types import cfs_analysis_type, cfs_result_type, cfs_element_type
from .pycfs_data_fixtures import (
    dummy_CFSMeshData_obj,
    dummy_CFSResultContainer_obj,
    dummy_CFSResultContainer_history_obj,
    dummy_CFSMeshData_linear_elements,
    dummy_CFSResultArray_obj,
)


def test_CFSMeshData(dummy_CFSMeshData_obj):

    print(dummy_CFSMeshData_obj.get_mesh_quality())

    reg_info_demo = dummy_CFSMeshData_obj.Regions
    coord = dummy_CFSMeshData_obj.Coordinates
    conn = dummy_CFSMeshData_obj.Connectivity[1:, :]
    mesh_coord = io.CFSMeshData.from_coordinates_connectivity(coordinates=coord, connectivity=conn, element_dimension=2)
    print(mesh_coord)
    print(mesh_coord.Regions[0])


def test_CFSMeshData_element_centroids(dummy_CFSMeshData_obj):
    ref_sol = np.array([[0.5, 0.5, 0.5], [0.0, 1 / 3.0, 1 / 3.0], [0.0, 2 / 3.0, 2 / 3.0], [1.0, 0.5, 0.5]])
    np.testing.assert_array_equal(dummy_CFSMeshData_obj.get_mesh_centroids(), ref_sol)

    ref_sol_reg = np.array([[0.5, 0.5, 0.5]])
    np.testing.assert_array_equal(dummy_CFSMeshData_obj.get_region_centroids(region="Vol"), ref_sol_reg)


def test_CFSMeshData_element_quality(dummy_CFSMeshData_obj):
    ref_sol = np.array([0.8660254, 0.8660254, 1.0, 1.0])
    np.testing.assert_array_almost_equal(dummy_CFSMeshData_obj.get_mesh_quality(), ref_sol, decimal=6)

    ref_sol_reg = np.array([1.0])
    np.testing.assert_array_almost_equal(
        dummy_CFSMeshData_obj.get_region_element_quality(region="Vol"), ref_sol_reg, decimal=9
    )
    ref_sol_reg = np.array([0.25, 0.25])
    np.testing.assert_array_almost_equal(
        dummy_CFSMeshData_obj.get_region_element_quality(region="Surf1", metric="skewness"), ref_sol_reg, decimal=9
    )


def test_CFSMeshData_surface_normal(dummy_CFSMeshData_obj):
    ref_sol_el = np.array([[np.nan, np.nan, np.nan], [-1.0, 0, 0], [-1.0, 0, 0], [-1.0, 0, 0]])
    np.testing.assert_array_equal(dummy_CFSMeshData_obj.get_mesh_surface_normals(), ref_sol_el)

    ref_sol_node = np.tile(np.array([-1.0, 0, 0]), (8, 1))
    np.testing.assert_array_equal(
        dummy_CFSMeshData_obj.get_mesh_surface_normals(restype=cfs_result_type.NODE), ref_sol_node
    )


def test_CFSMeshData_surface_normal_selected_elems(working_directory="."):
    file = f"{working_directory}/tests/data/sim_io/NormalSurfaceOscillatingSphere.h5ref"
    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        mesh_data_read = h5reader.MeshData
    # non-flat surface region
    region = "S_r"
    # get region element ids
    elems = mesh_data_read.get_region_elements(region)
    # indices of some elements
    elem_idx_choose = elems[5:8] - 1
    normals = mesh_data_read.get_mesh_surface_normals(restype=cfs_result_type.ELEMENT, el_idx_include=elem_idx_choose)
    ref_sol = np.array(
        [
            [-8.429716448008717222e-01, 2.717155432814186145e-01, 4.642945935513318467e-01],
            [-5.524521970480528177e-01, 7.371719860968946048e-01, 3.890681596979366219e-01],
            [-8.348530249391070135e-02, 9.408554675727535122e-01, 3.283613762395871105e-01],
        ]
    )
    np.testing.assert_array_equal(normals, ref_sol)


def test_CFSMeshData_from_various(dummy_CFSMeshData_linear_elements: io.CFSMeshData):
    coord = dummy_CFSMeshData_linear_elements.Coordinates
    conn = dummy_CFSMeshData_linear_elements.Connectivity
    el_types = dummy_CFSMeshData_linear_elements.Types
    regions = dummy_CFSMeshData_linear_elements.Regions

    merged_region = None
    for r in dummy_CFSMeshData_linear_elements.Regions:
        if merged_region is None:
            merged_region = r
        else:
            merged_region, _, _ = merged_region.merge(r)

    merged_region.Name = "region_all_entities"

    mesh_merged = copy.deepcopy(dummy_CFSMeshData_linear_elements)
    mesh_merged.Regions = [merged_region]
    mesh_merged.drop_unused_nodes_elements()

    mesh_data = io.CFSMeshData.from_coordinates_connectivity(
        coordinates=coord, connectivity=conn, element_types=el_types, region_name="region_all_entities"
    )

    assert mesh_data == mesh_merged

    for reg in dummy_CFSMeshData_linear_elements.Regions:

        coord = dummy_CFSMeshData_linear_elements.get_region_coordinates(reg)
        conn = dummy_CFSMeshData_linear_elements.get_region_connectivity(reg)

        mesh_single_reg = copy.deepcopy(dummy_CFSMeshData_linear_elements)
        mesh_single_reg.drop_unused_nodes_elements(reg_data_list=[reg])

        mesh_data = io.CFSMeshData.from_coordinates_connectivity(
            coordinates=coord, connectivity=conn, element_dimension=reg.Dimension, region_name=reg.Name
        )

        assert mesh_data == mesh_single_reg


def test_CFSResultContainer_add_data_array(dummy_CFSResultContainer_obj, dummy_CFSMeshData_obj):
    data = np.ones((dummy_CFSResultContainer_obj.StepValues.size, 4, 1))
    meta_data = {
        "Quantity": "test_quantity",
        "Region": "Surf1",
        "StepValues": dummy_CFSResultContainer_obj.StepValues,
        "DimNames": None,
        "ResType": cfs_result_type.NODE,
        "IsComplex": False,
        "MultiStepID": 1,
        "AnalysisType": cfs_analysis_type.TRANSIENT,
    }

    dummy_CFSResultContainer_obj.add_data_array(data=data, meta_data=meta_data)

    dummy_CFSResultContainer_obj.check_result(mesh=dummy_CFSMeshData_obj)


def test_CFSResultContainerProperties(dummy_CFSResultContainer_obj: CFSResultContainer):
    # Check ResultContainer Properties
    assert all(
        item in [item.Quantity for item in dummy_CFSResultContainer_obj.Data]
        for item in dummy_CFSResultContainer_obj.Quantities
    )
    assert all(
        item in [item.Region for item in dummy_CFSResultContainer_obj.Data]
        for item in dummy_CFSResultContainer_obj.Regions
    )
    assert dummy_CFSResultContainer_obj.AnalysisType == cfs_analysis_type.TRANSIENT
    assert dummy_CFSResultContainer_obj.MultiStepID == 1
    assert all(
        item in [item.ResultInfo for item in dummy_CFSResultContainer_obj.Data]
        for item in dummy_CFSResultContainer_obj.ResultInfo
    )


def test_CFSResultArray_init():
    # Initialize empty CFSResultArray
    empty_array = io.CFSResultArray([])
    print(empty_array.MetaData)


def test_CFSResultArray_require_shape():
    # Initialize single step scalar node data with unsupported shape
    shape_array = io.CFSResultArray(np.zeros(shape=(4)))

    shape_array.ResType = cfs_result_type.NODE
    data_array = shape_array.require_shape()

    data_array.check_result_array()

    # Initialize array with unsupported shape
    shape_array = io.CFSResultArray(np.zeros(shape=(1, 4, 3)))

    shape_array.ResType = cfs_result_type.REGION
    shape_array.StepValues = np.linspace(0, 1, 4)
    data_array = shape_array.require_shape()

    data_array.check_result_array()

    # Initialize array with swapped axes and 4th dimension
    shape_array = io.CFSResultArray(np.zeros(shape=(3, 3, 17, 1)))

    shape_array.ResType = cfs_result_type.ELEMENT
    shape_array.StepValues = np.linspace(0, 1, 3)
    shape_array.DimNames = ["x", "y", "z"]
    data_array = shape_array.require_shape()

    data_array.check_result_array()


def test_check_result_array(dummy_CFSResultArray_obj):
    dummy_CFSResultArray_obj[0, 0, 0] = np.nan
    dummy_CFSResultArray_obj.check_result_array()


def test_write_history(dummy_CFSMeshData_obj, dummy_CFSResultContainer_history_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io_history.cfs"

    print("Write demo history file")
    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh=dummy_CFSMeshData_obj)
        h5writer.write_history_multistep(result=dummy_CFSResultContainer_history_obj)


def test_read_history(dummy_CFSMeshData_obj, dummy_CFSResultContainer_history_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io_history.cfs"

    test_write_history(dummy_CFSMeshData_obj, dummy_CFSResultContainer_history_obj, working_directory)

    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        result_data_read = h5reader.HistoryData
        np.testing.assert_equal(dummy_CFSResultContainer_history_obj, result_data_read)


def test_file_info(working_directory="."):
    file = f"{working_directory}/tests/data/io/result_mixed_mesh_history.cfs"

    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        info_str = str(h5reader)

    ref_str = """Mesh
 - Dimension: 3
 - Nodes:     6197
 - Elements:  5369
 - Regions:   12
   - Group : P0_elem (3D, 8 nodes, 1 elements)
   - Group : P0_node (0D, 1 nodes, 1 elements)
   - Group : P1_elem (3D, 8 nodes, 1 elements)
   - Group : P1_node (0D, 1 nodes, 1 elements)
   - Group : P2_elem (3D, 8 nodes, 1 elements)
   - Group : P2_node (0D, 1 nodes, 1 elements)
   - Group : P3_elem (3D, 8 nodes, 1 elements)
   - Group : P3_node (0D, 1 nodes, 1 elements)
   - Region: S_bottom (2D, 69 nodes, 55 elements)
   - Region: S_top (2D, 69 nodes, 55 elements)
   - Region: V_air (3D, 5849 nodes, 4870 elements)
   - Region: V_elec (3D, 552 nodes, 385 elements)
MultiStep 1: static, 1 steps 
 - 'elecFieldIntensity' (real) defined in 'V_air' on Elements
 - 'elecFieldIntensity' (real) defined in 'V_elec' on Elements
 - 'elecFieldIntensity' (real) defined in 'P0_elem' on Elements
 - 'elecFieldIntensity' (real) defined in 'P1_elem' on Elements
 - 'elecFieldIntensity' (real) defined in 'P2_elem' on Elements
 - 'elecFieldIntensity' (real) defined in 'P3_elem' on Elements
 - 'elecFluxDensity' (real) defined in 'V_air' on Elements
 - 'elecFluxDensity' (real) defined in 'V_elec' on Elements
 - 'elecPotential' (real) defined in 'V_air' on Nodes
 - 'elecPotential' (real) defined in 'V_elec' on Nodes
 - 'elecPotential' (real) defined in 'P0_node' on Nodes
 - 'elecPotential' (real) defined in 'P1_node' on Nodes
 - 'elecPotential' (real) defined in 'P2_node' on Nodes
 - 'elecPotential' (real) defined in 'P3_node' on Nodes
 - 'elecCharge' (real) defined in 'S_top' on ElementGroup
 - 'elecEnergy' (real) defined in 'V_air' on Regions
 - 'elecEnergy' (real) defined in 'V_elec' on Regions
"""

    assert ref_str in info_str


def test_file_info_multisteps(
    dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, dummy_CFSResultContainer_history_obj, working_directory="."
):
    file = f"{working_directory}/tests/data_tmp/io/test_file_info_multisteps.cfs"
    with io.CFSWriter(filename=file) as h5writer:
        h5writer.create_file(mesh=dummy_CFSMeshData_obj, result=dummy_CFSResultContainer_obj)
        h5writer.write_multistep(result=dummy_CFSResultContainer_history_obj, multi_step_id=2)

    with io.CFSReader(filename=file) as h5reader:
        info_str = str(h5reader)

    ref_str = """Mesh
 - Dimension: 3
 - Nodes:     8
 - Elements:  4
 - Regions:   3
   - Group : Surf2 (2D, 4 nodes, 1 elements)
   - Region: Surf1 (2D, 4 nodes, 2 elements)
   - Region: Vol (3D, 8 nodes, 1 elements)
MultiStep 1: transient, 5 steps 
 - 'quantity' (complex) defined in 'Vol' on Nodes
 - 'quantity3' (real) defined in 'Surf1' on Elements
MultiStep 2: undefined, 5 steps 
 - 'quantity' (complex) defined in 'Vol' on Regions
"""

    assert ref_str in info_str


def test_read_result_mixed_mesh_history(working_directory="."):
    file = f"{working_directory}/tests/data/io/result_mixed_mesh_history.cfs"

    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        result_data_mesh = h5reader.ResultMeshData
        result_data_history = h5reader.HistoryData

        result_data_all = h5reader.MultiStepData

    result_data_mesh.combine_with(result_data_history)

    assert result_data_all == result_data_mesh


def test_read_result_mixed_mesh_history_error_handling(
    dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, dummy_CFSResultContainer_history_obj, working_directory="."
):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_create_file(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory)

    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        res_all = h5reader.MultiStepData
        res_mesh = h5reader.ResultMeshData

    assert res_all == res_mesh

    file = f"{working_directory}/tests/data_tmp/pycfs_data_io_history.cfs"

    test_write_history(dummy_CFSMeshData_obj, dummy_CFSResultContainer_history_obj, working_directory)

    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        res_all = h5reader.MultiStepData
        res_hist = h5reader.HistoryData

    assert res_all == res_hist


def test_write_result_mixed_mesh_history(working_directory="."):
    file = f"{working_directory}/tests/data/io/result_mixed_mesh_history.cfs"
    file_out = f"{working_directory}/tests/data_tmp/io/result_mixed_mesh_history.cfs"

    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        mesh = h5reader.MeshData
        result = h5reader.MultiStepData

    with io.CFSWriter(file_out, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh=mesh, result=result)


def test_create_file(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh=dummy_CFSMeshData_obj, result=dummy_CFSResultContainer_obj)


def test_write_mesh(dummy_CFSMeshData_obj, working_directory="."):
    test_create_file(
        dummy_CFSMeshData_obj=dummy_CFSMeshData_obj,
        dummy_CFSResultContainer_obj=None,
        working_directory=working_directory,
    )


def test_write_mesh_result(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_write_mesh(dummy_CFSMeshData_obj, working_directory)

    print("Write mesh result to demo file")
    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.write_multistep(result=dummy_CFSResultContainer_obj)


def test_read_write_multistep2(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_create_file(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory)

    dummy_CFSResultContainer_obj2 = copy.deepcopy(dummy_CFSResultContainer_obj)
    dummy_CFSResultContainer_obj2.MultiStepID = 2
    dummy_CFSResultContainer_obj2.AnalysisType = cfs_analysis_type.HARMONIC

    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.write_multistep(result=dummy_CFSResultContainer_obj2, multi_step_id=2)

    with io.CFSReader(file, multistep_id=2, verbosity=v_def.all) as h5reader:
        np.testing.assert_equal(h5reader.ResultMeshData, dummy_CFSResultContainer_obj2)


def test_read_mesh(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_create_file(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory)

    print("Read demo file")
    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        # Read Mesh
        print("Read Demo Mesh")
        mesh_data_read = h5reader.MeshData
        reg_info_read_S2 = h5reader.get_mesh_region(region="Surf2", is_group=True)
        reg_info_read = h5reader.MeshGroupsRegions

        # Check Read Mesh Data
        print("Check Written/Read Mesh")
        print(f" - Mesh Info: {dummy_CFSMeshData_obj.MeshInfo == mesh_data_read.MeshInfo}")
        print(f" - Mesh Data: {dummy_CFSMeshData_obj == mesh_data_read}")
        for reg_read in reg_info_read:
            print(f" - Region {reg_read.Name}: {reg_read in dummy_CFSMeshData_obj.Regions}")

        np.testing.assert_equal(dummy_CFSMeshData_obj, mesh_data_read)


def test_read_data(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_create_file(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory)

    print("Read demo file")
    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        # Read Mesh
        print("Read Demo Mesh")
        mesh_data_read = h5reader.MeshData

        # Read Data
        np.testing.assert_equal(h5reader.ResultMeshData, dummy_CFSResultContainer_obj)

        node_id = h5reader.get_closest_node(coordinate=np.array([[0.1, 0, 0], [0, 0, 1]]), region="Vol")
        np.testing.assert_equal(
            mesh_data_read.get_closest_node(coordinate=np.array([[0.1, 0, 0], [0, 0, 1]]), region="Vol"), node_id
        )
        result_data_1 = [
            h5reader.get_single_data_steps(quantity="quantity", region="Vol", entity_id=node_id[i]) for i in node_id
        ]
        el_id = h5reader.get_closest_element(coordinate=np.array([[1, 1, 1], [0, 0, 0]]), region="Surf1")
        np.testing.assert_equal(
            mesh_data_read.get_closest_element(coordinate=np.array([[1, 1, 1], [0, 0, 0]]), region="Surf1"), el_id
        )
        result_data_1_3 = [
            h5reader.get_single_data_steps(quantity="quantity3", region="Surf1", entity_id=el_id[i]) for i in el_id
        ]


def test_read_data_sequential(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_create_file(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory)

    print("Read demo file")
    with io.CFSReader(file, processes=1, verbosity=v_def.all) as h5reader:
        # Read Mesh
        print("Read Demo Mesh")
        mesh_data_read = h5reader.MeshData

        # Read Data
        np.testing.assert_equal(h5reader.ResultMeshData, dummy_CFSResultContainer_obj)


def test_read_group_wo_elements(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    """Read group/region without elements (nodes only)."""

    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_create_file(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory)

    print("Delete Dataset /Mesh/Groups/")
    h5_path = f"Mesh/Regions/Surf1/Elements"
    with h5py.File(file, "r+") as f:
        del f[h5_path]

    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        mesh_data_read = h5reader.MeshData

    test_write_mesh(mesh_data_read, working_directory=working_directory)


def test_sort_result_data(dummy_CFSResultContainer_obj):
    # Write unsorted StepValues
    step_values = dummy_CFSResultContainer_obj.StepValues
    unsort_idx = np.arange(start=len(step_values) - 1, stop=-1, step=-1)
    step_values = step_values[unsort_idx]
    dummy_CFSResultContainer_obj.StepValues = step_values

    # Sort ResultData by StepValues
    sort_idx = dummy_CFSResultContainer_obj.sort_steps(return_idx=True)
    np.testing.assert_array_equal(sort_idx, unsort_idx)


def test_reorient(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    dummy_CFSMeshData_obj.reorient_region("Surf1")
    dummy_CFSMeshData_obj.reorient_region("Surf2")
    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh=dummy_CFSMeshData_obj, result=dummy_CFSResultContainer_obj)


def test_manipulate_result_data(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    result_data_extract = dummy_CFSResultContainer_obj.extract_quantity_region("quantity3", "Surf1")
    result_data_other = dummy_CFSResultContainer_obj.extract_quantity_region("quantity", "Vol")
    result_data_other_selection = result_data_other[[0, 2]]
    result_data_write = result_data_other.combine_with(result_data_extract)[1:3]
    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh=dummy_CFSMeshData_obj, result=result_data_write)


def test_remove_region(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj):
    print("Remove region and write reduced mesh and data")
    reg_info_keep = [dummy_CFSMeshData_obj.Regions[i] for i in [1, 2]]

    result_data_extract = dummy_CFSMeshData_obj.extract_regions(
        regions=reg_info_keep, result_data=dummy_CFSResultContainer_obj
    )

    dummy_CFSMeshData_obj.check_mesh()
    result_data_extract.check_result(dummy_CFSMeshData_obj)


def test_merge_meshes(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    print("Merge meshes")
    mesh_data_1 = copy.deepcopy(dummy_CFSMeshData_obj)
    mesh_data_2 = copy.deepcopy(dummy_CFSMeshData_obj)

    mesh_data_2.convert_quad2tria(idx_convert=np.array([3]))

    reg_info_1 = [mesh_data_1.Regions[i] for i in [0]]
    reg_info_2 = [mesh_data_2.Regions[i] for i in [2]]

    mesh_data_1.drop_unused_nodes_elements(reg_data_list=reg_info_1)
    mesh_data_2.drop_unused_nodes_elements(reg_data_list=reg_info_2)

    mesh_merged = mesh_data_1.merge(mesh_data_2)
    mesh_added = mesh_data_1 + mesh_data_2
    print(mesh_merged == mesh_added)

    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh=mesh_merged)


def test_convert_to_simplex(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    result = dummy_CFSMeshData_obj.convert_to_simplex(result_data=dummy_CFSResultContainer_obj)

    with io.CFSWriter(file, verbosity=v_def.all) as f:
        f.create_file(dummy_CFSMeshData_obj, result)


def test_drop_nodes_elements(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj):
    result_data = dummy_CFSMeshData_obj.drop_nodes_elements(
        node_idx=np.array([3]), el_idx=np.array([3]), result_data=dummy_CFSResultContainer_obj
    )

    dummy_CFSMeshData_obj.check_mesh()
    result_data.check_result(mesh=dummy_CFSMeshData_obj)


def test_extract_nodes_elements(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj):
    result_data = dummy_CFSMeshData_obj.extract_nodes_elements(
        node_idx=np.array([3]), el_idx=np.array([3]), result_data=dummy_CFSResultContainer_obj
    )

    dummy_CFSMeshData_obj.check_mesh()
    result_data.check_result(mesh=dummy_CFSMeshData_obj)


def test_extract_regions(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj):
    result_data = dummy_CFSMeshData_obj.extract_regions(
        regions=["Surf1", "Surf2"], result_data=dummy_CFSResultContainer_obj
    )

    dummy_CFSMeshData_obj.check_mesh()
    result_data.check_result(mesh=dummy_CFSMeshData_obj)

    ref_array = dummy_CFSResultContainer_obj.get_data_array(quantity="quantity3", region="Surf1")
    r_array = result_data.get_data_array(quantity="quantity3", region="Surf1")

    np.testing.assert_array_equal(ref_array, r_array)


def test_add_point_elements(dummy_CFSMeshData_obj):
    reg_to_add = io.CFSRegData(name="point_cloud", nodes=np.array([1, 2, 3]))
    dummy_CFSMeshData_obj.Regions.append(reg_to_add)
    dummy_CFSMeshData_obj.check_add_point_elements()

    dummy_CFSMeshData_obj.check_mesh()

    reg_added = dummy_CFSMeshData_obj.get_region(region="point_cloud")

    assert reg_added == reg_to_add

    conn_added = np.array(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0],
        ]
    )

    el_types_added = np.array([cfs_element_type.POINT for _ in range(reg_to_add.Elements.size)]).reshape(-1, 1)

    np.testing.assert_array_equal(conn_added, dummy_CFSMeshData_obj.Connectivity[-3:])
    np.testing.assert_array_equal(el_types_added, dummy_CFSMeshData_obj.Types[-3:])


def test_split_regions_by_connectivity(working_directory="."):
    """Read group/region without elements (nodes only)."""

    file = f"{working_directory}/tests/data/io/connected_regions.cfs"
    ref_file = f"{working_directory}/tests/data/io/disconnected_regions.cfs"

    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        mesh_data_read = h5reader.MeshData
        result_data_read = h5reader.ResultMeshData

    new_result_data = mesh_data_read.split_regions_by_connectivity(result_data=result_data_read, regions=["S_PSV"])

    mesh_data_read.check_mesh()
    new_result_data.check_result(mesh=mesh_data_read)

    # compare to reference file
    with io.CFSReader(ref_file, verbosity=v_def.all) as h5reader:
        mesh_data_ref = h5reader.MeshData
        result_data_ref = h5reader.ResultMeshData

    assert mesh_data_ref == mesh_data_read
    assert result_data_ref == new_result_data


def test_simple(dummy_CFSMeshData_obj, dummy_CFSResultContainer_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io_simple.cfs"

    res_list = [copy.deepcopy(dummy_CFSResultContainer_obj), copy.deepcopy(dummy_CFSResultContainer_obj)]
    res_dict = {1: copy.deepcopy(dummy_CFSResultContainer_obj), 3: copy.deepcopy(dummy_CFSResultContainer_obj)}
    res_dict[3].MultiStepID = 3

    # Test writing file
    io.write_file(file=file, mesh=dummy_CFSMeshData_obj, result=dummy_CFSResultContainer_obj)
    io.write_file(file=file, mesh=dummy_CFSMeshData_obj, result=dummy_CFSResultContainer_obj.Data)
    io.write_file(file=file, mesh=dummy_CFSMeshData_obj, result=copy.deepcopy(res_list))
    io.write_file(file=file, mesh=dummy_CFSMeshData_obj, result=copy.deepcopy(res_dict))

    # Test reading file
    mesh = io.read_mesh(file=file)
    assert mesh == dummy_CFSMeshData_obj

    result = io.read_data(file=file, multistep=1)
    assert result == dummy_CFSResultContainer_obj

    mesh, result = io.read_file(file=file)
    assert mesh == dummy_CFSMeshData_obj
    for mid in result:
        assert result[mid] == res_dict[mid]
