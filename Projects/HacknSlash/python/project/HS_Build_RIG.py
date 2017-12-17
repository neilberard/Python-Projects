'''HSBuild_RIG'''
import pymel.core as pm

import HS_Clean as cln
import HS_Consts as cn
import HS_FK as fk
import HS_IK as ik
from interop.utils import HS_Funcs as funcs

reload(ik)

cln.cleanup()

fk.make_ctrls()
'''MIRROR'''
funcs.mirror(pm.ls('*' + cn.type['ctrl']))
funcs.mirror(pm.ls('*' + cn.name['clavicle']) + pm.ls('*' + cn.name['hip']))
'''IKFK JOINTS'''
fk.make_ik_fk_joints(pm.ls(['*' + x for x in cn.arm[1:4] + cn.leg],type='joint'))
'''FK CTRLS'''
hands = pm.ls(['*' + x + '*' for x in cn.hand], type= 'joint')
fkjoints =  pm.ls(['*' + x + cn.type['fk'] for x in cn.arm[1:4] + cn.leg], type= 'joint')
funcs.make_joint_ctrls(fkjoints,ctrlName = cn.type['ctrl'],ctrlSize = .5)
funcs.make_joint_ctrls(hands,ctrlName = cn.type['ctrl'],ctrlSize = .5)

'''IK HANDLES'''
ik.make_ik_handle(startjoint=cn.arm[1],endjoint=cn.arm[3])
ik.make_ik_handle(startjoint=cn.leg[0],endjoint=cn.leg[2])
ik.make_ik_handle(startjoint=cn.leg[2],endjoint=cn.leg[3])
ik.make_ik_handle(startjoint=cn.leg[3],endjoint=cn.leg[4])

'''OFFSET'''
funcs.create_offset_groups(Objects = pm.ls('*' + cn.type['ctrl']), offsetName = cn.type['offset'])
funcs.create_offset_groups(Objects = pm.ls('*' + cn.type['hdl']), offsetName = cn.type['offset'])


ik.ik_switch_snap()
ik.snap_ik_ctrls()
'''reconnect hands'''
fk.parent_constraint_hands()

'''connect switch'''
ik.make_switch_utility()
ik.connect_switch_utility()

'''Pole CTRLs'''
ik.snap_pole_ctrls()  
ik.group_foot_ik()            

print 'done'

