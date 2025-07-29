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
"""This script is used to test the functionality of the meshpy module."""

import os
import random
import warnings

import autograd.numpy as npAD
import numpy as np
import pytest
import vtk

from meshpy.core.boundary_condition import BoundaryCondition
from meshpy.core.conf import mpy
from meshpy.core.coupling import Coupling
from meshpy.core.element_beam import Beam
from meshpy.core.geometry_set import GeometryName, GeometrySet, GeometrySetNodes
from meshpy.core.material import MaterialBeam
from meshpy.core.mesh import Mesh
from meshpy.core.node import Node, NodeCosserat
from meshpy.core.rotation import Rotation
from meshpy.core.vtk_writer import VTKWriter
from meshpy.four_c.element_beam import (
    Beam3eb,
    Beam3k,
    Beam3rHerm2Line3,
    Beam3rLine2Line2,
)
from meshpy.four_c.function import Function
from meshpy.four_c.header_functions import (
    add_result_description,
    set_beam_to_solid_meshtying,
    set_header_static,
    set_runtime_output,
)
from meshpy.four_c.input_file import InputFile
from meshpy.four_c.material import (
    MaterialEulerBernoulli,
    MaterialKirchhoff,
    MaterialReissner,
    MaterialReissnerElastoplastic,
    MaterialStVenantKirchhoff,
)
from meshpy.mesh_creation_functions.beam_basic_geometry import (
    create_beam_mesh_arc_segment_via_rotation,
    create_beam_mesh_line,
)
from meshpy.mesh_creation_functions.beam_curve import create_beam_mesh_curve
from meshpy.mesh_creation_functions.beam_honeycomb import create_beam_mesh_honeycomb
from meshpy.utils.nodes import (
    get_min_max_coordinates,
    get_single_node,
)


def create_test_mesh(mesh):
    """Fill the mesh with a couple of test nodes and elements."""

    # Set the seed for the pseudo random numbers
    random.seed(0)

    # Add material to mesh.
    material = MaterialReissner()
    mesh.add(material)

    # Add three test nodes and add them to a beam element
    for _j in range(3):
        mesh.add(
            NodeCosserat(
                [100 * random.uniform(-1, 1) for _i in range(3)],
                Rotation(
                    [100 * random.uniform(-1, 1) for _i in range(3)],
                    100 * random.uniform(-1, 1),
                ),
            )
        )
    beam = Beam3rHerm2Line3(material=material, nodes=mesh.nodes)
    mesh.add(beam)

    # Add a beam line with three elements
    create_beam_mesh_line(
        mesh,
        Beam3rHerm2Line3,
        material,
        [100 * random.uniform(-1, 1) for _i in range(3)],
        [100 * random.uniform(-1, 1) for _i in range(3)],
        n_el=3,
    )


def test_meshpy_rotations(assert_results_equal):
    """Check if the Mesh function rotation gives the same results as rotating
    each node it self."""

    mesh_1 = InputFile()
    create_test_mesh(mesh_1)

    mesh_2 = InputFile()
    create_test_mesh(mesh_2)

    # Set the seed for the pseudo random numbers
    random.seed(0)
    rot = Rotation(
        [100 * random.uniform(-1, 1) for _i in range(3)],
        100 * random.uniform(-1, 1),
    )
    origin = [100 * random.uniform(-1, 1) for _i in range(3)]

    for node in mesh_1.nodes:
        node.rotate(rot, origin=origin)

    mesh_2.rotate(rot, origin=origin)

    # Compare the output for the two meshes.
    assert_results_equal(mesh_1, mesh_2)


def test_meshpy_mesh_rotations_individual(assert_results_equal):
    """Check if the Mesh function rotation gives the same results as rotating
    each node it self, when an array is passed with different rotations."""

    mesh_1 = InputFile()
    create_test_mesh(mesh_1)

    mesh_2 = InputFile()
    create_test_mesh(mesh_2)

    # Set the seed for the pseudo random numbers
    random.seed(0)

    # Rotate each node with a different rotation
    rotations = np.zeros([len(mesh_1.nodes), 4])
    origin = [100 * random.uniform(-1, 1) for _i in range(3)]
    for j, node in enumerate(mesh_1.nodes):
        rot = Rotation(
            [100 * random.uniform(-1, 1) for _i in range(3)],
            100 * random.uniform(-1, 1),
        )
        rotations[j, :] = rot.get_quaternion()
        node.rotate(rot, origin=origin)

    mesh_2.rotate(rotations, origin=origin)

    # Compare the output for the two meshes.
    assert_results_equal(mesh_1, mesh_2)


@pytest.mark.parametrize("origin", [False, True])
@pytest.mark.parametrize("flip", [False, True])
def test_meshpy_mesh_reflection(origin, flip, assert_results_equal):
    """Create a mesh, and its mirrored counterpart and then compare the input
    files."""

    # Rotations to be applied.
    rot_1 = Rotation([0, 1, 1], np.pi / 6)
    rot_2 = Rotation([1, 2.455, -1.2324], 1.2342352)

    mesh_ref = InputFile()
    mesh = InputFile()
    mat = MaterialReissner(radius=0.1)

    # Create the reference mesh.
    if not flip:
        create_beam_mesh_line(
            mesh_ref, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0], n_el=1
        )
        create_beam_mesh_line(
            mesh_ref, Beam3rHerm2Line3, mat, [1, 0, 0], [1, 1, 0], n_el=1
        )
        create_beam_mesh_line(
            mesh_ref, Beam3rHerm2Line3, mat, [1, 1, 0], [1, 1, 1], n_el=1
        )
    else:
        create_beam_mesh_line(
            mesh_ref, Beam3rHerm2Line3, mat, [1, 0, 0], [0, 0, 0], n_el=1
        )
        create_beam_mesh_line(
            mesh_ref, Beam3rHerm2Line3, mat, [1, 1, 0], [1, 0, 0], n_el=1
        )
        create_beam_mesh_line(
            mesh_ref, Beam3rHerm2Line3, mat, [1, 1, 1], [1, 1, 0], n_el=1
        )

        # Reorder the internal nodes.
        old = mesh_ref.nodes.copy()
        mesh_ref.nodes[0] = old[2]
        mesh_ref.nodes[2] = old[0]
        mesh_ref.nodes[3] = old[5]
        mesh_ref.nodes[5] = old[3]
        mesh_ref.nodes[6] = old[8]
        mesh_ref.nodes[8] = old[6]

    mesh_ref.rotate(rot_1)

    # Create the mesh that will be mirrored.
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [-1, 0, 0], n_el=1)
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [-1, 0, 0], [-1, 1, 0], n_el=1)
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [-1, 1, 0], [-1, 1, 1], n_el=1)
    mesh.rotate(rot_1.inv())

    # Rotate everything, to show generalized reflection.
    mesh_ref.rotate(rot_2)
    mesh.rotate(rot_2)

    if origin:
        # Translate everything so the reflection plane is not in the
        # origin.
        r = [1, 2.455, -1.2324]
        mesh_ref.translate(r)
        mesh.translate(r)
        mesh.reflect(2 * (rot_2 * [1, 0, 0]), origin=r, flip_beams=flip)
    else:
        mesh.reflect(2 * (rot_2 * [1, 0, 0]), flip_beams=flip)

    # Compare the input files.
    # TODO: Also add fixed result files to compare the tests with
    assert_results_equal(mesh_ref, mesh)


@pytest.mark.parametrize("full_import", [[True, "full"], [False, None]])
def test_meshpy_comments_in_solid(
    get_bc_data,
    assert_results_equal,
    get_corresponding_reference_file_path,
    full_import,
):
    """Check if comments in the solid file are handled correctly if they are
    inside a mesh section."""

    # Convert the solid mesh to meshpy objects.
    mpy.import_mesh_full = full_import[0]
    solid_file = get_corresponding_reference_file_path(additional_identifier="initial")
    mesh = InputFile(yaml_file=solid_file)

    # Add one element with BCs.
    mat = MaterialReissner()
    sets = create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 2, 3])
    mesh.add(
        BoundaryCondition(
            sets["start"], get_bc_data(identifier=1), bc_type=mpy.bc.dirichlet
        )
    )
    mesh.add(
        BoundaryCondition(
            sets["end"], get_bc_data(identifier=2), bc_type=mpy.bc.neumann
        )
    )

    # Compare the output of the mesh.
    assert_results_equal(get_corresponding_reference_file_path(), mesh)


