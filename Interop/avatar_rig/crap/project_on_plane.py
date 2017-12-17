import maya.cmds as cmds
import maya.api.OpenMaya as om


aPos = om.MVector(cmds.xform(cmds.ls('A')[0],q=True,ws=True,t=True))
bPos = om.MVector(cmds.xform(cmds.ls('B')[0],q=True,ws=True,t=True))
cPos = om.MVector(cmds.xform(cmds.ls('C')[0],q=True,ws=True,t=True))
pPos = om.MVector(cmds.xform(cmds.ls('P')[0],q=True,ws=True,t=True))
"Cross product, plane"
baPos = om.MVector(aPos - bPos)
bcPos = om.MVector(cPos - bPos)

cross = (baPos ^ bcPos)

"Get the normal vector of the plane"
bCross = cross

cmds.xform(cmds.ls('Normal')[0], t=normal , ws=True)

"Projection Vectors"
u = pPos - bPos
v = bCross - bPos

dotProduct = bCross * u

magnitude_squared = bCross.length() * bCross.length()

projection_scalar = dotProduct/magnitude_squared

projection = bCross * projection_scalar 



final = pPos - projection


cmds.xform(cmds.ls('projection')[0], t=projection, ws=True)
cmds.xform(cmds.ls('Final')[0], t= (final[0],final[1],final[2]), ws=True)




