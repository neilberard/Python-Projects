import sys
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import pymel.core as pymel

# MPX PLUGIN
kPluginCmdName = 'reset_vertex_position'

"Stores vertex positions of last selected object"


def get_vtx_pos(base):
    """
    :param base: PyNode
    :return: Vertex positions as Mfn point array.
    """
    try:
        mfn = base.__apimfn__()
        points = OpenMaya.MPointArray()
        mfn.getPoints(points)
    except Exception as ex:
        sys.stderr.write('Cannot get vertex pos for {}: \n {}'.format(base, ex))
        return
    return points


def set_vtx_pos(target, points):
    """
    :param target: Target object. Must have same vertex count and order.
    :param points: Source object's vertex positions. MfnObject.getPoints()
    :return: None
    """
    try:
        mfn_target = target.__apimfn__()
        mfn_target.setPoints(points)
    except Exception as ex:
        sys.stderr.write('Cannot set vertex pos for {}: \n {}'.format(target, ex))
        return


class MyUndoableCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)  # todo: from tutorial, try using the super initializer.

        self.target = None
        self.target_vtx_pos = None
        self.source = None
        self.source_vtx_pos = None

    def doIt(self, args):

        # """This is called once when the command is first executed"""
        self.redoIt()

    def redoIt(self):

        try:
            self.target = pymel.selected()[-1]

        except IndexError:
            sys.stderr.write('Need 2 meshes selected: ' + kPluginCmdName)
            return

        """Get Vertex Positions"""
        self.target_vtx_pos = get_vtx_pos(base=self.target)

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
        sys.stderr.write('failed to deregister command: ' + kPluginCmdName)