def test_meshpy_mesh_transformations_with_solid(
    assert_results_equal,
    get_corresponding_reference_file_path,
):
    """Test the different mesh transformation methods in combination with solid
    elements."""

    def base_test_mesh_translations(*, import_full=False, radius=None, reflect=True):
        """Create the line and wrap it with passing radius to the wrap
        function."""

        # Set if we want to do a full import or not
        mpy.import_mesh_full = import_full

        # Create the mesh.
        mesh = InputFile(
            yaml_file=get_corresponding_reference_file_path(
                reference_file_base_name="4C_input_solid_cuboid"
            )
        )
        mat = MaterialReissner(radius=0.05)

        # Create the line.
        create_beam_mesh_line(
            mesh,
            Beam3rHerm2Line3,
            mat,
            [0.2, 0, 0],
            [0.2, 5 * 0.2 * 2 * np.pi, 4],
            n_el=3,
        )

        # Transform the mesh.
        mesh.wrap_around_cylinder(radius=radius)
        mesh.translate([1, 2, 3])
        mesh.rotate(Rotation([1, 2, 3], np.pi * 17.0 / 27.0))
        if reflect:
            mesh.reflect([0.1, -2, 1])

        # Check the output.
        assert_results_equal(
            get_corresponding_reference_file_path(
                additional_identifier="full" if import_full else "yaml"
            ),
            mesh,
        )

    base_test_mesh_translations(import_full=False, radius=None)
    base_test_mesh_translations(import_full=False, radius=0.2)
    base_test_mesh_translations(import_full=True, radius=0.2, reflect=False)

    # Not specifying or specifying the wrong radius should raise an error
    # In this case because everything is on one plane ("no" solid nodes in this case)
    # and we specify the radius
    with pytest.raises(ValueError):
        base_test_mesh_translations(import_full=False, radius=666, reflect=False)

    # In this case because we need to specify a radius because with the solid nodes there
    # is no clear radius
    with pytest.raises(ValueError):
        base_test_mesh_translations(
            import_full=True,
            radius=None,
            reflect=False,
        )


def test_meshpy_fluid_element_section(
    assert_results_equal,
    get_corresponding_reference_file_path,
):
    """Add beam elements to an input file containing fluid elements."""
    input_file = InputFile(
        yaml_file=get_corresponding_reference_file_path(additional_identifier="import")
    )

    beam_mesh = Mesh()
    material = MaterialEulerBernoulli(youngs_modulus=1e8, radius=0.001, density=10)
    beam_mesh.add(material)

    create_beam_mesh_line(
        beam_mesh, Beam3eb, material, [0, -0.5, 0], [0, 0.2, 0], n_el=5
    )
    input_file.add(beam_mesh)

    # Check the output.
    assert_results_equal(get_corresponding_reference_file_path(), input_file)


def test_meshpy_wrap_cylinder_not_on_same_plane(
    assert_results_equal, get_corresponding_reference_file_path
):
    """Create a helix that is itself wrapped around a cylinder."""

    # Ignore the warnings from wrap around cylinder.
    warnings.filterwarnings("ignore")

    # Create the mesh.
    mesh = InputFile()
    mat = MaterialReissner(radius=0.05)

    # Create the line and bend it to a helix.
    create_beam_mesh_line(
        mesh,
        Beam3rHerm2Line3,
        mat,
        [0.2, 0, 0],
        [0.2, 5 * 0.2 * 2 * np.pi, 4],
        n_el=20,
    )
    mesh.wrap_around_cylinder()

    # Move the helix so its axis is in the y direction and goes through
    # (2 0 0). The helix is also moved by a lot in y-direction, this only
    # affects the angle phi when wrapping around a cylinder, not the shape
    # of the beam.
    mesh.rotate(Rotation([1, 0, 0], -0.5 * np.pi))
    mesh.translate([2, 666.666, 0])

    # Wrap the helix again.
    mesh.wrap_around_cylinder(radius=2.0)

    # Check the output.
    assert_results_equal(get_corresponding_reference_file_path(), mesh)


def test_meshpy_get_nodes_by_function():
    """Check if the get_nodes_by_function method of Mesh works properly."""

    def get_nodes_at_x(node, x_value):
        """True for all coordinates at a certain x value."""
        if np.abs(node.coordinates[0] - x_value) < 1e-10:
            return True
        else:
            return False

    mat = MaterialReissner()

    mesh = Mesh()
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [5, 0, 0], n_el=5)
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 1, 0], [10, 1, 0], n_el=10)

    nodes = mesh.get_nodes_by_function(get_nodes_at_x, 1.0)
    assert 2 == len(nodes)
    for node in nodes:
        assert np.abs(1.0 - node.coordinates[0]) < 1e-10


def test_meshpy_get_min_max_coordinates(get_corresponding_reference_file_path):
    """Test if the get_min_max_coordinates function works properly."""

    # Create the mesh.
    mpy.import_mesh_full = True
    mesh = InputFile(
        yaml_file=get_corresponding_reference_file_path(
            reference_file_base_name="4C_input_solid_cuboid"
        )
    )
    mat = MaterialReissner(radius=0.05)
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [2, 3, 4], n_el=10)

    # Check the results.
    min_max = get_min_max_coordinates(mesh.nodes)
    ref_solution = [-0.5, -1.0, -1.5, 2.0, 3.0, 4.0]
    assert np.linalg.norm(min_max - ref_solution) < 1e-10


def test_meshpy_geometry_sets(
    assert_results_equal, get_corresponding_reference_file_path
):
    """Test functionality of the GeometrySet objects."""

    mesh = InputFile()
    for i in range(6):
        mesh.add(NodeCosserat([i, 2 * i, 3 * i], Rotation()))

    set_1 = GeometrySetNodes(
        mpy.geo.point, [mesh.nodes[0], mesh.nodes[1], mesh.nodes[2]]
    )
    set_2 = GeometrySetNodes(
        mpy.geo.point, [mesh.nodes[2], mesh.nodes[3], mesh.nodes[4]]
    )
    set_12 = GeometrySetNodes(mpy.geo.point)
    set_12.add(set_1)
    set_12.add(set_2)
    set_3 = GeometrySet(set_1.get_points())

    mesh.add(set_1, set_2, set_12, set_3)

    # Check the output.
    assert_results_equal(get_corresponding_reference_file_path(), mesh)


def test_meshpy_unique_ordering_of_get_all_nodes_for_line_condition(
    get_bc_data, assert_results_equal, get_corresponding_reference_file_path
):
    """This test ensures that the ordering of the nodes returned from the
    function get_all_nodes is unique for line sets."""

    # set up a beam mesh with material
    input_file = InputFile()
    mat = MaterialReissner()
    beam_set = create_beam_mesh_line(
        input_file, Beam3rHerm2Line3, mat, [0, 0, 0], [2, 0, 0], n_el=10
    )

    # apply different Dirichlet conditions to all nodes within this condition
    for i, node in enumerate(beam_set["line"].get_all_nodes()):
        # add different condition value for each node
        input_file.add(
            BoundaryCondition(
                GeometrySet(node),
                get_bc_data(identifier=node.coordinates[0]),
                bc_type=mpy.bc.dirichlet,
            )
        )

    # Check the input file
    assert_results_equal(
        get_corresponding_reference_file_path(),
        input_file,
    )


def test_meshpy_reissner_beam(
    assert_results_equal, get_corresponding_reference_file_path
):
    """Test that the input file for all types of Reissner beams is generated
    correctly."""

    # Create input file.
    material = MaterialReissner(radius=0.1, youngs_modulus=1000, interaction_radius=2.0)
    input_file = InputFile()

    # Create a beam arc with the different Reissner beam types.
    for i, beam_type in enumerate([Beam3rHerm2Line3, Beam3rLine2Line2]):
        create_beam_mesh_arc_segment_via_rotation(
            input_file,
            beam_type,
            material,
            [0.0, 0.0, i],
            Rotation([0.0, 0.0, 1.0], np.pi / 2.0),
            2.0,
            np.pi / 2.0,
            n_el=2,
        )

    # Compare with the reference solution.
    assert_results_equal(get_corresponding_reference_file_path(), input_file)


