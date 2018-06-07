import pymel.core as pymel
import os

from project.maya.lib.avatar import av_tool_consts as consts
from project.maya.lib.avatar import avatar_connect_visibility


def save_offsets(*args):
    sel = pymel.selected()
    pymel.select('Offset_Proportions', replace=True)
    pymel.namespace(set=':')
    path = os.path.normpath(consts.RIG_PATH + '/Extraction_Shapes/Body_Offset_Shapes.fbx')
    path = path.replace('\\', '/')

    pymel.mel.eval('FBXExport -file "{}" -s'.format(path))
    pymel.select(sel, replace=True)


def import_offsets(*args):
    ref_namespace = pymel.textField('Rig_Namespace', query=True, text=True)
    sel = pymel.selected()
    pymel.namespace(set=':')
    path = os.path.normpath(consts.RIG_PATH + '/Extraction_Shapes/Body_Offset_Shapes.fbx')
    path = path.replace('\\', '/')
    pymel.mel.eval('FBXResetImport()')
    pymel.mel.eval('FBXImport -file "{}" -s'.format(path))
    offsets = pymel.ls('Body_Grp')[0].getChildren()
    avatar_connect_visibility.connect_meshes(ref_namespace, offsets)

    pymel.select(sel, replace=True)


def remove_offsets(*args):
    if pymel.objExists('Offset_Proportions'):
        pymel.delete('Offset_Proportions')
    if pymel.objExists('Offset_BodyShapes_Lyr'):
        vis_lyr = pymel.ls('Offset_BodyShapes_Lyr')[0]
        pymel.delete(vis_lyr)


def make_window(*args):
    if pymel.namespace(exists=':Avatar_Rig'):
        namespace = 'Avatar_Rig:'

    else:
        namespace = ''

    window_name = 'offsets'
    if pymel.window('window1', exists=True):
        print 'yes!'
        pymel.deleteUI('window1')
    window = pymel.window(title=window_name, widthHeight=(250, 100))
    pymel.columnLayout(adjustableColumn=True)
    pymel.text('Rig Namespace')
    pymel.textField('Rig_Namespace', text=namespace)
    pymel.button('Import Offsets', command=import_offsets)
    pymel.button('Save Offsets', command=save_offsets)
    pymel.button('Remove_Offsets', command=remove_offsets)
    pymel.showWindow(window)


make_window()
