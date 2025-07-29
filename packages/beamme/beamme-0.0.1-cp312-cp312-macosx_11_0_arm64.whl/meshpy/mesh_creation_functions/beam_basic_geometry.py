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
"""This file has functions to create basic geometry items with meshpy."""

import warnings as _warnings

import numpy as _np

from meshpy.core.conf import mpy as _mpy
from meshpy.core.mesh import Mesh as _Mesh
from meshpy.core.rotation import Rotation as _Rotation
from meshpy.mesh_creation_functions.beam_generic import (
    create_beam_mesh_function as _create_beam_mesh_function,
)
from meshpy.utils.nodes import get_single_node as _get_single_node


def create_beam_mesh_line(mesh, beam_class, material, start_point, end_point, **kwargs):
    """Generate a straight line of beam elements.

    Args
    ----
    mesh: Mesh
        Mesh that the line will be added to.
    beam_class: Beam
        Class of beam that will be used for this line.
    material: Material
        Material for this line.
    start_point, end_point: _np.array, list
        3D-coordinates for the start and end point of the line.

    **kwargs (for all of them look into create_beam_mesh_function)
    ----
    n_el: int
        Number of equally spaced beam elements along the line. Defaults to 1.
        Mutually exclusive with l_el.
    l_el: float
        Desired length of beam elements. Mutually exclusive with n_el.
        Be aware, that this length might not be achieved, if the elements are
        warped after they are created.
    start_node: Node, GeometrySet
        Node to use as the first node for this line. Use this if the line
        is connected to other lines (angles have to be the same, otherwise
        connections should be used). If a geometry set is given, it can
        contain one, and one node only.
    add_sets: bool
        If this is true the sets are added to the mesh and then displayed
        in eventual VTK output, even if they are not used for a boundary
        condition or coupling.

    Return
    ----
    return_set: GeometryName
        Set with the 'start' and 'end' node of the line. Also a 'line' set
        with all nodes of the line.
    """

    # Get geometrical values for this line.
    start_point = _np.asarray(start_point)
    end_point = _np.asarray(end_point)
    direction = end_point - start_point
    line_length = _np.linalg.norm(direction)
    t1 = direction / line_length

    # Check if the z or y axis are larger projected onto the direction.
    # The tolerance is used here to ensure that round-off changes in the last digits of
    # the floating point values don't switch the case. This increases the robustness in
    # testing.
    if abs(_np.dot(t1, [0, 0, 1])) < abs(_np.dot(t1, [0, 1, 0])) - _mpy.eps_quaternion:
        t2 = [0, 0, 1]
    else:
        t2 = [0, 1, 0]
    rotation = _Rotation.from_basis(t1, t2)

    def get_beam_geometry(parameter_a, parameter_b):
        """Return a function for the position along the beams axis."""

        def beam_function(xi):
            """Return a point on the beams axis for a given parameter
            coordinate xi."""
            point_a = start_point + parameter_a * direction
            point_b = start_point + parameter_b * direction
            pos = 0.5 * (1 - xi) * point_a + 0.5 * (1 + xi) * point_b
            arc_length = (
                0.5 * (1 - xi) * parameter_a + 0.5 * (1 + xi) * parameter_b
            ) * line_length
            return (pos, rotation, arc_length)

        return beam_function

    # Create the beam in the mesh
    return _create_beam_mesh_function(
        mesh,
        beam_class=beam_class,
        material=material,
        function_generator=get_beam_geometry,
        interval=[0.0, 1.0],
        interval_length=line_length,
        **kwargs,
    )


