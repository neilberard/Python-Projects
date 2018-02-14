import maya.api.OpenMaya as om2
import pymel.core as pymel

"Copy vertex position from 1st selected item to 2nd selected item"


original_vertex_position = {}


def get_vtx_pos(base):
    """
    :param base: Source object. Can be a String, Pymel Transform Node or Maya API 2.0 dag path
    :return: Vertex positions as Mfn point array.
    """
    try:
        sel_list = om2.MGlobal.getSelectionListByName(str(base))
        base = sel_list.getDagPath(0)
        mfn_object = om2.MFnMesh(base)
    except:
        pass

    return mfn_object.getPoints()


def set_vtx_pos(target, points):
    """
    :param target: Target object. Must have same vertex count and order.
    :param points: Source object's vertex positions. MfnObject.getPoints()
    :return: None
    """

    if type(target) == str or type(target) == pymel.nodetypes.Transform:
        sel_list = om2.MGlobal.getSelectionListByName(str(target))
        target = sel_list.getDagPath(0)
        print type(target)

    mfn_object = om2.MFnMesh(target)
    mfn_object.setPoints(points)


def undo_set_vtx_pos(*args):
    """
    Undo bake mesh position.
    :param original_pos: dict with meshes and mesh pointsvtx
    :param mesh:
    :return:
    """
    for i in original_vertex_position:
        set_vtx_pos(i, original_vertex_position[str(i)])


def run(*args):
    selection_list = om2.MGlobal.getActiveSelectionList()
    vertex_pos = get_vtx_pos(base=selection_list.getDagPath(0))
    set_vtx_pos(target=selection_list.getDagPath(1), points=vertex_pos)


def button_run(a=True):
    run()

def create_window():

    windowName = "Match Vertex Position"

    if pymel.window(windowName, exists=True):
        pymel.deleteUI(windowName)

    window = pymel.window(windowName, t=windowName, widthHeight=(400, 150))
    pymel.columnLayout(adjustableColumn=True)
    pymel.text('Select Source Mesh then Target')
    pymel.button(label='Match', command=run)
    pymel.button(label='Undo', command=undo_set_vtx_pos)
    pymel.showWindow(window)


