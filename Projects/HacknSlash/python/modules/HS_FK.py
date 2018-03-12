'''HS_FK'''
import pymel.core as pm

import HS_Consts as cn
import HS_Shapes as shapes
from interop.utils import HS_Funcs as funcs

'''build calls make functions'''

def parent_constraint_hands():
    wrist = pm.ls('*' + cn.name['wrist'],type = 'joint')
    hands = pm.ls(['*' + x + '_A*' + cn.type['offset'] for x in cn.hand])
    
    for h in hands:                
        for w in wrist:
            if h[0] == w[0]:                
                pm.parentConstraint(w,h, mo=True)
            
    
def build_fk_ctrls():
    
    clavicle = ['*' + cn.name['clavicle']]        
        
    fkJnts = ['*' + x + cn.type['fk'] for x in cn.arm[1:4]]
    fkJnts.extend(['*' + x + cn.type['fk'] for x in cn.leg[0:4]])

    clavCtrl = funcs.make_joint_ctrls(pm.ls(clavicle,type = 'joint'),cn.type['fk'] + cn.type['ctrl'],1)
    fkCtrl = funcs.make_joint_ctrls(pm.ls(fkJnts,type = 'joint'),cn.type['ctrl'],.5)
    
    for i in range(len(clavCtrl)):
        pm.parent(fkCtrl[i],clavCtrl[i])
    

'''Takes a list of joints duplicates Ik and FK joints from them. Parent Constraints Jnts to IK and FK Jnts'''

def make_ik_fk_joints(jnts):
   
    heirarchy = {}
     
    for obj in jnts:
        
        jnt = obj          
        chld = pm.listRelatives(jnt,c=True)         
        prnt = pm.listRelatives(jnt,p=True)           
        heirarchy[jnt]= prnt,chld
        '''UnParent'''
        if len(chld) > 0:                         
            for obj in chld:           
                pm.parent(obj, w=True)
          
        pm.parent(jnt, w=True)
        
        ik = pm.duplicate(jnt,name = jnt + cn.type['ik'])        
        fk = pm.duplicate(jnt, name = jnt + cn.type['fk'])
        contsraint = pm.parentConstraint(ik,fk,jnt,n=jnt + cn.type['const'])
                
    '''ReParent''' 
        
    for obj in heirarchy:
        j = obj                      
        p = heirarchy[obj][0]
        c = heirarchy[obj][1]
          
        if len(c) > 0 and c[0] in heirarchy.keys():
            
            pm.parent(pm.ls(str(c[0]) + cn.type['ik']),str(j) + cn.type['ik'])
            pm.parent(pm.ls(str(c[0]) + cn.type['fk']),str(j) + cn.type['fk'])
                         
        if len(c) > 0:
            for i in c:
                pm.parent(i,obj)
        if len(p) > 0:           
            pm.parent(obj,p[0])     
                          
def ctrl_name(base):
    name = cn.type['l'] + base + cn.type['ik'] + cn.type['ctrl'] 
    return name

foot_dist = funcs.get_distance(pm.ls('*Ankle')[0],pm.ls('*Toe')[0])
hand_dist = funcs.get_distance(pm.ls('*Wrist')[0],pm.ls('*Index_C')[0])

def make_ctrls():
    shapes.make_foot_ctrl(name = ctrl_name(cn.name['foot']),size = (-.06 * foot_dist,.06 * foot_dist,.06 * foot_dist),offset = (-8,0,0))
    shapes.make_cube_ctrl(name = ctrl_name(cn.name['hand']),size = (.6 * hand_dist,.5 * hand_dist,.2 * hand_dist),offset = (-22,0,0))
    
    shapes.make_diamond_ctrl(name = ctrl_name(cn.type['arm'] + cn.name['pole']),size = (.2 * hand_dist),offset = (0,0,0))
    shapes.make_diamond_ctrl(name = ctrl_name(cn.type['leg'] + cn.name['pole']),size = (.2 * hand_dist),offset = (0,0,0))
    '''Make Switch CTRLS'''

    armSwitch = shapes.make_ik_fk_swich_ctrl(name = cn.type['l'] + cn.type['arm'] + cn.name['switch'] + cn.type['ctrl'],size = (.05 * hand_dist),offset = (10,0,0))            
    legSwitch = shapes.make_ik_fk_swich_ctrl(name = cn.type['l'] + cn.type['leg'] + cn.name['switch'] + cn.type['ctrl'],size = (.05 * hand_dist),offset = (10,0,0))
    pm.select(armSwitch,legSwitch,r=True)
    pm.addAttr(ln='IKFK',min=0,max=1,at='double',k=True)
 

    