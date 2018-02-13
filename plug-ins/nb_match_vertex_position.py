import sys
import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMaya as OpenMaya2  #todo: Might want to rewrite in Maya Api 1.0 for consistancy
import pymel.core as pymel


def get_vtx_pos(base):
    """
    :param base: Source object. Can be a String, Pymel Transform Node or Maya API 2.0 dag path
    :return: Vertex positions as Mfn point array.
    """
    try:
        sel_list = OpenMaya2.MGlobal.getSelectionListByName(str(base))
        base = sel_list.getDagPath(0)
        mfn_object = OpenMaya2.MFnMesh(base)
    except:
        sys.stderr.write('Cannot get vertex pos for {}'.format(base))
        return

    return mfn_object.getPoints()


def set_vtx_pos(target, points):
    """
    :param target: Target object. Must have same vertex count and order.
    :param points: Source object's vertex positions. MfnObject.getPoints()
    :return: None
    """
    try:
        sel_list = OpenMaya2.MGlobal.getSelectionListByName(str(target))
        target = sel_list.getDagPath(0)
        mfn_object = OpenMaya2.MFnMesh(target)
        mfn_object.setPoints(points)
    except:
        sys.stderr.write('Cannot set vertex pos for {}'.format(target))


# MPX PLUGIN
kPluginCmdName = 'match_vertex_position'


class MyUndoableCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)  # todo: from tutorial, try using the super initializer.

        self.target = None
        self.target_vtx_pos = None
        self.source = None
        self.source_vtx_pos = None

    def doIt(self, args):
        """This is called once when the command is first executed"""
        self.redoIt()

    def redoIt(self):
        try:
            self.target = pymel.selected()[1]
            self.source = pymel.selected()[0]
        except IndexError:
            sys.stderr.write('Need 2 meshes selected: ' + kPluginCmdName)
            return

        """Get Vertex Positions"""
        self.target_vtx_pos = get_vtx_pos(base=self.target)
        self.source_vtx_pos = get_vtx_pos(base=self.source)

        """Set Vertex Positions"""
        set_vtx_pos(target=self.target, points=self.source_vtx_pos)


    def undoIt(self):
        set_vtx_pos(target=self.target, points=self.target_vtx_pos)


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
        sys.stderr.write( 'failed to deregister command: ' + kPluginCmdName)

