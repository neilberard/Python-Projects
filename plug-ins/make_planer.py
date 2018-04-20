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
    average_normal = OpenMaya.MVector(0, 0, 0)
    count = 0

    for idx, vtx in enumerate(vertices):

        vector_a = OpenMaya.MVector(vertices[idx-1].getPosition()) - average_pos
        vector_b = OpenMaya.MVector(vertices[1].getPosition()) - average_pos

        count += 1
        average_normal += vector_a ^ vector_b
    print count
    if count:
        average_normal /= count
    average_normal.normalize()

    return average_normal


def get_average_pos(border_vertex_selection):

    average_pos = OpenMaya.MVector(0, 0, 0)
    count = 0
    for vtx in border_vertex_selection:
        count += 1

        pos = vtx.getPosition()
        average_pos += OpenMaya.MVector(pos[0], pos[1], pos[2])

    print count

    average_pos /= count
    return average_pos


def project_vertex():

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
    # norm = get_plane_normal(pos, [pymel.PyNode('pSphere1.vtx[293]'), pymel.PyNode('pSphere1.vtx[298]')])
    norm = get_average_normal(pymel.selected(flatten=True))
    # norm = OpenMaya.MVector(0,1,0)

    pymel.select(sel)
    pymel.runtime.ConvertSelectionToVertices()
    vert_selection = pymel.selected(flatten=True)
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

        projection_scalar = dotProduct / magnitude_squared
        projection = u * projection_scalar

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

    def doIt(self, args):
        """This is called once when the command is first executed"""
        self.redoIt()

    def redoIt(self):

        self.mfn, self.points, self.new_points = project_vertex()
        self.mfn.setPoints(self.new_points)

    def undoIt(self):
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

