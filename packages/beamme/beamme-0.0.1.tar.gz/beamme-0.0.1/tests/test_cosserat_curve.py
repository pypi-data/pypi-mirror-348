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
"""Test the functionality of the Cosserat curve module."""

import numpy as np
import pytest
import pyvista as pv
import quaternion

from meshpy.core.conf import mpy
from meshpy.core.rotation import Rotation
from meshpy.cosserat_curve.cosserat_curve import CosseratCurve
from meshpy.cosserat_curve.warping_along_cosserat_curve import (
    create_transform_boundary_conditions,
    get_mesh_transformation,
    warp_mesh_along_curve,
)
from meshpy.four_c.element_beam import Beam3rHerm2Line3
from meshpy.four_c.input_file import InputFile
from meshpy.four_c.material import MaterialReissner
from meshpy.mesh_creation_functions.beam_basic_geometry import create_beam_mesh_helix


def load_cosserat_curve_from_file(get_corresponding_reference_file_path):
    """Load the centerline coordinates from the reference files and create the
    Cosserat curve."""
    point_coordinates_file = get_corresponding_reference_file_path(
        reference_file_base_name="test_cosserat_curve_centerline", extension="txt"
    )
    coordinates = np.loadtxt(
        point_coordinates_file, comments="#", delimiter=",", unpack=False
    )
    return CosseratCurve(coordinates)


def create_beam_solid_input_file(get_corresponding_reference_file_path):
    """Create a beam and solid input file for testing purposes."""

    mpy.import_mesh_full = True
    mesh = InputFile(
        yaml_file=get_corresponding_reference_file_path(
            reference_file_base_name="test_cosserat_curve_mesh"
        )
    )
    create_beam_mesh_helix(
        mesh,
        Beam3rHerm2Line3,
        MaterialReissner(radius=0.05),
        [0, 0, 1],
        [0, 0, 0],
        [2, 0, 0],
        helix_angle=0.4,
        turns=3,
        n_el=5,
    )
    return mesh


def test_cosserat_curve_translate_and_rotate(get_corresponding_reference_file_path):
    """Test that a curve can be loaded, rotated and transformed."""

    curve = load_cosserat_curve_from_file(get_corresponding_reference_file_path)

    # Translate the curve so that the start is at the origin
    curve.translate(-curve.centerline_interpolation(5.0))

    # Rotate the curve around its center point
    pos_1, q_1 = curve.get_centerline_position_and_rotation(0.0)
    curve.rotate(Rotation.from_quaternion(quaternion.as_float_array(q_1)), origin=pos_1)

    # Get the points and rotations at certain points
    t = list(map(float, range(-10, 30, 5)))
    sol_half_pos, sol_half_q = curve.get_centerline_positions_and_rotations(
        t, factor=0.5
    )
    sol_full_pos, sol_full_q = curve.get_centerline_positions_and_rotations(
        t, factor=1.0
    )

    def load_compare(name):
        """Load the compare files and return a numpy array."""
        return np.loadtxt(
            get_corresponding_reference_file_path(
                additional_identifier=name, extension="txt"
            )
        )

    assert np.allclose(sol_half_pos, load_compare("pos_half_ref"), rtol=1e-14)
    assert np.allclose(
        quaternion.as_float_array(sol_half_q), load_compare("q_half_ref"), rtol=1e-14
    )

    assert np.allclose(sol_full_pos, load_compare("pos_full_ref"), rtol=1e-14)
    assert np.allclose(
        quaternion.as_float_array(sol_full_q), load_compare("q_full_ref"), rtol=1e-14
    )


def test_cosserat_curve_vtk_representation(
    tmp_path, get_corresponding_reference_file_path, assert_results_equal
):
    """Test the vtk representation of the Cosserat curve."""

    reference_path = get_corresponding_reference_file_path(extension="vtu")
    result_path = tmp_path / reference_path.name

    curve = load_cosserat_curve_from_file(get_corresponding_reference_file_path)
    pv.UnstructuredGrid(curve.get_pyvista_polyline()).save(result_path)

    assert_results_equal(
        reference_path,
        result_path,
        rtol=1e-8,
        atol=1e-8,
    )