def test_meshpy_reissner_elasto_plastic(assert_results_equal):
    """Test the elasto plastic Reissner beam material."""

    kwargs = {
        "radius": 0.1,
        "youngs_modulus": 1000,
        "interaction_radius": 2.0,
        "shear_correction": 5.0 / 6.0,
        "yield_moment": 2.3,
        "isohardening_modulus_moment": 4.5,
        "torsion_plasticity": False,
    }

    ref_dict = {
        "MAT": 69,
        "MAT_BeamReissnerElastPlastic": {
            "YOUNG": 1000,
            "POISSONRATIO": 0.0,
            "DENS": 0.0,
            "CROSSAREA": 0.031415926535897934,
            "SHEARCORR": 0.8333333333333334,
            "MOMINPOL": 0.00015707963267948968,
            "MOMIN2": 7.853981633974484e-05,
            "MOMIN3": 7.853981633974484e-05,
            "INTERACTIONRADIUS": 2.0,
            "YIELDM": 2.3,
            "ISOHARDM": 4.5,
            "TORSIONPLAST": False,
        },
    }

    mat = MaterialReissnerElastoplastic(**kwargs)
    mat.i_global = 69
    assert_results_equal(mat.dump_to_list(), [ref_dict])

    ref_dict["MAT_BeamReissnerElastPlastic"]["TORSIONPLAST"] = True
    kwargs["torsion_plasticity"] = True
    mat = MaterialReissnerElastoplastic(**kwargs)
    mat.i_global = 69
    assert_results_equal(mat.dump_to_list(), [ref_dict])


def test_meshpy_kirchhoff_beam(
    assert_results_equal, get_corresponding_reference_file_path
):
    """Test that the input file for all types of Kirchhoff beams is generated
    correctly."""

    # Create input file.
    input_file = InputFile()

    with warnings.catch_warnings():
        # Ignore the warnings for the rotvec beams.
        warnings.simplefilter("ignore")

        # Loop over options.
        for is_fad in (True, False):
            material = MaterialKirchhoff(radius=0.1, youngs_modulus=1000, is_fad=is_fad)
            for weak in (True, False):
                for rotvec in (True, False):
                    # Define the beam object factory function for the
                    # creation functions.
                    BeamObject = Beam3k(weak=weak, rotvec=rotvec, is_fad=is_fad)

                    # Create a beam.
                    set_1 = create_beam_mesh_line(
                        input_file,
                        BeamObject,
                        material,
                        [0, 0, 0],
                        [1, 0, 0],
                        n_el=2,
                    )
                    set_2 = create_beam_mesh_line(
                        input_file,
                        BeamObject,
                        material,
                        [1, 0, 0],
                        [2, 0, 0],
                        n_el=2,
                    )

                    # Couple the nodes.
                    if rotvec:
                        input_file.couple_nodes(
                            nodes=[
                                get_single_node(set_1["end"]),
                                get_single_node(set_2["start"]),
                            ]
                        )

                    # Move the mesh away from the next created beam.
                    input_file.translate([0, 0.5, 0])

    # Compare with the reference solution.
    assert_results_equal(get_corresponding_reference_file_path(), input_file)


def test_meshpy_kirchhoff_material(assert_results_equal):
    """Test the Kirchhoff Love beam material."""

    def set_stiff(material):
        """Set the material properties for the beam material."""
        material.area = 2.0
        material.mom2 = 3.0
        material.mom3 = 4.0
        material.polar = 5.0

    material = MaterialKirchhoff(youngs_modulus=1000, is_fad=True)
    set_stiff(material)
    assert_results_equal(
        material.dump_to_list(),
        [
            {
                "MAT": None,
                "MAT_BeamKirchhoffElastHyper": {
                    "YOUNG": 1000,
                    "SHEARMOD": 500.0,
                    "DENS": 0.0,
                    "CROSSAREA": 2.0,
                    "MOMINPOL": 5.0,
                    "MOMIN2": 3.0,
                    "MOMIN3": 4.0,
                    "FAD": True,
                },
            }
        ],
    )

    material = MaterialKirchhoff(youngs_modulus=1000, is_fad=False)
    set_stiff(material)
    assert_results_equal(
        material.dump_to_list(),
        [
            {
                "MAT": None,
                "MAT_BeamKirchhoffElastHyper": {
                    "YOUNG": 1000,
                    "SHEARMOD": 500.0,
                    "DENS": 0.0,
                    "CROSSAREA": 2.0,
                    "MOMINPOL": 5.0,
                    "MOMIN2": 3.0,
                    "MOMIN3": 4.0,
                    "FAD": False,
                },
            }
        ],
    )

    material = MaterialKirchhoff(youngs_modulus=1000, interaction_radius=1.1)
    set_stiff(material)
    assert_results_equal(
        material.dump_to_list(),
        [
            {
                "MAT": None,
                "MAT_BeamKirchhoffElastHyper": {
                    "YOUNG": 1000,
                    "SHEARMOD": 500.0,
                    "DENS": 0.0,
                    "CROSSAREA": 2.0,
                    "MOMINPOL": 5.0,
                    "MOMIN2": 3.0,
                    "MOMIN3": 4.0,
                    "FAD": False,
                    "INTERACTIONRADIUS": 1.1,
                },
            }
        ],
    )


def test_meshpy_euler_bernoulli(
    assert_results_equal, get_corresponding_reference_file_path
):
    """Recreate the 4C test case beam3eb_static_endmoment_quartercircle.4C.yaml
    This tests the implementation for Euler Bernoulli beams."""

    # Create the input file and add function and material.
    input_file = InputFile()
    fun = Function([{"COMPONENT": 0, "SYMBOLIC_FUNCTION_OF_SPACE_TIME": "t"}])
    input_file.add(fun)
    mat = MaterialEulerBernoulli(youngs_modulus=1.0, density=1.3e9)

    # Set the parameters that are also set in the test file.
    mat.area = 1
    mat.mom2 = 1e-4

    # Create the beam.
    beam_set = create_beam_mesh_line(
        input_file, Beam3eb, mat, [-1, 0, 0], [1, 0, 0], n_el=16
    )

    # Add boundary conditions.
    input_file.add(
        BoundaryCondition(
            beam_set["start"],
            {
                "NUMDOF": 6,
                "ONOFF": [1, 1, 1, 0, 1, 1],
                "VAL": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "FUNCT": [0, 0, 0, 0, 0, 0],
            },
            bc_type=mpy.bc.dirichlet,
        )
    )
    input_file.add(
        BoundaryCondition(
            beam_set["end"],
            {
                "NUMDOF": 6,
                "ONOFF": [0, 0, 0, 0, 0, 1],
                "VAL": [0.0, 0.0, 0.0, 0.0, 0.0, 7.8539816339744e-05],
                "FUNCT": [0, 0, 0, 0, 0, fun],
            },
            bc_type=mpy.bc.moment_euler_bernoulli,
        )
    )

    # Compare with the reference solution.
    assert_results_equal(get_corresponding_reference_file_path(), input_file)

    # Test consistency checks.
    rot = Rotation([1, 2, 3], 2.3434)
    input_file.nodes[-1].rotation = rot
    with pytest.raises(
        ValueError,
        match="The two nodal rotations in Euler Bernoulli beams must be the same",
    ):
        # This raises an error because not all rotation in the beams are
        # the same.
        input_file.get_dict_to_dump()

    for node in input_file.nodes:
        node.rotation = rot
    with pytest.raises(
        ValueError,
        match="The rotations do not match the direction of the Euler Bernoulli beam",
    ):
        # This raises an error because the rotations do not match the
        # director between the nodes.
        input_file.get_dict_to_dump()


