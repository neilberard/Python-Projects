import maya.api.OpenMaya as om2
import pymel.core as pm
"Copy vertex position from 1st selected item to 2nd selected item"

def create_window():
    
    windowName = "BakeBase"
    
    if pm.window(windowName, exists=True):
        print 'Check'
        pm.deleteUI(windowName)
    
    window = pm.window(windowName, t=windowName,widthHeight=(400, 50))
    pm.columnLayout( adjustableColumn=True )
                 
    pm.text('Select NEW shape, OLD shape, Target(s)')
    pm.button( label='Bake Delta', command='run()')
          
    pm.showWindow( window )
    
create_window()

def get_vtx_pos(base):
    """
    :param base: Source object.
    :return: Vertex positions as Mfn point array.
    """
           
    mfn_object = om2.MFnMesh(base)
    return mfn_object.getPoints()


def set_vtx_pos(target, points):
    """
    :param target: Target object. Must have same vertex count and order.
    :param points: Source object's vertex positions. MfnObject.getPoints()
    :return: None
    """
    mfn_object = om2.MFnMesh(target)
    mfn_object.setPoints(points)
    
def run():
    selection_list = om2.MGlobal.getActiveSelectionList()
    
    if selection_list.length() <3:
        pm.warning('NEED A MINIMUM OF 3 OBJECTS SELECTED. New shape, old shape, blendshape target(s)')
        return
    else:
        vertex_pos_a = get_vtx_pos(base=selection_list.getDagPath(1))
        vertex_pos_b = get_vtx_pos(base=selection_list.getDagPath(0))
        
        delta = [vertex_pos_a[x] - vertex_pos_b[x] for x in range(len(vertex_pos_a))] 
                
        
        for i in range(selection_list.length() -2):
            
            vertex_pos_c = get_vtx_pos(base=selection_list.getDagPath(i+2))
            finalPos = [vertex_pos_c[x] - delta[x] for x in range(len(vertex_pos_a))]
            set_vtx_pos(target=selection_list.getDagPath(i+2), points=finalPos)
    
    print '-----DONE-----'            
             
