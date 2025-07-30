"""
Tutorial for using the Exodus Reader.

- Read Exodus file and convert it to cfs mesh
- Write mesh to cfs file
"""

# Import Exodus reader and CFS writer
from pyCFS.data.extras.exodus_io import read_exodus
from pyCFS.data.io import CFSWriter

# Read mesh from Exodus file and convert it to cfs mesh
file_read = "beam2D.e"
cfs_mesh = read_exodus(file_read)

# Write mesh to cfs file
file_write = "beam2D.cfs"
with CFSWriter(file_write) as f:
    f.create_file(mesh=cfs_mesh)
