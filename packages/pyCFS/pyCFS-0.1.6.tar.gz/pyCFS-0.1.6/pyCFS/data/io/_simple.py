"""
pyCFS.data.io._top_level

Top-level functions for reading and writing CFS files.
"""

from typing import List, Dict, Optional, Sequence

from pyCFS.data.io import CFSReader, CFSMeshData, CFSResultContainer, CFSResultArray, CFSWriter


def read_mesh(file: str):
    """
    Read a mesh from a CFS file.

    Parameters
    ----------
    file : str
        Path to the CFS file.

    Returns
    -------
    tuple
        A tuple containing the mesh data and region data.

    Examples
    --------
    >>> from pyCFS.data.io import read_mesh
    >>> mesh = read_mesh(file="file.cfs")
    """
    with CFSReader(file) as f:
        mesh = f.MeshData

    return mesh


def read_data(file: str, multistep=1):
    """
    Read result data from a CFS file.

    Parameters
    ----------
    file : str
        Path to the CFS file.
    multistep : int, optional
        Multi-step ID to read (default is 1).

    Returns
    -------
    tuple
        A tuple containing the mesh data and result data.

    Examples
    --------
    >>> from pyCFS.data.io import read_data
    >>> result = read_data(file="file.cfs", multistep=1)
    """
    with CFSReader(file) as f:
        res = f.get_multi_step_data(multi_step_id=multistep)

    return res


def read_file(file: str):
    """
    Read a CFS file and return the mesh and result data for all multi-steps.

    Parameters
    ----------
    file : str
        Path to the CFS file.

    Returns
    -------
    tuple[CFSMeshData, dict[int, CFSResultContainer]]
        A tuple containing the mesh data and a dictionary mapping multi-step IDs to result data.

    Examples
    --------
    >>> from pyCFS.data.io import read_file
    >>> mesh, result = read_file(file="file.cfs")
    """

    res_dict = {}
    with CFSReader(file) as f:
        mesh = f.MeshData
        for mid in f.MultiStepIDs:
            res_dict[mid] = f.get_multi_step_data(multi_step_id=mid)

    return mesh, res_dict


def write_file(
    file: str,
    mesh: Optional[CFSMeshData] = None,
    result: (
        Dict[int, CFSResultContainer] | List[CFSResultContainer] | CFSResultContainer | List[CFSResultArray] | None
    ) = None,
):
    """
    Write mesh and result data to a CFS file.

    Parameters
    ----------
    file : str
        Path to the CFS file to write.
    mesh : CFSMeshData, optional
        Mesh data to write to the file. If None, only result data is written (if provided).
    result : dict[int, CFSResultContainer] or list[CFSResultContainer] or CFSResultContainer or list[CFSResultArray], optional
        Result data to write.
        Can be a dictionary mapping multi-step IDs to result containers, a list of result containers,
        a single result container, or a list of result arrays. If None, only mesh data is written (if provided).

    Examples
    --------
    >>> from pyCFS.data.io import write_file
    >>> write_file(file="file.cfs", mesh=mesh)
    >>> write_file(file="file.cfs", mesh=mesh, result=result)
    >>> write_file(file="file.cfs", mesh=mesh, result={1: result_1, 2: result_2})
    >>> write_file(file="file.cfs", mesh=mesh, result=[result_1, result_2])
    """
    with CFSWriter(file) as f:
        f.create_file(mesh=mesh)

        if isinstance(result, dict):
            for mid in result:
                f.write_multistep(result=result[mid], multi_step_id=mid)
        elif isinstance(result, Sequence) and all([isinstance(item, CFSResultContainer) for item in result]):
            for midx, item in enumerate(result):
                f.write_multistep(result=item, multi_step_id=midx + 1)
        elif isinstance(result, CFSResultContainer) or (
            isinstance(result, Sequence) and all([isinstance(item, CFSResultArray) for item in result])
        ):
            f.write_multistep(result=result, multi_step_id=1)
