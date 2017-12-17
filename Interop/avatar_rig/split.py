import maya.cmds as cmds
import maya.mel as mel

meshes = cmds.listRelatives('Meshes' , c= True, type='transform')

bodys = cmds.listRelatives('Avatar_Rig:Body_Grp' , c= True, type='transform')



#orig = cmds.hyperShade(objects='Avatar_Rig:Hide_Geo')


sel = cmds.ls(sl=True, type='transform')


def selectHalf(*args):

    
    verts = cmds.polyEvaluate(sel,v=True)


    #cmds.select(d=True)


    for i in range(verts -1):
        v = str(sel) + '.vtx[' + str(i) + ']'
        p = cmds.pointPosition(v)
        if p[0] >= -.001:             
            cmds.select(v, add=True)
            

    mel.eval('PolySelectConvert 10;')
    if '_F' in str(sel):
        print sel
        cmds.hyperShade( assign='Avatar_Rig:Body_Female' ) 



for i in bodys:
    sel = i
    selectHalf(sel)
'''
if '_F' in str(sel[0]):
    print sel[0]
    cmds.hyperShade( assign='Avatar_Rig:Body_Female' ) 
'''