import sys
import pymel.core as pymel
import maya.OpenMaya as OpenMaya
import math
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


"""
Using reset vertex position to store previous vertex position in an Undo step
"""
try:
    if not pymel.pluginInfo('reset_vertex_position.py', query=True, loaded=True):
        pymel.loadPlugin('reset_vertex_position.py')
except Exception as ex:
    log.error('Could not load reset_vertex_position.py')
    pass


def get_select_type():

    if pymel.selectType(vertex=True, query=True):
        return 'vertex'
    elif pymel.selectType(facet=True, query=True):
        return 'face'
    elif pymel.selectType(edge=True, query=True):
        return 'edge'


def set_select_type(mesh, select_type):
    if select_type == 'vertex':
        command = 'doMenuComponentSelection("{}", "vertex");'.format(mesh)
        pymel.mel.eval(command)
    elif select_type == 'face':
        command = 'doMenuComponentSelection("{}", "facet");'.format(mesh)
        pymel.mel.eval(command)
    elif select_type == 'edge':
        command = 'doMenuComponentSelection("{}", "edge");'.format(mesh)
        pymel.mel.eval(command)


def get_components():
    # Mesh Selection
    mesh = pymel.selected(objectsOnly=True)[0]

    # Original Selection
    orig_sel = pymel.selected()
    orig_sel_type = get_select_type()

    # Set UNDO point
    pymel.select(mesh)
    pymel.reset_vertex_position()
    pymel.select(orig_sel)

    # Get Vertices
    pymel.mel.eval('ConvertSelectionToVertices')
    vertex_selection = pymel.selected(flatten=True)

    # Get Border Vertices
    pymel.runtime.ConvertSelectionToVertexPerimeter()
    border_selection = pymel.selected(flatten=True)

    return mesh, vertex_selection, border_selection, orig_sel, orig_sel_type



def get_average_pos(verts):
    """
    Returns center of min and max positions for x,y,z
    :param verts:
    :return:
    """

    x_pos = [x.getPosition(space='world').x for x in verts]
    y_pos = [x.getPosition(space='world').y for x in verts]
    z_pos = [x.getPosition(space='world').z for x in verts]

    med_x = sum([max(x_pos), min(x_pos)]) / 2
    med_y = sum([max(y_pos), min(y_pos)]) / 2
    med_z = sum([max(z_pos), min(z_pos)]) / 2

    average_pos = OpenMaya.MVector(med_x, med_y, med_z)
    return average_pos


def get_manipulator_orientation():
    """This is a cheat until I find a better way to calculate the plane"""

    # Store original manipulator mode setting
    orig_mode = pymel.manipMoveContext('Move', query=True, mode=True)

    # Set manipulator to 'Component'
    pymel.manipMoveContext('Move', edit=True, mode=9)


    # Get manipulator Orientation
    orientation = pymel.manipMoveContext('Move', query=True, orientAxes=True)
    print orientation

    loc = pymel.spaceLocator(name='orientation')
    loc.setRotation([pymel.util.degrees(orientation[0]), pymel.util.degrees(orientation[1]), pymel.util.degrees(orientation[2])])
    print loc.getRotation()

    # Get X normal
    values = loc.getMatrix()[0][0:3]
    # print values


    pymel.delete(loc)
    pymel.manipMoveContext('Move', edit=True, mode=orig_mode)

    return OpenMaya.MVector(values[0], values[1], values[2])


def get_plane_normal(average_pos, vertices):

    pos_a = vertices[0].getPosition(space='world')
    pos_b = vertices[-1].getPosition(space='world')

    # Get the first cross product
    vector_a = average_pos - OpenMaya.MVector(pos_a.x, pos_a.y, pos_a.z)
    vector_b = average_pos - OpenMaya.MVector(pos_b.x, pos_b.y, pos_b.z)

    first_normal = vector_a ^ vector_b

    average_normal = OpenMaya.MVector(0, 0, 0)

    for idx, vtx in enumerate(vertices):

        vector_a = average_pos - OpenMaya.MVector(vertices[idx].getPosition(space='world'))
        vector_b = average_pos - OpenMaya.MVector(vertices[idx-2].getPosition(space='world'))

        normal = vector_a ^ vector_b
        dot = normal * first_normal

        if dot < 0:

            normal = vector_b ^ vector_a
            dot = normal * first_normal

        final_pos = average_pos + normal

        average_normal += normal

    if len(vertices):
        average_normal /= len(vertices)

    average_normal.normalize()

    # final_pos = average_pos + average_normal

    # loc = pymel.spaceLocator(name='normal')
    # loc.setTranslation((final_pos.x, final_pos.y, final_pos.z), space='world')
    # loc.setScale((.2, .2, .2))

    return average_normal


def project_vertex(mode='Manipulator Pivot', x=None, y=None, z=None):
    """
    Will get a plane normal based on mode and project(flatten) vertices to that plane.
    :param mode: How the plane orientation is determined.
    :param x: Planer set to X axis
    :param y: Planer set to Y axis
    :param z: Planer set to Z axis
    """

    # get component data
    mesh, vertex_selection, border_selection, orig_sel, orig_sel_type = get_components()

    # Get selected Object
    mfn = mesh.__apimfn__()

    # Get Points
    points = OpenMaya.MPointArray()
    mfn.getPoints(points)
    new_points = OpenMaya.MPointArray()
    new_points.copy(points)

    # Get average Pos
    pos = get_average_pos(border_selection)

    # Get Plane Normal
    norm = None

    if mode == 'Calculate Plane':
        norm = get_plane_normal(pos, border_selection)

    elif mode == 'Manipulator Pivot':
        norm = get_manipulator_orientation()

    elif x:
        norm = OpenMaya.MVector(1.0, 0.0, 0.0)
    elif y:
        norm = OpenMaya.MVector(0.0, 1.0, 0.0)
    elif z:
        norm = OpenMaya.MVector(0.0, 0.0, 1.0)

    for vtx in vertex_selection:
        idx = vtx.index()
        vertexPos = points[idx]

        "Projection Vectors"
        # cross = norm + pos
        ''' v is the vertex vector, u is the projection plane normal'''
        v = OpenMaya.MVector(vertexPos) - pos
        u = norm

        dotProduct = u * v

        magnitude_squared = u * u

        if magnitude_squared:
            projection_scalar = dotProduct / magnitude_squared
            projection = u * projection_scalar

        else:
            projection = u

        final = vertexPos - projection

        new_points.set(final, idx)

    mfn.setPoints(new_points)

    # Restore Original Selection.
    pymel.select(orig_sel)
    set_select_type(mesh, orig_sel_type)






