# The MIT License (MIT)
#
# Copyright (c) 2018-2025 MeshPy Authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""This module defines a global object that manages all kind of stuff regarding
meshpy."""

from enum import Enum as _Enum
from enum import auto as _auto


class Geometry(_Enum):
    """Enum for geometry types."""

    point = _auto()
    line = _auto()
    surface = _auto()
    volume = _auto()


class BoundaryCondition(_Enum):
    """Enum for boundary condition types."""

    dirichlet = _auto()
    neumann = _auto()
    locsys = _auto()
    moment_euler_bernoulli = _auto()
    beam_to_beam_contact = _auto()
    beam_to_solid_volume_meshtying = _auto()
    beam_to_solid_surface_meshtying = _auto()
    beam_to_solid_surface_contact = _auto()
    point_coupling = _auto()
    point_coupling_penalty = _auto()


class BeamType(_Enum):
    """Enum for beam types."""

    reissner = _auto()
    kirchhoff = _auto()
    euler_bernoulli = _auto()


class CouplingDofType(_Enum):
    """Enum for coupling types."""

    fix = _auto()
    joint = _auto()


class BeamToSolidInteractionType(_Enum):
    """Enum for beam-to-solid interaction types."""

    volume_meshtying = _auto()
    surface_meshtying = _auto()


class DoubleNodes(_Enum):
    """Enum for handing double nodes in Neumann conditions."""

    remove = _auto()
    keep = _auto()


class GeometricSearchAlgorithm(_Enum):
    """Enum for VTK value types."""

    automatic = _auto()
    brute_force_cython = _auto()
    binning_cython = _auto()
    boundary_volume_hierarchy_arborx = _auto()


class VTKGeometry(_Enum):
    """Enum for VTK geometry types (for now cells and points)."""

    point = _auto()
    cell = _auto()


class VTKTensor(_Enum):
    """Enum for VTK tensor types."""

    scalar = _auto()
    vector = _auto()


class VTKType(_Enum):
    """Enum for VTK value types."""

    int = _auto()
    float = _auto()


class MeshPy(object):
    """A global object that stores options for the whole MeshPy application."""

    def __init__(self):
        self.set_default_values()

        # Geometry types.
        self.geo = Geometry

        # Boundary conditions types.
        self.bc = BoundaryCondition

        # Beam types.
        self.beam = BeamType

        # Beam-to-solid interaction types.
        self.beam_to_solid = BeamToSolidInteractionType

        # Coupling types.
        self.coupling_dof = CouplingDofType

        # Handling of multiple nodes in Neumann bcs.
        self.double_nodes = DoubleNodes

        # Geometric search options.
        self.geometric_search_algorithm = GeometricSearchAlgorithm

        # VTK types.
        # Geometry types, cell or point.
        self.vtk_geo = VTKGeometry
        # Tensor types, scalar or vector.
        self.vtk_tensor = VTKTensor
        # Data types, integer or float.
        self.vtk_type = VTKType

    def set_default_values(self):
        """Set the configuration to the default values."""

        # Set the epsilons for comparison of different types of values.
        self.eps_quaternion = 1e-10
        self.eps_pos = 1e-10
        self.eps_knot_vector = 1e-10

        # Allow the rotation of beams when connected and the triads do not
        # match.
        self.allow_beam_rotation = True

        # Import meshes as pure dict or import the geometry.
        self.import_mesh_full = False

        # Number of digits for node set output (this will be set in the
        # Mesh.get_unique_geometry_sets() method.
        self.vtk_node_set_format = "{:05}"
        # Nan values for vtk data, since we currently can't set nan explicitly.
        self.vtk_nan_int = -1
        self.vtk_nan_float = 0.0

        # Check for overlapping elements when creating an input file.
        self.check_overlapping_elements = True

        # Lines to be added to each created input file
        self.input_file_meshpy_header = [
            "-" * 40,
            "This input file was created with MeshPy.",
            "Copyright (c) 2018-2025 MeshPy Authors",
            "https://imcs-compsim.github.io/meshpy/",
            "-" * 40,
        ]


mpy = MeshPy()