def test_meshpy_close_beam(assert_results_equal, get_corresponding_reference_file_path):
    """
    Create a circle with different methods.
    - Create the mesh manually by creating the nodes and connecting them to
        the elements.
    - Create one full circle and connect it to its beginning.
    - Create two half circle and connect their start / end nodes.
    All of those methods should give the exact same mesh.
    Both variants are also tried with different rotations at the beginning.
    """

    # Parameters for this test case.
    n_el = 3
    R = 1.235
    additional_rotation = Rotation([0, 1, 0], 0.5)

    # Define material.
    mat = MaterialReissner(radius=0.1)

    def create_mesh_manually(start_rotation):
        """Create the full circle manually."""
        input_file = InputFile()
        input_file.add(mat)

        # Add nodes.
        for i in range(4 * n_el):
            basis = start_rotation * Rotation([0, 0, 1], np.pi * 0.5)
            r = [R, 0, 0]
            node = NodeCosserat(r, basis)
            rotation = Rotation([0, 0, 1], 0.5 * i * np.pi / n_el)
            node.rotate(rotation, origin=[0, 0, 0])
            input_file.nodes.append(node)

        # Add elements.
        for i in range(2 * n_el):
            node_index = [2 * i, 2 * i + 1, 2 * i + 2]
            nodes = []
            for index in node_index:
                if index == len(input_file.nodes):
                    nodes.append(input_file.nodes[0])
                else:
                    nodes.append(input_file.nodes[index])
            element = Beam3rHerm2Line3(mat, nodes)
            input_file.add(element)

        # Add sets.
        geom_set = GeometryName()
        geom_set["start"] = GeometrySet(input_file.nodes[0])
        geom_set["end"] = GeometrySet(input_file.nodes[0])
        geom_set["line"] = GeometrySet(input_file.elements)
        input_file.add(geom_set)
        return input_file

    def one_full_circle_closed(function, argument_list, additional_rotation=None):
        """Create one full circle and connect it to itself."""

        input_file = InputFile()

        if additional_rotation is not None:
            start_rotation = additional_rotation * Rotation([0, 0, 1], np.pi * 0.5)
            input_file.add(NodeCosserat([R, 0, 0], start_rotation))
            beam_sets = function(
                input_file,
                start_node=input_file.nodes[0],
                close_beam=True,
                **(argument_list),
            )
        else:
            beam_sets = function(input_file, close_beam=True, **(argument_list))
        input_file.add(beam_sets)
        return input_file

    def two_half_circles_closed(function, argument_list, additional_rotation=None):
        """Create two half circles and close them, by reusing the connecting
        nodes."""

        input_file = InputFile()

        if additional_rotation is not None:
            start_rotation = additional_rotation * Rotation([0, 0, 1], np.pi * 0.5)
            input_file.add(NodeCosserat([R, 0, 0], start_rotation))
            set_1 = function(
                input_file, start_node=input_file.nodes[0], **(argument_list[0])
            )
        else:
            set_1 = function(input_file, **(argument_list[0]))

        set_2 = function(
            input_file,
            start_node=set_1["end"],
            end_node=set_1["start"],
            **(argument_list[1]),
        )

        # Add sets.
        geom_set = GeometryName()
        geom_set["start"] = GeometrySet(set_1["start"])
        geom_set["end"] = GeometrySet(set_2["end"])
        geom_set["line"] = GeometrySet([set_1["line"], set_2["line"]])
        input_file.add(geom_set)

        return input_file

    def get_arguments_arc_segment(circle_type):
        """Return the arguments for the arc segment function."""
        if circle_type == 0:
            # Full circle.
            arg_rot_angle = np.pi / 2
            arg_angle = 2 * np.pi
            arg_n_el = 2 * n_el
        elif circle_type == 1:
            # First half circle.
            arg_rot_angle = np.pi / 2
            arg_angle = np.pi
            arg_n_el = n_el
        elif circle_type == 2:
            # Second half circle.
            arg_rot_angle = 3 * np.pi / 2
            arg_angle = np.pi
            arg_n_el = n_el
        return {
            "beam_class": Beam3rHerm2Line3,
            "material": mat,
            "center": [0, 0, 0],
            "axis_rotation": Rotation([0, 0, 1], arg_rot_angle),
            "radius": R,
            "angle": arg_angle,
            "n_el": arg_n_el,
        }

    def circle_function(t):
        """Function for the circle."""
        return R * npAD.array([npAD.cos(t), npAD.sin(t)])

    def get_arguments_curve(circle_type):
        """Return the arguments for the curve function."""
        if circle_type == 0:
            # Full circle.
            arg_interval = [0, 2 * np.pi]
            arg_n_el = 2 * n_el
        elif circle_type == 1:
            # First half circle.
            arg_interval = [0, np.pi]
            arg_n_el = n_el
        elif circle_type == 2:
            # Second half circle.
            arg_interval = [np.pi, 2 * np.pi]
            arg_n_el = n_el
        return {
            "beam_class": Beam3rHerm2Line3,
            "material": mat,
            "function": circle_function,
            "interval": arg_interval,
            "n_el": arg_n_el,
        }

    # Check the meshes without additional rotation.
    assert_results_equal(
        get_corresponding_reference_file_path(), create_mesh_manually(Rotation())
    )
    assert_results_equal(
        get_corresponding_reference_file_path(),
        one_full_circle_closed(
            create_beam_mesh_arc_segment_via_rotation, get_arguments_arc_segment(0)
        ),
    )
    assert_results_equal(
        get_corresponding_reference_file_path(),
        two_half_circles_closed(
            create_beam_mesh_arc_segment_via_rotation,
            [get_arguments_arc_segment(1), get_arguments_arc_segment(2)],
        ),
    )
    assert_results_equal(
        get_corresponding_reference_file_path(),
        one_full_circle_closed(create_beam_mesh_curve, get_arguments_curve(0)),
    )
    assert_results_equal(
        get_corresponding_reference_file_path(),
        two_half_circles_closed(
            create_beam_mesh_curve, [get_arguments_curve(1), get_arguments_curve(2)]
        ),
    )

    # Check the meshes with additional rotation.
    additional_identifier = "rotation"
    assert_results_equal(
        get_corresponding_reference_file_path(
            additional_identifier=additional_identifier
        ),
        create_mesh_manually(additional_rotation),
    )
    assert_results_equal(
        get_corresponding_reference_file_path(
            additional_identifier=additional_identifier
        ),
        one_full_circle_closed(
            create_beam_mesh_arc_segment_via_rotation,
            get_arguments_arc_segment(0),
            additional_rotation=additional_rotation,
        ),
    )
    assert_results_equal(
        get_corresponding_reference_file_path(
            additional_identifier=additional_identifier
        ),
        two_half_circles_closed(
            create_beam_mesh_arc_segment_via_rotation,
            [get_arguments_arc_segment(1), get_arguments_arc_segment(2)],
            additional_rotation=additional_rotation,
        ),
    )
    assert_results_equal(
        get_corresponding_reference_file_path(
            additional_identifier=additional_identifier
        ),
        one_full_circle_closed(
            create_beam_mesh_curve,
            get_arguments_curve(0),
            additional_rotation=additional_rotation,
        ),
    )
    assert_results_equal(
        get_corresponding_reference_file_path(
            additional_identifier=additional_identifier
        ),
        two_half_circles_closed(
            create_beam_mesh_curve,
            [get_arguments_curve(1), get_arguments_curve(2)],
            additional_rotation=additional_rotation,
        ),
    )


def test_geometry_set_get_geometry_objects():
    """Test if the geometry set returns the objects(elements) in the correct
    order."""

    # Initialize material and input file.
    mat = MaterialReissner()
    mesh = InputFile()

    # number of elements
    n_el = 5

    # Create a simple beam.
    geometry = create_beam_mesh_line(
        mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [2, 0, 0], n_el=n_el
    )

    # Get all elements from the geometry set.
    elements_of_geometry = geometry["line"].get_geometry_objects()

    # Check number of elements.
    assert len(elements_of_geometry) == n_el

    # Check if the order of the elements from the geometry set is the same as for the mesh.
    for i_element, element in enumerate(elements_of_geometry):
        assert element == mesh.elements[i_element]


