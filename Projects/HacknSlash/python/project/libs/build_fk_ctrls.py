import pymel.core as pymel


def create_circle(size):
    circle = pymel.circle()
    return circle

def build_fk_ctrls(jnt, ctrl, **kwargs):
    """

    :param joints:
    :param ctrl_size:
    :return:
    """

    jnt_matrix = jnt.getMatrix(worldSpace=True)
    jnt_children = jnt.getChildren()
    jnt_parent = jnt.getParent()







for i in range(len(jnt)):
    pos = cmds.xform(jnt[i],q=True,m=True,ws=True)   
    c = cmds.circle(r=3,nr=(1,0,0), n=str(jnt[i]) + cn.basetype['fk']+ cn.basetype['ctrl'])
    cmds.xform(c,m=pos,ws=True)
    cmds.parentConstraint(c,jnt[i])
    
    p = cmds.listRelatives(jnt[i],p=True)
    if p is not None:
        j = (p,cmds.ls(c)[0])
        jntParent.append(j)

for i in range(len(jntParent)):
    jp = cmds.ls(str(jntParent[i][0][0]) + cn.basetype['fk'] + cn.basetype['ctrl'])     
    jc = jntParent[i][1]
    cmds.parent(jc,jp)