def create_beam_mesh_arc_segment_via_rotation(
    mesh, beam_class, material, center, axis_rotation, radius, angle, **kwargs
):
    """Generate a circular segment of beam elements.

    The circular segment is defined via a rotation, specifying the "initial"
    triad of the beam at the beginning of the arc.

    This function exists for compatibility reasons with older MeshPy implementations.
    The user is encouraged to use the newer implementation create_beam_mesh_arc_segment_via_axis

    Args
    ----
    mesh: Mesh
        Mesh that the arc segment will be added to.
    beam_class: Beam
        Class of beam that will be used for this line.
    material: Material
        Material for this segment.
    center: _np.array, list
        Center of the arc.
    axis_rotation: Rotation
        This rotation defines the spatial orientation of the arc.
        The 3rd base vector of this rotation is the rotation axis of the arc
        segment. The segment starts in the direction of the 1st basis vector
        and the starting point is along the 2nd basis vector.
    radius: float
        The radius of the segment.
    angle: float
        The central angle of this segment in radians.

    **kwargs (for all of them look into create_beam_mesh_function)
    ----
    n_el: int
        Number of equally spaced beam elements along the line. Defaults to 1.
        Mutually exclusive with l_el.
    l_el: float
        Desired length of beam elements. Mutually exclusive with n_el.
        Be aware, that this length might not be achieved, if the elements are
        warped after they are created.

    Return
    ----
    return_set: GeometryName
        Set with the 'start' and 'end' node of the line. Also a 'line' set
        with all nodes of the line.
    """

    # Convert the input to the one for create_beam_mesh_arc_segment_via_axis
    axis = axis_rotation * [0, 0, 1]
    start_point = center + radius * (axis_rotation * [0, -1, 0])
    return create_beam_mesh_arc_segment_via_axis(
        mesh, beam_class, material, axis, center, start_point, angle, **kwargs
    )


def create_beam_mesh_arc_segment_via_axis(
    mesh,
    beam_class,
    material,
    axis,
    axis_point,
    start_point,
    angle,
    **kwargs,
):
    """Generate a circular segment of beam elements.

    The arc is defined via a rotation axis, a point on the rotation axis a starting
    point, as well as the angle of the arc segment.

    Args
    ----
    mesh: Mesh
        Mesh that the arc segment will be added to.
    beam_class: Beam
        Class of beam that will be used for this line.
    material: Material
        Material for this segment.
    axis: _np.array, list
        Rotation axis of the arc.
    axis_point: _np.array, list
        Point lying on the rotation axis. Does not have to be the center of the arc.
    start_point: _np.array, list
        Start point of the arc.
    angle: float
        The central angle of this segment in radians.

    **kwargs (for all of them look into create_beam_mesh_function)
    ----
    n_el: int
        Number of equally spaced beam elements along the line. Defaults to 1.
        Mutually exclusive with l_el.
    l_el: float
        Desired length of beam elements. Mutually exclusive with n_el.
        Be aware, that this length might not be achieved, if the elements are
        warped after they are created.

    Return
    ----
    return_set: GeometryName
        Set with the 'start' and 'end' node of the line. Also a 'line' set
        with all nodes of the line.
    """

    # The angle can not be negative with the current implementation.
    if angle <= 0.0:
        raise ValueError(
            "The angle for a beam arc segment has to be a positive number!"
        )

    # Shortest distance from the given point to the axis of rotation gives
    # the "center" of the arc
    axis = _np.asarray(axis)
    axis_point = _np.asarray(axis_point)
    start_point = _np.asarray(start_point)

    axis = axis / _np.linalg.norm(axis)
    diff = start_point - axis_point
    distance = diff - _np.dot(_np.dot(diff, axis), axis)
    radius = _np.linalg.norm(distance)
    center = start_point - distance

    # Get the rotation at the start
    # No need to check the start node here, as eventual rotation offsets in
    # tangential direction will be covered by the create beam functionality.
    tangent = _np.cross(axis, distance)
    tangent /= _np.linalg.norm(tangent)
    start_rotation = _Rotation.from_rotation_matrix(
        _np.transpose(_np.array([tangent, -distance / radius, axis]))
    )

    def get_beam_geometry(alpha, beta):
        """Return a function for the position and rotation along the beam
        axis."""

        def beam_function(xi):
            """Return a point and the triad on the beams axis for a given
            parameter coordinate xi."""
            phi = 0.5 * (xi + 1) * (beta - alpha) + alpha
            arc_rotation = _Rotation(axis, phi)
            rot = arc_rotation * start_rotation
            pos = center + arc_rotation * distance
            return (pos, rot, phi * radius)

        return beam_function

    # Create the beam in the mesh
    return _create_beam_mesh_function(
        mesh,
        beam_class=beam_class,
        material=material,
        function_generator=get_beam_geometry,
        interval=[0.0, angle],
        interval_length=angle * radius,
        **kwargs,
    )