@pytest.mark.parametrize("use_nodal_geometry_sets", [True, False])
def test_meshpy_replace_nodes_geometry_set(
    get_bc_data, use_nodal_geometry_sets, assert_results_equal
):
    """Test case for coupling of nodes, and reusing the identical nodes."""

    mpy.check_overlapping_elements = False

    mat = MaterialReissner(radius=0.1, youngs_modulus=1)
    rot = Rotation([1, 2, 43], 213123)

    def create_mesh():
        """Create two empty meshes."""
        return InputFile(), InputFile()

    # Create a beam with two elements. Once immediately and once as two
    # beams with couplings.
    mesh_ref, mesh_couple = create_mesh()

    # Create a simple beam.
    create_beam_mesh_line(mesh_ref, Beam3rHerm2Line3, mat, [0, 0, 0], [2, 0, 0], n_el=2)
    create_beam_mesh_line(mesh_couple, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0])
    create_beam_mesh_line(mesh_couple, Beam3rHerm2Line3, mat, [1, 0, 0], [2, 0, 0])

    ref_nodes = list(mesh_ref.nodes)
    coupling_nodes = list(mesh_couple.nodes)

    # Add a set with all nodes, to check that the nodes in the
    # boundary condition are replaced correctly.
    if use_nodal_geometry_sets:
        mesh_ref.add(GeometrySetNodes(mpy.geo.line, ref_nodes))
        mesh_ref.add(GeometrySetNodes(mpy.geo.point, ref_nodes))
        mesh_couple.add(GeometrySetNodes(mpy.geo.line, coupling_nodes))
        mesh_couple.add(GeometrySetNodes(mpy.geo.point, coupling_nodes))
    else:
        mesh_ref.add(GeometrySet(mesh_ref.elements))
        mesh_ref.add(GeometrySet(ref_nodes))
        mesh_couple.add(GeometrySet(mesh_couple.elements))
        mesh_couple.add(GeometrySet(coupling_nodes))

    # Add another set with all nodes, this time only the coupling node
    # that will be kept is in this set.
    coupling_nodes_without_replace_node = list(coupling_nodes)
    del coupling_nodes_without_replace_node[3]
    if use_nodal_geometry_sets:
        mesh_ref.add(GeometrySetNodes(mpy.geo.point, ref_nodes))
        mesh_couple.add(
            GeometrySetNodes(mpy.geo.point, coupling_nodes_without_replace_node)
        )
    else:
        mesh_ref.add(GeometrySet(ref_nodes))
        mesh_couple.add(GeometrySet(coupling_nodes_without_replace_node))

    # Add another set with all nodes, this time only the coupling node
    # that will be replaced is in this set.
    coupling_nodes_without_replace_node = list(coupling_nodes)
    del coupling_nodes_without_replace_node[2]
    if use_nodal_geometry_sets:
        mesh_ref.add(GeometrySetNodes(mpy.geo.point, ref_nodes))
        mesh_couple.add(
            GeometrySetNodes(mpy.geo.point, coupling_nodes_without_replace_node)
        )
    else:
        mesh_ref.add(GeometrySet(ref_nodes))
        mesh_couple.add(GeometrySet(coupling_nodes_without_replace_node))

    # Rotate both meshes
    mesh_ref.rotate(rot)
    mesh_couple.rotate(rot)

    # Couple the coupling mesh.
    mesh_couple.couple_nodes(
        coupling_dof_type=mpy.coupling_dof.fix, reuse_matching_nodes=True
    )

    # Compare the meshes.
    assert_results_equal(mesh_ref, mesh_couple)

    # Create two overlapping beams. This is to test that the middle nodes
    # are not coupled.
    mesh_ref, mesh_couple = create_mesh()

    # Create a simple beam.
    set_ref = create_beam_mesh_line(
        mesh_ref, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0]
    )
    create_beam_mesh_line(
        mesh_ref,
        Beam3rHerm2Line3,
        mat,
        [0, 0, 0],
        [1, 0, 0],
        start_node=set_ref["start"],
        end_node=set_ref["end"],
    )
    create_beam_mesh_line(mesh_couple, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0])
    create_beam_mesh_line(mesh_couple, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0])

    # Rotate both meshes
    mesh_ref.rotate(rot)
    mesh_couple.rotate(rot)

    # Couple the coupling mesh.
    mesh_couple.couple_nodes(
        coupling_dof_type=mpy.coupling_dof.fix, reuse_matching_nodes=True
    )

    # Compare the meshes.
    assert_results_equal(mesh_ref, mesh_couple)

    # Create a beam with two elements. Once immediately and once as two
    # beams with couplings.
    mesh_ref, mesh_couple = create_mesh()

    # Create a simple beam.
    create_beam_mesh_line(mesh_ref, Beam3rHerm2Line3, mat, [0, 0, 0], [2, 0, 0], n_el=2)
    create_beam_mesh_line(mesh_couple, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0])
    create_beam_mesh_line(mesh_couple, Beam3rHerm2Line3, mat, [1, 0, 0], [2, 0, 0])

    # Create set with all the beam nodes.
    if use_nodal_geometry_sets:
        node_set_1_ref = GeometrySetNodes(mpy.geo.line, mesh_ref.nodes)
        node_set_2_ref = GeometrySetNodes(mpy.geo.line, mesh_ref.nodes)
        node_set_1_couple = GeometrySetNodes(mpy.geo.line, mesh_couple.nodes)
        node_set_2_couple = GeometrySetNodes(mpy.geo.line, mesh_couple.nodes)
    else:
        node_set_1_ref = GeometrySet(mesh_ref.elements)
        node_set_2_ref = GeometrySet(mesh_ref.elements)
        node_set_1_couple = GeometrySet(mesh_couple.elements)
        node_set_2_couple = GeometrySet(mesh_couple.elements)

    # Create connecting beams.
    create_beam_mesh_line(mesh_ref, Beam3rHerm2Line3, mat, [1, 0, 0], [2, 2, 2])
    create_beam_mesh_line(mesh_ref, Beam3rHerm2Line3, mat, [1, 0, 0], [2, -2, -2])
    create_beam_mesh_line(mesh_couple, Beam3rHerm2Line3, mat, [1, 0, 0], [2, 2, 2])
    create_beam_mesh_line(mesh_couple, Beam3rHerm2Line3, mat, [1, 0, 0], [2, -2, -2])

    # Rotate both meshes
    mesh_ref.rotate(rot)
    mesh_couple.rotate(rot)

    # Couple the mesh.
    mesh_ref.couple_nodes(coupling_dof_type=mpy.coupling_dof.fix)
    mesh_couple.couple_nodes(
        coupling_dof_type=mpy.coupling_dof.fix, reuse_matching_nodes=True
    )

    # Add the node sets.
    mesh_ref.add(node_set_1_ref)
    mesh_couple.add(node_set_1_couple)

    # Add BCs.
    mesh_ref.add(
        BoundaryCondition(node_set_2_ref, get_bc_data(), bc_type=mpy.bc.neumann)
    )
    mesh_couple.add(
        BoundaryCondition(node_set_2_couple, get_bc_data(), bc_type=mpy.bc.neumann)
    )

    # Compare the meshes.
    # TODO: Add reference mesh for this test
    assert_results_equal(mesh_ref, mesh_couple)


def create_beam_to_solid_conditions_model(get_corresponding_reference_file_path):
    """Create the input file for the beam-to-solid input conditions tests."""

    # Create input file.
    input_file = InputFile(
        yaml_file=get_corresponding_reference_file_path(
            reference_file_base_name="test_create_cubit_input_block"
        )
    )

    # Add beams to the model.
    beam_mesh = Mesh()
    material = MaterialReissner(youngs_modulus=1000, radius=0.05)
    create_beam_mesh_line(
        beam_mesh, Beam3rHerm2Line3, material, [0, 0, 0], [0, 0, 1], n_el=3
    )
    create_beam_mesh_line(
        beam_mesh, Beam3rHerm2Line3, material, [0, 0.5, 0], [0, 0.5, 1], n_el=3
    )

    # Set beam-to-solid coupling conditions.
    line_set = GeometrySet(beam_mesh.elements)
    beam_mesh.add(
        BoundaryCondition(
            line_set,
            bc_type=mpy.bc.beam_to_solid_volume_meshtying,
            data={"COUPLING_ID": 1},
        )
    )
    beam_mesh.add(
        BoundaryCondition(
            line_set,
            bc_type=mpy.bc.beam_to_solid_surface_meshtying,
            data={"COUPLING_ID": 2},
        )
    )

    # Add the beam to the solid mesh.
    input_file.add(beam_mesh)

    return input_file


@pytest.mark.parametrize("test_type", [None, "full"])
def test_meshpy_beam_to_solid_conditions(
    test_type,
    assert_results_equal,
    get_corresponding_reference_file_path,
):
    """Create the input file for the beam-to-solid input conditions tests."""

    if test_type == "full":
        mpy.import_mesh_full = True
    else:
        mpy.import_mesh_full = False

    # Get the input file.
    input_file = create_beam_to_solid_conditions_model(
        get_corresponding_reference_file_path
    )

    # Check results
    assert_results_equal(
        get_corresponding_reference_file_path(additional_identifier=test_type),
        input_file,
    )


def test_meshpy_surface_to_surface_contact_import(
    assert_results_equal, get_corresponding_reference_file_path
):
    """Test that surface-to-surface contact problems can be imported as
    expected."""

    # Create input file.
    mpy.import_mesh_full = True
    input_file = InputFile(
        yaml_file=get_corresponding_reference_file_path(
            additional_identifier="solid_mesh"
        )
    )

    # Compare with the reference file.
    assert_results_equal(get_corresponding_reference_file_path(), input_file)


