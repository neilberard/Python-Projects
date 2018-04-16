import sys
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import pymel.core as pymel


def get_vtx_pos(base):
    """
    :param base: Source object. Can be a String, Pymel Transform Node or Maya API 2.0 dag path
    :return: Vertex positions as Mfn point array.
    """
    try:
        mfn = base.getShape().__apimfn__()
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
        mfn_target = target.getShape().__apimfn__()
        mfn_target.setPoints(points)
    except Exception as ex:
        sys.stderr.write('Cannot set vertex pos for {}: \n {}'.format(target, ex))
        return


# MPX PLUGIN
kPluginCmdName = 'bake_delta'


class BakeDelta(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

        self.target = None
        self.target_vtx_pos = None
        self.source = None
        self.source_vtx_pos = None
        self.stored_positions = []
        self.selection_list = []

    def doIt(self, args):
        """This is called once when the command is first executed"""
        self.redoIt()

    def redoIt(self):
        self.stored_positions = []

        self.selection_list = pymel.selected()
        if len(self.selection_list) < 3:
            pymel.warning('NEED A MINIMUM OF 3 OBJECTS SELECTED. New shape, old shape, blendshape target(s)')
            return

        vertex_pos_a = get_vtx_pos(self.selection_list[1])
        vertex_pos_b = get_vtx_pos(self.selection_list[0])
        delta = [vertex_pos_a[x] - vertex_pos_b[x] for x in range(vertex_pos_a.length())]

        for idx, obj in enumerate(self.selection_list[:-2]):
            vertex_pos_c = get_vtx_pos(self.selection_list[idx + 2])
            self.stored_positions.append(vertex_pos_c)

            final_pos = OpenMaya.MPointArray()
            final_pos.setLength(vertex_pos_c.length())

            for x in range(final_pos.length()):
                pos = vertex_pos_c[x] - delta[x]
                final_pos.set(pos, x)

            set_vtx_pos(self.selection_list[idx + 2], points=final_pos)

    def undoIt(self):
        for idx, obj in enumerate(self.selection_list[:-2]):
            set_vtx_pos(self.selection_list[idx + 2], points=self.stored_positions[idx])

    def isUndoable(self):
        return True


def cmdCreator():
    return OpenMayaMPx.asMPxPtr(BakeDelta())

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

