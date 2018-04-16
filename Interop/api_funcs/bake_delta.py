import maya.OpenMaya as om
import pymel.core as pymel

"Copy vertex position from 1st selected item to 2nd selected item"


def get_vtx_pos(base):
    """
    :param base: Source object.
    :return: Vertex positions as Mfn point array.
    """

    mfn_object = base.getShape().__apimfn__()
    points = om.MPointArray()
    mfn_object.getPoints(points)

    return points

def set_vtx_pos(target, points):
    """
    :param target: Target object. Must have same vertex count and order.
    :param points: Source object's vertex positions. MfnObject.getPoints()
    :return: None
    """
    mfn_object = target.getShape().__apimfn__()
    mfn_object.setPoints(points)


def run(*args):

    selection_list = pymel.selected()
    if len(selection_list) < 3:
        pymel.warning('NEED A MINIMUM OF 3 OBJECTS SELECTED. New shape, old shape, blendshape target(s)')
        return

    vertex_pos_a = get_vtx_pos(selection_list[1])
    vertex_pos_b = get_vtx_pos(selection_list[0])

    delta = [vertex_pos_a[x] - vertex_pos_b[x] for x in range(vertex_pos_a.length())]

    for idx, obj in enumerate(selection_list[:-2]):
        vertex_pos_c = get_vtx_pos(selection_list[idx + 2])

        final_pos = om.MPointArray()
        final_pos.setLength(vertex_pos_c.length())

        for x in range(final_pos.length()):

            pos = vertex_pos_c[x] - delta[x]
            final_pos.set(pos, x)

        set_vtx_pos(selection_list[idx + 2], points=final_pos)

    print '-----DONE-----'


def create_window():
    windowName = "BakeBase"

    if pymel.window(windowName, exists=True):
        print 'Check'
        pymel.deleteUI(windowName)

    window = pymel.window(windowName, t=windowName, widthHeight=(400, 50))
    pymel.columnLayout(adjustableColumn=True)

    pymel.text('Select NEW shape, OLD shape, Target(s)')
    pymel.button(label='Bake Delta', command=run)
    print 'OPEN'

    pymel.showWindow(window)


create_window()