def test_meshpy_nurbs_import(
    assert_results_equal, get_corresponding_reference_file_path
):
    """Test if the import of a NURBS mesh works as expected.

    This script generates the 4C test case:
    beam3r_herm2line3_static_beam_to_solid_volume_meshtying_nurbs27_mortar_penalty_line4
    """

    # Create beam mesh and load solid file.
    input_file = InputFile(
        yaml_file=get_corresponding_reference_file_path(
            additional_identifier="solid_mesh"
        )
    )
    set_header_static(
        input_file,
        time_step=0.5,
        n_steps=2,
        tol_residuum=1e-14,
        tol_increment=1e-8,
        option_overwrite=True,
    )
    set_beam_to_solid_meshtying(
        input_file,
        mpy.beam_to_solid.volume_meshtying,
        contact_discretization="mortar",
        mortar_shape="line4",
        penalty_parameter=1000,
        n_gauss_points=6,
        segmentation=True,
        binning_parameters={
            "binning_bounding_box": [-3, -3, -1, 3, 3, 5],
            "binning_cutoff_radius": 1,
        },
    )
    set_runtime_output(input_file, output_solid=False)
    input_file.add(
        {
            "IO": {
                "OUTPUT_BIN": True,
                "STRUCT_DISP": True,
                "VERBOSITY": "Standard",
            }
        },
        option_overwrite=True,
    )
    fun = Function([{"COMPONENT": 0, "SYMBOLIC_FUNCTION_OF_SPACE_TIME": "t"}])
    input_file.add(fun)

    # Create the beam material.
    material = MaterialReissner(youngs_modulus=1000, radius=0.05)

    # Create the beams.
    set_1 = create_beam_mesh_line(
        input_file, Beam3rHerm2Line3, material, [0, 0, 0.95], [1, 0, 0.95], n_el=2
    )
    set_2 = create_beam_mesh_line(
        input_file,
        Beam3rHerm2Line3,
        material,
        [-0.25, -0.3, 0.85],
        [-0.25, 0.5, 0.85],
        n_el=2,
    )

    # Add boundary conditions on the beams.
    input_file.add(
        BoundaryCondition(
            set_1["start"],
            {
                "NUMDOF": 9,
                "ONOFF": [0, 0, 0, 1, 1, 1, 0, 0, 0],
                "VAL": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                "FUNCT": [0, 0, 0, 0, 0, 0, 0, 0, 0],
            },
            bc_type=mpy.bc.dirichlet,
        )
    )
    input_file.add(
        BoundaryCondition(
            set_1["end"],
            {
                "NUMDOF": 9,
                "ONOFF": [0, 1, 0, 0, 0, 0, 0, 0, 0],
                "VAL": [0, 0.02, 0, 0, 0, 0, 0, 0, 0],
                "FUNCT": [0, fun, 0, 0, 0, 0, 0, 0, 0],
            },
            bc_type=mpy.bc.neumann,
        )
    )
    input_file.add(
        BoundaryCondition(
            set_2["start"],
            {
                "NUMDOF": 9,
                "ONOFF": [0, 0, 0, 1, 1, 1, 0, 0, 0],
                "VAL": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                "FUNCT": [0, 0, 0, 0, 0, 0, 0, 0, 0],
            },
            bc_type=mpy.bc.dirichlet,
        )
    )
    input_file.add(
        BoundaryCondition(
            set_2["end"],
            {
                "NUMDOF": 9,
                "ONOFF": [1, 0, 0, 0, 0, 0, 0, 0, 0],
                "VAL": [-0.06, 0, 0, 0, 0, 0, 0, 0, 0],
                "FUNCT": [fun, 0, 0, 0, 0, 0, 0, 0, 0],
            },
            bc_type=mpy.bc.neumann,
        )
    )

    # Add result checks.
    displacements = [
        [
            -5.14451531793581718e-01,
            -1.05846397858073843e-01,
            -1.77822866851472888e-01,
        ]
    ]
    nodes = [64]
    add_result_description(input_file, displacements, nodes)

    # Compare with the reference solution.
    assert_results_equal(get_corresponding_reference_file_path(), input_file)


def test_meshpy_stvenantkirchhoff_solid(
    assert_results_equal, get_corresponding_reference_file_path
):
    """Test that the input file for a solid with St.

    Venant Kirchhoff material properties is generated correctly
    """

    # Create materials
    material_1 = MaterialStVenantKirchhoff(youngs_modulus=157, nu=0.17, density=6.1e-7)

    material_2 = MaterialStVenantKirchhoff(youngs_modulus=370, nu=0.20, density=5.2e-7)

    # Create input file
    input_file = InputFile()
    input_file.add(material_1)
    input_file.add(material_2)

    # Compare with the reference file
    assert_results_equal(get_corresponding_reference_file_path(), input_file)


@pytest.mark.parametrize(
    "coupling_type",
    [
        ["exact", mpy.bc.point_coupling, mpy.coupling_dof.fix],
        [
            "penalty",
            mpy.bc.point_coupling_penalty,
            {
                "POSITIONAL_PENALTY_PARAMETER": 10000,
                "ROTATIONAL_PENALTY_PARAMETER": 0,
            },
        ],
    ],
)
def test_meshpy_point_couplings(
    coupling_type, assert_results_equal, get_corresponding_reference_file_path
):
    """Create the input file for the test_point_couplings method."""

    # Create input file.
    material = MaterialReissner(radius=0.1, youngs_modulus=1000, interaction_radius=2.0)
    input_file = InputFile()

    # Create a 2x2 grid of beams.
    for i in range(3):
        for j in range(2):
            create_beam_mesh_line(
                input_file, Beam3rHerm2Line3, material, [j, i, 0.0], [j + 1, i, 0.0]
            )
            create_beam_mesh_line(
                input_file, Beam3rHerm2Line3, material, [i, j, 0.0], [i, j + 1, 0.0]
            )

    # Couple the beams.
    input_file.couple_nodes(
        reuse_matching_nodes=True,
        coupling_type=coupling_type[1],
        coupling_dof_type=coupling_type[2],
    )

    assert_results_equal(
        get_corresponding_reference_file_path(additional_identifier=coupling_type[0]),
        input_file,
    )


def test_meshpy_point_couplings_check():
    """Test that the check for points at the same spatial position works for
    point couplings."""

    def get_nodes(scale_factor):
        """Return a list with nodes to be added to a coupling condition.

        The coordinates are modified such that they are close to each
        other within a radius of mpy.eps_pos * scale_factor
        """
        coordinates = np.zeros((10, 3))
        ref_point = [1, 2, 3]
        coordinates[0] = ref_point
        for i in range(1, 10):
            coordinates[i] = ref_point
            for i_dir in range(3):
                factor = 2 * ((i + i_dir % 3) % 2) - 1
                # Multiply with 0.5 here, because we add the tolerance in + and - direction
                coordinates[i, i_dir] += factor * mpy.eps_pos * scale_factor
        return [Node(coord) for coord in coordinates]

    # This should work, as the points are within the global tolerance of each
    # other
    Coupling(get_nodes(0.5), None, None)

    with pytest.raises(ValueError):
        # This should fail, as the points are not within the global tolerance
        # of each other
        Coupling(get_nodes(1.0), None, None)

    # This should work, as the points are not within the global tolerance of
    # each other but we dont perform the check
    Coupling(get_nodes(1.0), None, None, check_overlapping_nodes=False)


