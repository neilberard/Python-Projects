import maya.OpenMaya as om
import maya.cmds as cmds

start_time = cmds.timerX()

selection_list = om.MSelectionList()
dag_path = om.MDagPath()

om.MGlobal.getActiveSelectionList(selection_list)
selection_iterator = om.MItSelectionList(selection_list)
selection_list.getDagPath(0, dag_path)

area = 0

#iterate

while not selection_iterator.isDone():
    mesh = om.MDagPath()
    component = om.MObject()
    selection_iterator.getDagPath(mesh, component)
    
    face_iterator = om.MItMeshPolygon(mesh, component)
    face_area = om.MScriptUtil()
    face_area_double = face_area.asDoublePtr()
    
    #Iterate over each face
    while not face_iterator.isDone():
        face_iterator.getArea(face_area_double)
        area += face_area.getDouble(face_area_double)
        face_iterator.next()
    selection_iterator.next()
        
 
print 'Area = %.2f' %area
print 'Duration = %f seconds' %cmds.timerX(st=start_time)   


