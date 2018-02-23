import pymel.core as pymel
import maya.api.OpenMaya as om2

"""NOT UNDOABLE"""
def mfn_object(mesh):
    sel_list = om2.MGlobal.getSelectionListByName(mesh.name())
    base = sel_list.getDagPath(0)
    mfn_object = om2.MFnMesh(base)
    return mfn_object

  
selected = pymel.selected()

source_dag = mfn_object(selected[0])
source_uvs = source_dag.getUVs()

for obj in selected:
    dag = mfn_object(obj)
    dag.setUVs(source_uvs[0], source_uvs[1], uvSet='map1') 