def test_meshpy_vtk_writer(
    assert_results_equal, get_corresponding_reference_file_path, tmp_path
):
    """Test the output created by the VTK writer."""

    # Initialize writer.
    writer = VTKWriter()

    # Add poly line.
    indices = writer.add_points([[0, 0, -2], [1, 1, -2], [2, 2, -1]])
    writer.add_cell(vtk.vtkPolyLine, indices)

    # Add quadratic quad.
    cell_data = {}
    cell_data["cell_data_1"] = 3
    cell_data["cell_data_2"] = [66, 0, 1]
    point_data = {}
    point_data["point_data_1"] = [1, 2, 3, 4, 5, -2, -3, 0]
    point_data["point_data_2"] = [
        [0.25, 0, -0.25],
        [1, 0.25, 0],
        [2, 0, 0],
        [2.25, 1.25, 0.5],
        [2, 2.25, 0],
        [1, 2, 0.5],
        [0, 2.25, 0],
        [0, 1, 0.5],
    ]
    indices = writer.add_points(
        [
            [0.25, 0, -0.25],
            [1, 0.25, 0],
            [2, 0, 0],
            [2.25, 1.25, 0.5],
            [2, 2.25, 0],
            [1, 2, 0.5],
            [0, 2.25, 0],
            [0, 1, 0.5],
        ],
        point_data=point_data,
    )
    writer.add_cell(
        vtk.vtkQuadraticQuad, indices[[0, 2, 4, 6, 1, 3, 5, 7]], cell_data=cell_data
    )

    # Add tetrahedron.
    cell_data = {}
    cell_data["cell_data_2"] = [5, 0, 10]
    point_data = {}
    point_data["point_data_1"] = [1, 2, 3, 4]
    indices = writer.add_points(
        [[3, 3, 3], [4, 4, 3], [4, 3, 3], [4, 4, 4]], point_data=point_data
    )
    writer.add_cell(vtk.vtkTetra, indices[[0, 2, 1, 3]], cell_data=cell_data)

    # Before we can write the data to file we have to store the cell and
    # point data in the grid
    writer.complete_data()

    # Write to file.
    ref_file = get_corresponding_reference_file_path(extension="vtu")
    vtk_file = tmp_path / ref_file.name
    writer.write_vtk(vtk_file, binary=False)

    # Compare the vtk files.
    assert_results_equal(ref_file, vtk_file)


def test_meshpy_vtk_writer_beam(
    assert_results_equal, get_corresponding_reference_file_path, tmp_path
):
    """Create a sample mesh and check the VTK output."""

    # Create the mesh.
    mesh = Mesh()

    # Add content to the mesh.
    mat = MaterialBeam(radius=0.05)
    create_beam_mesh_honeycomb(
        mesh, Beam3rHerm2Line3, mat, 2.0, 2, 3, n_el=2, add_sets=True
    )

    # Write VTK output, with coupling sets."""
    ref_file = get_corresponding_reference_file_path(extension="vtu")
    vtk_file = tmp_path / ref_file.name
    mesh.write_vtk(
        output_name="test_meshpy_vtk_writer",
        coupling_sets=True,
        output_directory=tmp_path,
        binary=False,
    )
    assert_results_equal(ref_file, vtk_file, atol=mpy.eps_pos)

    # Write VTK output, without coupling sets."""
    ref_file = get_corresponding_reference_file_path(
        additional_identifier="no_coupling_beam", extension="vtu"
    )
    vtk_file = tmp_path / ref_file.name
    mesh.write_vtk(
        output_name="test_meshpy_vtk_writer_beam_no_coupling",
        coupling_sets=False,
        output_directory=tmp_path,
        binary=False,
    )
    assert_results_equal(ref_file, vtk_file, atol=mpy.eps_pos)

    # Write VTK output, with coupling sets and additional points for visualization."""
    ref_file = get_corresponding_reference_file_path(
        additional_identifier="smooth_centerline_beam", extension="vtu"
    )
    vtk_file = tmp_path / ref_file.name
    mesh.write_vtk(
        output_name="test_meshpy_vtk_writer_beam_smooth_centerline",
        coupling_sets=True,
        output_directory=tmp_path,
        binary=False,
        beam_centerline_visualization_segments=3,
    )
    assert_results_equal(ref_file, vtk_file, atol=mpy.eps_pos)


def test_meshpy_vtk_writer_solid(
    assert_results_equal, get_corresponding_reference_file_path, tmp_path
):
    """Import a solid mesh and check the VTK output."""

    # Convert the solid mesh to meshpy objects. Without this parameter no
    # solid VTK file would be written.
    mpy.import_mesh_full = True

    # Create the input file and read solid mesh data.
    input_file = InputFile()
    input_file.read_yaml(
        get_corresponding_reference_file_path(
            reference_file_base_name="test_create_cubit_input_tube"
        )
    )

    # Write VTK output.
    ref_file = get_corresponding_reference_file_path(extension="vtu")
    vtk_file = tmp_path / ref_file.name
    if os.path.isfile(vtk_file):  # Todo: Can this check be removed?
        os.remove(vtk_file)
    input_file.write_vtk(
        output_name="test_meshpy_vtk_writer", output_directory=tmp_path, binary=False
    )

    # Compare the vtk files.
    assert_results_equal(ref_file, vtk_file)


def test_meshpy_vtk_writer_solid_elements(
    assert_results_equal, get_corresponding_reference_file_path, tmp_path
):
    """Import a solid mesh with all solid types and check the VTK output."""

    # Convert the solid mesh to meshpy objects. Without this parameter no
    # solid VTK file would be written.
    mpy.import_mesh_full = True

    # Create the input file and read solid mesh data.
    input_file = InputFile()
    input_file.read_yaml(
        get_corresponding_reference_file_path(additional_identifier="import")
    )

    # Write VTK output.
    ref_file = get_corresponding_reference_file_path(
        additional_identifier="solid", extension="vtu"
    )
    vtk_file = tmp_path / ref_file.name
    if os.path.isfile(vtk_file):  # Todo: Can this check be removed?
        os.remove(vtk_file)
    input_file.write_vtk(
        output_name="test_meshpy_vtk_writer_solid_elements",
        output_directory=tmp_path,
        binary=False,
    )

    # Compare the vtk files.
    assert_results_equal(ref_file, vtk_file)


def test_meshpy_vtk_curve_cell_data(
    assert_results_equal, get_corresponding_reference_file_path, tmp_path
):
    """Test that when creating a beam, cell data can be given.

    This test also checks, that the nan values in vtk can be explicitly
    given.
    """

    # Create the mesh.
    mesh = Mesh()
    mpy.vtk_nan_float = 69.69
    mpy.vtk_nan_int = 69

    # Add content to the mesh.
    mat = MaterialBeam(radius=0.05)
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [2, 0, 0], n_el=2)
    create_beam_mesh_line(
        mesh,
        Beam3rHerm2Line3,
        mat,
        [0, 1, 0],
        [2, 1, 0],
        n_el=2,
        vtk_cell_data={"cell_data": (1, mpy.vtk_type.int)},
    )
    create_beam_mesh_arc_segment_via_rotation(
        mesh,
        Beam3rHerm2Line3,
        mat,
        [0, 2, 0],
        Rotation([1, 0, 0], np.pi),
        1.5,
        np.pi / 2.0,
        n_el=2,
        vtk_cell_data={"cell_data": (2, mpy.vtk_type.int), "other_data": 69},
    )

    # Write VTK output, with coupling sets."""
    ref_file = get_corresponding_reference_file_path(
        additional_identifier="beam", extension="vtu"
    )
    vtk_file = tmp_path / ref_file.name
    mesh.write_vtk(
        output_name="test_meshpy_vtk_curve_cell_data",
        output_directory=tmp_path,
        binary=False,
    )

    # Compare the vtk files.
    assert_results_equal(ref_file, vtk_file)


@pytest.mark.skip(
    reason="Temporarily disabled due to switch to .yaml based input files - check if test is necessary and fix"
)
@pytest.mark.cubitpy
def test_meshpy_cubitpy_import(
    assert_results_equal,
    get_corresponding_reference_file_path,
    tmp_path,
):
    """Check that a import from a cubitpy object is the same as importing the
    input file."""

    # Load the mesh creation functions
    from tests.create_cubit_input import create_tube, create_tube_cubit

    # Create the input file and read the file.
    file_path = os.path.join(tmp_path, "test_cubitpy_import.4C.yaml")
    create_tube(file_path)
    input_file = InputFile(yaml_file=file_path)

    # Create the input file and read the cubit object.
    input_file_cubit = InputFile(cubit=create_tube_cubit())

    # Load the file from the reference folder.
    file_path_ref = get_corresponding_reference_file_path(
        reference_file_base_name="test_create_cubit_input_tube"
    )
    input_file_ref = InputFile(yaml_file=file_path_ref)

    # Compare the input files.
    assert_results_equal(input_file, input_file_cubit)
    assert_results_equal(input_file, input_file_ref, rtol=1e-14)