def create_beam_mesh_arc_segment_2d(
    mesh, beam_class, material, center, radius, phi_start, phi_end, **kwargs
):
    """Generate a circular segment of beam elements in the x-y plane.

    Args
    ----
    mesh: Mesh
        Mesh that the arc segment will be added to.
    beam_class: Beam
        Class of beam that will be used for this line.
    material: Material
        Material for this segment.
    center: _np.array, list
        Center of the arc. If the z component is not 0, an error will be
        thrown.
    radius: float
        The radius of the segment.
    phi_start, phi_end: float
        The start and end angles of the arc w.r.t the x-axis. If the start
        angle is larger than the end angle the beam faces in counter-clockwise
        direction, and if the start angle is smaller than the end angle, the
        beam faces in clockwise direction.

    **kwargs (for all of them look into create_beam_mesh_function)
    ----
    n_el: int
        Number of equally spaced beam elements along the line. Defaults to 1.
        Mutually exclusive with l_el.
    l_el: float
        Desired length of beam elements. Mutually exclusive with n_el.
        Be aware, that this length might not be achieved, if the elements are
        warped after they are created.

    Return
    ----
    return_set: GeometryName
        Set with the 'start' and 'end' node of the line. Also a 'line' set
        with all nodes of the line.
    """

    # The center point has to be on the x-y plane.
    if _np.abs(center[2]) > _mpy.eps_pos:
        raise ValueError("The z-value of center has to be 0!")

    # Check if the beam is in clockwise or counter clockwise direction.
    angle = phi_end - phi_start
    axis = _np.array([0, 0, 1])
    start_point = center + radius * (_Rotation(axis, phi_start) * [1, 0, 0])

    counter_clockwise = _np.sign(angle) == 1
    if not counter_clockwise:
        # If the beam is not in counter clockwise direction, we have to flip
        # the rotation axis.
        axis = -1.0 * axis

    return create_beam_mesh_arc_segment_via_axis(
        mesh,
        beam_class,
        material,
        axis,
        center,
        start_point,
        _np.abs(angle),
        **kwargs,
    )


def create_beam_mesh_line_at_node(
    mesh, beam_class, material, start_node, length, **kwargs
):
    """Generate a straight line at a given node. The tangent will be the same
    as at that node.

    Args
    ----
    mesh: Mesh
        Mesh that the arc segment will be added to.
    beam_class: Beam
        Class of beam that will be used for this line.
    material: Material
        Material for this segment.
    start_node: _np.array, list
        Point where the arc will continue.
    length: float
        Length of the line.

    **kwargs (for all of them look into create_beam_mesh_function)
    ----
    n_el: int
        Number of equally spaced beam elements along the line. Defaults to 1.
        Mutually exclusive with l_el.
    l_el: float
        Desired length of beam elements. Mutually exclusive with n_el.
        Be aware, that this length might not be achieved, if the elements are
        warped after they are created.

    Return
    ----
    return_set: GeometryName
        Set with the 'start' and 'end' node of the line. Also a 'line' set
        with all nodes of the line.
    """

    if length < 0:
        raise ValueError("Length has to be positive!")

    # Create the line starting from the given node
    start_node = _get_single_node(start_node)
    tangent = start_node.rotation * [1, 0, 0]
    start_position = start_node.coordinates
    end_position = start_position + tangent * length

    return create_beam_mesh_line(
        mesh,
        beam_class,
        material,
        start_position,
        end_position,
        start_node=start_node,
        **kwargs,
    )


