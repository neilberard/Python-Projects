'''HS_Funcs'''
import maya.api.OpenMaya as om
import pymel.core as pymel
import project.HS_Consts as cn


'''Better way of finding a connection by type'''           
def list_history(object, type):
    hist = pymel.listHistory(object, lv=1)
    nodes = []
    for h in hist:
        if pymel.objectType(h) == type:
            nodes.append(h) 
    return nodes   


def get_pole_position(a,b,c):
  
    vA = om.MVector(pymel.xform(a, ws=True, t=True, q=True))
    vB = om.MVector(pymel.xform(b, ws=True, t=True, q=True))
    vC = om.MVector(pymel.xform(c, ws=True, t=True, q=True))
    
    mid = (vA + vC)/2
    midVector = om.MVector.normalize(vB - mid)
    pole = (midVector * 50) + vB        
    return pole


def get_distance(a,b):
        
    vA = om.MVector(pymel.xform(a, ws=True, t=True, q=True))
    vB = om.MVector(pymel.xform(b, ws=True, t=True, q=True))
    vC = vA - vB
    return vC.length() 
    

def mirror(objects):    
    '''check which side to mirror'''        
    
    for obj in objects:
        
        if obj.find(cn.type['r']) != -1:
            side = cn.type['r'], cn.type['l']
        
        if obj.find(cn.type['l']) != -1:
            side = cn.type['l'], cn.type['r']        
        
        if pymel.nodeType(obj) == 'joint':
            
            pymel.mirrorJoint(obj, mirrorYZ=True, mb=True, sr=(side))
            
        if obj.find(cn.type['ctrl']) != -1:
             
            d = pymel.duplicate(obj)
            n = obj.replace(side[0],side[1])
            
            
            pymel.rename(d, n)
            
            if d[0].find('IKFK')== -1:                
                d[0].scaleX.set(-1)
                #d[0].scaleY.set(-1)
                pymel.makeIdentity(d[0], a=True)
                pymel.delete(obj, ch=True)
               

def group_ctrls():
    
    ctrls = pymel.ls('*' + cn.type['ctrl'], type='transform')
    hdls = pymel.ls('*' + cn.type['hdl'], type='transform')
    create_offset_groups(ctrls)
    create_offset_groups(hdls)
            
'''Parents object under an offset group and adds offset name as suffix'''
def delete_objects(transform_nodes):
    """
    deletes selected objects without deleting their children.
    :param transform_nodes: Objects to delete
    :return: None
    """
    for transform in transform_nodes:
        children = transform.getChildren()
        parent = transform.getParent()

        for child in children:
            child.setParent(parent)

        pymel.delete(transform)


def create_offset_groups(transform_nodes, group_name='_GRP'):
    """
    Parents Each object to a group node with the object's transforms.
    :param transform_nodes: list of pymel transforms to group.
    :param group_name: Suffix added.
    :return: List of offset groups.
    """

    offset_groups = []

    for transform in transform_nodes:

        transform_parent = transform.getParent()
        transform_matrix = transform.getMatrix(worldSpace=True)

        new_group = pymel.group(empty=True, name=(transform.name() + group_name))
        new_group.setMatrix(transform_matrix, worldSpace=True)

        if transform_parent:
            new_group.setParent(transform_parent)
        new_group.addChild(transform)

        offset_groups.append(new_group)

    return offset_groups


'''ctrl name is the added suffix to the  name'''
def make_joint_ctrls(jnts,ctrlName,ctrlSize):
    
    ctrlHierarchy = {}
    ctrls = []
    
    '''Running a check to make sure joints are uniquely named'''
    for obj in jnts:
        if obj.find('|') != -1:
            pymel.error(str(obj) + 'joint is not uniquely named, please rename joint')
             
    for i in range(len(jnts)):
        
        distance = 10
        prnt = pymel.listRelatives(jnts[i], p=True, type='joint')
        chld = pymel.listRelatives(jnts[i], c=True, type='joint')
        
        '''Get relative distance to determine ctrl size'''
        if len(prnt) > 0:
            distance = get_distance(prnt,jnts[i])
        
        if len(chld) > 0:      
            distance = get_distance(chld[0],jnts[i])

        '''make jnt ctrls, parent constraint joints'''        
        pos = pymel.xform(jnts[i], q=True, m=True, ws=True)
        ctrl = pymel.circle(r=distance * ctrlSize, nr=(1, 0, 0), n =str(jnts[i]) + ctrlName)
        ctrls.append(ctrl)
        pymel.xform(ctrl, m=pos, ws=True)
        pymel.parentConstraint(ctrl, jnts[i])
        
        '''assemble a list of ctrl parents'''   
        if len(prnt) > 0:                  
            ctrlHierarchy[prnt[0]] = ctrl[0]
            
    '''lists CTRL parent for dict, if found, parents CTRL to CTRL Parent.'''            
    for key in ctrlHierarchy:
                                
        ctrlParent = pymel.ls(key + ctrlName)
        ctrlChild = ctrlHierarchy[key]
      
        if len(ctrlParent) > 0:
            
            pymel.parent(ctrlHierarchy[key], ctrlParent[0])

    return ctrls

'''checks if a attribute is connected, if true, prints connection'''
def connect_attributes(a,b):
    if pymel.isConnected(a, b) is not True:
        connection = pymel.connectAttr(a, b)
        return connection 
    else:
        print str(a) + ' is already connected to ' + str(b)
         