def test_meshpy_deep_copy(get_bc_data, assert_results_equal):
    """This test checks that the deep copy function on a mesh does not copy the
    materials or functions."""

    # Create material and function object.
    mat = MaterialReissner(youngs_modulus=1, radius=1)
    fun = Function("COMPONENT 0 SYMBOLIC_FUNCTION_OF_SPACE_TIME t")

    def create_mesh(mesh):
        """Add material and function to the mesh and create a beam."""
        mesh.add(fun, mat)
        set1 = create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0])
        set2 = create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [1, 0, 0], [1, 1, 0])
        mesh.add(
            BoundaryCondition(
                set1["line"], get_bc_data(identifier=1), bc_type=mpy.bc.dirichlet
            )
        )
        mesh.add(
            BoundaryCondition(
                set2["line"], get_bc_data(identifier=2), bc_type=mpy.bc.neumann
            )
        )
        mesh.couple_nodes()

    # The second mesh will be translated and rotated with those vales.
    translate = [1.0, 2.34535435, 3.345353]
    rotation = Rotation([1, 0.2342342423, -2.234234], np.pi / 15 * 27)

    # First create the mesh twice, move one and get the input file.
    mesh_ref_1 = Mesh()
    mesh_ref_2 = Mesh()
    create_mesh(mesh_ref_1)
    create_mesh(mesh_ref_2)
    mesh_ref_2.rotate(rotation)
    mesh_ref_2.translate(translate)
    input_file_ref = InputFile()
    input_file_ref.add(mesh_ref_1, mesh_ref_2)

    # Now copy the first mesh and add them together in the input file.
    mesh_copy_1 = Mesh()
    create_mesh(mesh_copy_1)
    mesh_copy_2 = mesh_copy_1.copy()
    mesh_copy_2.rotate(rotation)
    mesh_copy_2.translate(translate)
    input_file_copy = InputFile()
    input_file_copy.add(mesh_copy_1, mesh_copy_2)

    # Check that the input files are the same.
    # TODO: add reference file check here as well
    assert_results_equal(input_file_ref, input_file_copy)


def test_meshpy_mesh_add_checks():
    """This test checks that Mesh raises an error when double objects are added
    to the mesh."""

    # Mesh instance for this test.
    mesh = Mesh()

    # Create basic objects that will be added to the mesh.
    node = Node([0, 1.0, 2.0])
    element = Beam()
    mesh.add(node)
    mesh.add(element)

    # Create objects based on basic mesh items.
    coupling = Coupling(mesh.nodes, mpy.bc.point_coupling, mpy.coupling_dof.fix)
    coupling_penalty = Coupling(
        mesh.nodes, mpy.bc.point_coupling_penalty, mpy.coupling_dof.fix
    )
    geometry_set = GeometrySet(mesh.elements)
    mesh.add(coupling)
    mesh.add(coupling_penalty)
    mesh.add(geometry_set)

    # Add the objects again and check for errors.
    with pytest.raises(ValueError):
        mesh.add(node)
    with pytest.raises(ValueError):
        mesh.add(element)
    with pytest.raises(ValueError):
        mesh.add(coupling)
    with pytest.raises(ValueError):
        mesh.add(coupling_penalty)
    with pytest.raises(ValueError):
        mesh.add(geometry_set)


def test_meshpy_check_two_couplings(
    assert_results_equal, get_corresponding_reference_file_path
):
    """The current implementation can handle more than one coupling on a node
    correctly, therefore we check this here."""

    # Create mesh object
    mesh = InputFile()
    mat = MaterialReissner()
    mesh.add(mat)

    # Add two beams to create an elbow structure. The beams each have a
    # node at the intersection
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0])
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [1, 0, 0], [1, 1, 0])

    # Call coupling twice -> this will create two coupling objects for the
    # corner node
    mesh.couple_nodes()
    mesh.couple_nodes()

    # Create the input file
    assert_results_equal(get_corresponding_reference_file_path(), mesh)


@pytest.mark.parametrize("reuse_nodes", [[None, False], ["reuse", True]])
def test_meshpy_check_multiple_node_penalty_coupling(
    reuse_nodes, assert_results_equal, get_corresponding_reference_file_path
):
    """For point penalty coupling constraints, we add multiple coupling
    conditions.

    This is checked in this test case. This method creates the flag
    reuse_nodes decides if equal nodes are unified to a single node.
    """

    # Create mesh object
    mesh = InputFile()
    mat = MaterialReissner()
    mesh.add(mat)

    # Add three beams that have one common point
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0])
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [1, 0, 0], [2, 0, 0])
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [1, 0, 0], [2, -1, 0])

    mesh.couple_nodes(
        reuse_matching_nodes=reuse_nodes[1],
        coupling_type=mpy.bc.point_coupling_penalty,
        coupling_dof_type={
            "POSITIONAL_PENALTY_PARAMETER": 10000,
            "ROTATIONAL_PENALTY_PARAMETER": 0,
        },
    )
    assert_results_equal(
        get_corresponding_reference_file_path(additional_identifier=reuse_nodes[0]),
        mesh,
    )


def test_meshpy_check_double_elements(
    assert_results_equal, get_corresponding_reference_file_path, tmp_path
):
    """Check if there are overlapping elements in a mesh."""

    # Create mesh object.
    mesh = InputFile()
    mat = MaterialReissner()
    mesh.add(mat)

    # Add two beams to create an elbow structure. The beams each have a
    # node at the intersection.
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [2, 0, 0], n_el=2)
    create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0])

    # Rotate the mesh with an arbitrary rotation.
    mesh.rotate(Rotation([1, 2, 3.24313], 2.2323423), [1, 3, -2.23232323])

    # The elements in the created mesh are overlapping, check that an error
    # is thrown.
    with pytest.raises(ValueError):
        mesh.check_overlapping_elements()

    # Check if the overlapping elements are written to the vtk output.
    warnings.filterwarnings("ignore")
    ref_file = get_corresponding_reference_file_path(
        additional_identifier="beam", extension="vtu"
    )
    vtk_file = tmp_path / ref_file.name
    mesh.write_vtk(
        output_name="test_meshpy_check_double_elements",
        output_directory=tmp_path,
        binary=False,
        overlapping_elements=True,
    )

    # Compare the vtk files.
    assert_results_equal(ref_file, vtk_file)


@pytest.mark.parametrize("check", [True, False])
def test_meshpy_check_overlapping_coupling_nodes(check):
    """Per default, we check that coupling nodes are at the same physical
    position.

    This check can be deactivated with the keyword
    check_overlapping_nodes when creating a Coupling.
    """

    # Create mesh object.
    mesh = InputFile()
    mat = MaterialReissner()
    mesh.add(mat)

    # Add two beams to create an elbow structure. The beams each have a
    # node at the intersection.
    set_1 = create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0])
    set_2 = create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [2, 0, 0], [3, 0, 0])

    # Couple two nodes that are not at the same position.

    # Create the input file. This will cause an error, as there are two
    # couplings for one node.
    args = [
        [set_1["start"], set_2["end"]],
        mpy.bc.point_coupling,
        "coupling_type_string",
    ]
    if check:
        with pytest.raises(ValueError):
            Coupling(*args)
    else:
        Coupling(*args, check_overlapping_nodes=False)


def test_meshpy_check_start_end_node_error():
    """Check that an error is raised if wrong start and end nodes are given to
    a mesh creation function."""

    # Create mesh object.
    mesh = Mesh()
    mat = MaterialReissner()
    mesh.add(mat)

    # Try to create a line with a starting node that is not in the mesh.
    node = NodeCosserat([0, 0, 0], Rotation())
    args = [mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 0, 0]]
    kwargs = {"start_node": node}
    with pytest.raises(ValueError):
        create_beam_mesh_line(*args, **kwargs)
    node.coordinates = [1, 0, 0]
    kwargs = {"end_node": node}
    with pytest.raises(ValueError):
        create_beam_mesh_line(*args, **kwargs)


def test_meshpy_userdefined_boundary_condition(
    get_bc_data, assert_results_equal, get_corresponding_reference_file_path
):
    """Check if an user defined boundary condition can be added."""

    mesh = InputFile()

    mat = MaterialReissner()
    sets = create_beam_mesh_line(mesh, Beam3rHerm2Line3, mat, [0, 0, 0], [1, 2, 3])
    mesh.add(
        BoundaryCondition(
            sets["line"], get_bc_data(), bc_type="DESIGN VOL ALE DIRICH CONDITIONS"
        )
    )

    # Compare the output of the mesh.
    assert_results_equal(get_corresponding_reference_file_path(), mesh)


def test_meshpy_display_pyvista(get_corresponding_reference_file_path):
    """Test that the display in pyvista function does not lead to errors.

    TODO: Add a check for the created visualziation
    """

    mpy.import_mesh_full = True
    mesh = create_beam_to_solid_conditions_model(get_corresponding_reference_file_path)
    _ = mesh.display_pyvista(resolution=3)