def create_beam_mesh_arc_at_node(
    mesh, beam_class, material, start_node, arc_axis_normal, radius, angle, **kwargs
):
    """Generate a circular segment starting at a given node. The arc will be
    tangent to the given node.

    Args
    ----
    mesh: Mesh
        Mesh that the arc segment will be added to.
    beam_class: Beam
        Class of beam that will be used for this line.
    material: Material
        Material for this segment.
    start_node: _np.array, list
        Point where the arc will continue.
    arc_axis_normal: 3d-vector
        Rotation axis for the created arc.
    radius: float
        The radius of the arc segment.
    angle: float
        Angle of the arc. If the angle is negative, the arc will point in the
        opposite direction, i.e., as if the arc_axis_normal would change sign.

    **kwargs (for all of them look into create_beam_mesh_function)
    ----
    n_el: int
        Number of equally spaced beam elements along the line. Defaults to 1.
        Mutually exclusive with l_el.
    l_el: float
        Desired length of beam elements. Mutually exclusive with n_el.
        Be aware, that this length might not be achieved, if the elements are
        warped after they are created.

    Return
    ----
    return_set: GeometryName
        Set with the 'start' and 'end' node of the line. Also a 'line' set
        with all nodes of the line.
    """

    # If the angle is negative, the normal is switched
    arc_axis_normal = _np.asarray(arc_axis_normal)
    if angle < 0:
        arc_axis_normal = -1.0 * arc_axis_normal

    # The normal has to be perpendicular to the start point tangent
    start_node = _get_single_node(start_node)
    tangent = start_node.rotation * [1, 0, 0]
    if _np.abs(_np.dot(tangent, arc_axis_normal)) > _mpy.eps_pos:
        raise ValueError(
            "The normal has to be perpendicular to the tangent in the start node!"
        )

    # Get the center of the arc
    center_direction = _np.cross(tangent, arc_axis_normal)
    center_direction *= 1.0 / _np.linalg.norm(center_direction)
    center = start_node.coordinates - center_direction * radius

    return create_beam_mesh_arc_segment_via_axis(
        mesh,
        beam_class,
        material,
        arc_axis_normal,
        center,
        start_node.coordinates,
        _np.abs(angle),
        start_node=start_node,
        **kwargs,
    )


