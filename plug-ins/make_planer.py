import sys
import maya.OpenMayaMPx as OpenMayaMPx
import pymel.core as pymel
import maya.OpenMaya as OpenMaya


def get_average_normal(face_selection):

    average_normal = OpenMaya.MVector(0, 0, 0)
    for face in face_selection:
        average_normal += face.getNormal()

    average_normal /= len(face_selection)
    average_normal.normalize()
    return average_normal


def get_plane_normal(average_pos, vertices):
    vector_a = average_pos - OpenMaya.MVector(vertices[0].getPosition())
    vector_b = average_pos - OpenMaya.MVector(vertices[-1].getPosition())

    first_normal = vector_a ^ vector_b

    average_normal = OpenMaya.MVector(0, 0, 0)

    for idx, vtx in enumerate(vertices):

        vector_a = average_pos - OpenMaya.MVector(vertices[idx].getPosition())
        vector_b = average_pos - OpenMaya.MVector(vertices[idx-1].getPosition())

        normal = vector_a ^ vector_b
        dot = normal * first_normal

        if dot < 0:
            normal = vector_b ^ vector_a

        # final_pos = average_pos + normal
        # pymel.spaceLocator(position=(final_pos.x, final_pos.y, final_pos.z))

        average_normal += normal

    print len(vertices)
    if len(vertices):
        average_normal /= len(vertices)

    average_normal.normalize()

    return average_normal


def get_average_pos(border_vertex_selection):

    average_pos = OpenMaya.MVector(0, 0, 0)
    count = 0
    for vtx in border_vertex_selection:
        count += 1

        pos = vtx.getPosition()
        average_pos += OpenMaya.MVector(pos[0], pos[1], pos[2])

    average_pos /= count
    return average_pos


def project_vertex():

    # pymel.delete(pymel.ls(type='locator'))  # todo: TEMP

    # Get selected Object
    mesh = pymel.selected(objectsOnly=True)[0]
    mfn = mesh.__apimfn__()

    # Get selected Faces
    sel = pymel.selected()
    face_selection = sel

    # Get Points
    points = OpenMaya.MPointArray()
    mfn.getPoints(points)
    new_points = OpenMaya.MPointArray()
    new_points.copy(points)

    pymel.runtime.ConvertSelectionToVertexPerimeter()
    pos = get_average_pos(pymel.selected(flatten=True))
    norm = get_plane_normal(pos, pymel.selected(flatten=True))
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
        ''' u is the vertex vector, u is the projection plane normal'''
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

    def doIt(self, args):
        """This is called once when the command is first executed"""
        self.redoIt()

    def redoIt(self):
        self.sel = pymel.selected()
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

