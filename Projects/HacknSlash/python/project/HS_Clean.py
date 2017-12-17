'''HS_Clean'''
import HS_Consts as cn
import pymel.core as pm


def cleanup():     
        
    pm.delete(all=True,cn=True)
    pm.delete(pm.ls(type='nurbsCurve'),cn=True)
        
    ctrls = pm.ls('*' + cn.type['ctrl'])
    if len(ctrls) > 0:
        pm.delete(ctrls)
    
    lf = pm.ls('*' + cn.type['l'] + '*')
    if len(lf) > 0:
        pm.delete(lf)
                                                                   
    fk = pm.ls('*' + cn.type['fk'] + '*')
    if len(fk) > 0:
        pm.delete(fk)
    
    ik = pm.ls('*' + cn.type['ik'] + '*')
    if len(ik) > 0:
        pm.delete(ik)
    
    hdl = pm.ls(type='ikHandle')
    if len(hdl) > 0:
        pm.delete(hdl)
    
    grp = pm.ls('*' + cn.type['grp'])
    if len(grp) > 0:
        pm.delete(grp)
        
    offset = pm.ls('*' + cn.type['offset'])
    if len(offset) > 0:
        pm.delete(offset)
    
    anno = pm.ls('*' + cn.type['anno'])
    if len(anno) > 0:
        pm.delete(anno)
    
    loc = pm.ls('*' + cn.type['loc'])
    if len(loc) > 0:
        pm.delete(loc)
        
    utl = pm.ls('*' + cn.type['utility'] + '*')
    if len(utl) > 0:
        pm.delete(utl)
               
    con = pm.ls('*' + cn.type['con'] + '*')
    if len(con) > 0:
        pm.delete(con)
    