def test_cosserat_curve_project_point(get_corresponding_reference_file_path):
    """Test that the project point function works as expected."""

    # Load the curve
    curve = load_cosserat_curve_from_file(get_corresponding_reference_file_path)

    # Translate the curve so that the start is at the origin
    curve.translate(-curve.centerline_interpolation(0.0))

    # Check the projection results
    rtol = 1e-14
    t_ref = 4.264045157204052
    assert np.allclose(t_ref, curve.project_point([-5, 1, 1]), rtol=rtol)
    assert np.allclose(t_ref, curve.project_point([-5, 1, 1], t0=2.0), rtol=rtol)
    assert np.allclose(t_ref, curve.project_point([-5, 1, 1], t0=4.0), rtol=rtol)


def test_cosserat_curve_mesh_transformation(
    get_corresponding_reference_file_path,
    assert_results_equal,
):
    """Test that the get_mesh_transformation function works as expected."""

    curve = load_cosserat_curve_from_file(get_corresponding_reference_file_path)
    pos, rot = curve.get_centerline_position_and_rotation(0)
    rot = Rotation.from_quaternion(quaternion.as_float_array(rot))
    curve.translate(-pos)
    curve.translate([1, 2, 3])

    mesh = create_beam_solid_input_file(get_corresponding_reference_file_path)
    pos, rot = get_mesh_transformation(
        curve,
        mesh.nodes,
        origin=[0.5, 1.0, -1.0],
        reference_rotation=(
            Rotation([0, 0, 1], -0.5 * np.pi) * Rotation([0, 1, 0], -0.5 * np.pi)
        ),
        n_steps=3,
    )

    assert_results_equal(
        get_corresponding_reference_file_path(extension="json"),
        {"pos": pos, "rot": quaternion.as_float_array(rot)},
        rtol=1e-14,
    )


def test_cosserat_curve_mesh_warp(
    get_corresponding_reference_file_path,
    assert_results_equal,
):
    """Warp a balloon along a centerline."""

    # Load the curve
    curve = load_cosserat_curve_from_file(get_corresponding_reference_file_path)
    pos, rot = curve.get_centerline_position_and_rotation(0)
    rot = Rotation.from_quaternion(quaternion.as_float_array(rot))
    curve.translate(-pos)
    curve.translate([1, 2, 3])

    # Warp the mesh. The reference coordinate system is rotated such that z axis is the longitudinal direction,
    # and x and y are the first and second cross-section basis vectors respectively.
    mesh = create_beam_solid_input_file(get_corresponding_reference_file_path)
    warp_mesh_along_curve(
        mesh,
        curve,
        origin=[0.5, 1.0, -1.0],
        reference_rotation=(
            Rotation([0, 0, 1], -0.5 * np.pi) * Rotation([0, 1, 0], -0.5 * np.pi)
        ),
    )

    assert_results_equal(get_corresponding_reference_file_path(), mesh, rtol=1e-10)


def test_cosserat_curve_mesh_warp_transform_boundary_conditions(
    get_corresponding_reference_file_path,
    assert_results_equal,
):
    """Test the transform boundary creation function."""

    # Load the curve
    curve = load_cosserat_curve_from_file(get_corresponding_reference_file_path)
    pos, rot = curve.get_centerline_position_and_rotation(0)
    rot = Rotation.from_quaternion(quaternion.as_float_array(rot))
    curve.translate(-pos)
    curve.translate([1, 2, 3])

    # Load the mesh
    mesh = create_beam_solid_input_file(get_corresponding_reference_file_path)

    # Apply the transform boundary conditions
    create_transform_boundary_conditions(
        mesh,
        curve,
        n_steps=3,
        origin=[2, 3, 0.5],
        reference_rotation=(
            Rotation([0, 0, 1], -0.5 * np.pi) * Rotation([0, 1, 0], -0.5 * np.pi)
        ),
    )

    assert_results_equal(
        get_corresponding_reference_file_path(), mesh, rtol=1e-8, atol=1e-8
    )
