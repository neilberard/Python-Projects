import sys
import maya.OpenMayaMPx as OpenMayaMPx
import pymel.core as pymel
import maya.OpenMaya as OpenMaya
import math


def get_manipulator_orientation():
    """This is a cheat until I find a better way to calculate the plane"""

    # Store original manipulator mode setting
    orig_mode = pymel.manipMoveContext('Move', query=True, mode=True)

    # Set manipulator to 'Component'
    pymel.manipMoveContext('Move', edit=True, mode=9)

    # Get manipulator Orientation
    orientation = pymel.manipMoveContext('Move', query=True, orientAxes=True)

    loc = pymel.spaceLocator(name='orientation')
    loc.setRotation([pymel.util.degrees(orientation[0]), pymel.util.degrees(orientation[1]), pymel.util.degrees(orientation[2])])

    # loc_b = pymel.spaceLocator(name='normal')
    # loc_b.setTranslation(loc.getMatrix()[0][0:3])

    values = loc.getMatrix()[0][0:3]
    pymel.delete(loc)

    return OpenMaya.MVector(values[0], values[1], values[2])


def get_average_normal(face_selection):

    average_normal = OpenMaya.MVector(0, 0, 0)
    for face in face_selection:
        average_normal += face.getNormal()

    average_normal /= len(face_selection)
    average_normal.normalize()
    return average_normal


def get_plane_normal_min_max(average_pos, verts):

    vert_positions = [v.getPosition(space='world') for v in verts]
    average_normal = OpenMaya.MVector()
    count = 0
    first_normal = None

    def min_max(axis=0):
        val = [vtx[axis] for vtx in vert_positions]
        val_min = min(xrange(len(val)), key=val.__getitem__)
        val_max = max(xrange(len(val)), key=val.__getitem__)

        dist_vector = OpenMaya.MVector(vert_positions[val_min]) - OpenMaya.MVector(vert_positions[val_max])
        print dist_vector.length(), 'Vector Length'
        return val_min, val_max, dist_vector.length()

    axis_vectors = [v for min_max(axis=v) in range(3)]
    distances = [d[2] for d in axis_vectors]
    max_dist = max(xrange(len(distances)), key=distances.__getitem__)

    # Max Cross Product

    # Cross Product
    for idx in range(3):
        values = min_max(axis=idx)

        vec_a = average_pos - OpenMaya.MVector(vert_positions[values[0]])
        vec_b = average_pos - OpenMaya.MVector(vert_positions[values[1]])

        # Skip parallel vectors
        if vec_a * vec_b == 1.0 or vec_a * vec_b == 0.0:
            continue

        # Add count for vector avarage
        count += 1
        normal = OpenMaya.MVector(vec_a ^ vec_b)
        normal.normalize()
        average_normal += normal

        # Reverse cross product if facing away from first normal
        if first_normal:
            if first_normal * normal < 0:
                normal = OpenMaya.MVector(vec_b ^ vec_a)

        if not first_normal:
            first_normal = OpenMaya.MVector(normal)

    # Divide by count
    if count:
        average_normal /= count
        average_normal.normalize()
        return average_normal
    else:
        return average_normal


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

        # if dot > 0:
        #     loc = pymel.spaceLocator()
        #     loc.setTranslation((final_pos.x, final_pos.y, final_pos.z), space='world')
        #     loc.setScale((.2, .2, .2))

        average_normal += normal

    if len(vertices):
        average_normal /= len(vertices)

    average_normal.normalize()

    final_pos = average_pos + average_normal

    loc = pymel.spaceLocator(name='normal')
    loc.setTranslation((final_pos.x, final_pos.y, final_pos.z), space='world')
    loc.setScale((.2, .2, .2))

    return average_normal


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


def project_vertex():
    for obj in pymel.ls(type='locator'):
        try:
            pymel.delete(obj.getParent())
        except:
            pass

    # Get selected Object
    mesh = pymel.selected(objectsOnly=True)[0]
    mfn = mesh.__apimfn__()

    # Get selected Faces
    sel = pymel.selected()
    face_selection = sel

    # get Norm
    # norm = get_manipulator_orientation()
    pymel.select(sel)

    # Get Points
    points = OpenMaya.MPointArray()
    mfn.getPoints(points)
    new_points = OpenMaya.MPointArray()
    new_points.copy(points)

    # Get vertex paremeter
    pymel.runtime.ConvertSelectionToVertexPerimeter()
    vertex_selection = pymel.selected(flatten=True)
    print vertex_selection

    # Get average Pos
    pos = get_average_pos(vertex_selection)
    print pos, 'pos'
    # norm = get_plane_normal(pos, vertex_selection)

    norm = get_plane_normal_min_max(pos, vertex_selection)
    # norm = get_average_normal(face_selection)


    print norm, 'norm'

    pymel.select(sel)

    pymel.runtime.ConvertSelectionToVertices()
    vert_selection = pymel.selected(flatten=True, )
    pymel.runtime.ConvertSelectionToFaces()
    pymel.select(sel)

    for vtx in vert_selection:
        idx = vtx.index()
        vertexPos = points[idx]

        "Projection Vectors"
        #cross = norm + pos
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

    return mfn, points, new_points


# MPX PLUGIN
kPluginCmdName = 'make_planer'


class MyUndoableCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)  # todo: from tutorial, try using the super initializer.

        self.mfn = None
        self.points = None
        self.new_points = None
        self.sel = None

    def doIt(self, *args):
        """This is called once when the command is first executed"""
        self.redoIt(self.sel)

    def redoIt(self, sel):
        if not sel:
            print 'Need a selection'
        self.sel = sel
        self.mfn, self.points, self.new_points = project_vertex()
        self.mfn.setPoints(self.new_points)

    def undoIt(self):
        pymel.select(self.sel)
        self.mfn.setPoints(self.points)

    def isUndoable(self):
        return True


def cmdCreator():
    return OpenMayaMPx.asMPxPtr(MyUndoableCommand())

def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(kPluginCmdName, cmdCreator)
    except:
        sys.stderr.write('Failed to register command: ' + kPluginCmdName)

def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write('failed to deregister command: ' + kPluginCmdName)