def create_beam_mesh_helix(
    mesh,
    beam_class,
    material,
    axis_vector,
    axis_point,
    start_point,
    *,
    helix_angle=None,
    height_helix=None,
    turns=None,
    warning_straight_line=True,
    **kwargs,
):
    """Generate a helical segment starting at a given start point around a
    predefined axis (defined by axis_vector and axis_point). The helical
    segment is defined by a start_point and exactly two of the basic helical
    quantities [helix_angle, height_helix, turns].

    Args
    ----
    mesh: Mesh
        Mesh that the helical segment will be added to.
    beam_class: Beam
        Class of beam that will be used for this line.
    material: Material
        Material for this segment.
    axis_vector: _np.array, list
        Vector for the orientation of the helical center axis.
    axis_point: _np.array, list
        Point lying on the helical center axis. Does not need to align with
        bottom plane of helix.
    start_point: _np.array, list
        Start point of the helix. Defines the radius.
    helix_angle: float
        Angle of the helix (synonyms in literature: twist angle or pitch
        angle).
    height_helix: float
        Height of helix.
    turns: float
        Number of turns.
    warning_straight_line: bool
        Warn if radius of helix is zero or helix angle is 90 degrees and
        simple line is returned.

    **kwargs (for all of them look into create_beam_mesh_function)
    ----
    n_el: int
        Number of equally spaced beam elements along the line. Defaults to 1.
        Mutually exclusive with l_el.
    l_el: float
        Desired length of beam elements. Mutually exclusive with n_el.
        Be aware, that this length might not be achieved, if the elements are
        warped after they are created.

    Return
    ----
    return_set: GeometryName
        Set with the 'start' and 'end' node of the line. Also a 'line' set
        with all nodes of the line.
    """

    if [helix_angle, height_helix, turns].count(None) != 1:
        raise ValueError(
            "Exactly two arguments of [helix_angle, height_helix, turns]"
            " must be provided!"
        )

    if helix_angle is not None and _np.isclose(_np.sin(helix_angle), 0.0):
        raise ValueError(
            "Helix angle of helix is 0 degrees! "
            + "Change angle for feasible helix geometry!"
        )

    if height_helix is not None and _np.isclose(height_helix, 0.0):
        raise ValueError(
            "Height of helix is 0! Change height for feasible helix geometry!"
        )

    # determine radius of helix
    axis_vector = _np.asarray(axis_vector)
    axis_point = _np.asarray(axis_point)
    start_point = _np.asarray(start_point)

    axis_vector = axis_vector / _np.linalg.norm(axis_vector)
    origin = axis_point + _np.dot(
        _np.dot(start_point - axis_point, axis_vector), axis_vector
    )
    start_point_origin_vec = start_point - origin
    radius = _np.linalg.norm(start_point_origin_vec)

    # create temporary mesh to not alter original mesh
    mesh_temp = _Mesh()

    # return line if radius of helix is 0, helix angle is pi/2 or turns is 0
    if (
        _np.isclose(radius, 0)
        or (helix_angle is not None and _np.isclose(_np.cos(helix_angle), 0.0))
        or (turns is not None and _np.isclose(turns, 0.0))
    ):
        if height_helix is None:
            raise ValueError(
                "Radius of helix is 0, helix angle is 90 degrees or turns is 0! "
                + "Fallback to simple line geometry but height cannot be "
                + "determined based on helix angle and turns! Either switch one "
                + "helix parameter to height of helix or change radius!"
            )

        if warning_straight_line:
            _warnings.warn(
                "Radius of helix is 0, helix angle is 90 degrees or turns is 0! "
                + "Simple line geometry is returned!"
            )

        if helix_angle is not None and height_helix is not None:
            end_point = start_point + height_helix * axis_vector * _np.sign(
                _np.sin(helix_angle)
            )
        elif height_helix is not None and turns is not None:
            end_point = start_point + height_helix * axis_vector

        line_sets = create_beam_mesh_line(
            mesh_temp,
            beam_class,
            material,
            start_point=start_point,
            end_point=end_point,
            **kwargs,
        )

        # add line to mesh
        mesh.add_mesh(mesh_temp)

        return line_sets

    # generate simple helix
    if helix_angle and height_helix:
        end_point = _np.array(
            [
                radius,
                _np.sign(_np.sin(helix_angle)) * height_helix / _np.tan(helix_angle),
                _np.sign(_np.sin(helix_angle)) * height_helix,
            ]
        )
    elif helix_angle and turns:
        end_point = _np.array(
            [
                radius,
                _np.sign(_np.cos(helix_angle)) * 2 * _np.pi * radius * turns,
                _np.sign(_np.cos(helix_angle))
                * 2
                * _np.pi
                * radius
                * _np.abs(turns)
                * _np.tan(helix_angle),
            ]
        )
    elif height_helix and turns:
        end_point = _np.array(
            [
                radius,
                2 * _np.pi * radius * turns,
                height_helix,
            ]
        )

    helix_sets = create_beam_mesh_line(
        mesh_temp,
        beam_class,
        material,
        start_point=[radius, 0, 0],
        end_point=end_point,
        **kwargs,
    )

    mesh_temp.wrap_around_cylinder()

    # rotate and translate simple helix to align with necessary axis and starting point
    mesh_temp.rotate(
        _Rotation.from_basis(start_point_origin_vec, axis_vector)
        * _Rotation([1, 0, 0], -_np.pi * 0.5)
    )
    mesh_temp.translate(-mesh_temp.nodes[0].coordinates + start_point)

    # add helix to mesh
    mesh.add_mesh(mesh_temp)

    return helix_sets
