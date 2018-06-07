import maya.api.OpenMaya as om
import maya.cmds as cmds
import re

"Plane Equation from 3 vertices, returns cross product an point positions"

def get_plane(mfnObject, vertex_A,vertex_B,vertex_C) :
               
    a = mfnObject.getPoint(vertex_A, om.MSpace.kWorld)
    b = mfnObject.getPoint(vertex_B, om.MSpace.kWorld)
    c = mfnObject.getPoint(vertex_C, om.MSpace.kWorld)
    aPos = om.MVector(a[0],a[1],a[2])
    bPos = om.MVector(b[0],b[1],b[2])
    cPos = om.MVector(c[0],c[1],c[2])
    
    caVector = om.MVector(aPos - cPos)
    cbVector = om.MVector(bPos - cPos)

    cross = om.MVector(caVector ^ cbVector)

    return aPos,bPos,cPos,cross

def project_vertex(mfnObject,cPos,cross,vertexNum):
    
    v = mfnObject.getPoint(int(vertexNum), om.MSpace.kWorld)    
    vertexPos = om.MVector(v[0],v[1],v[2])
    
    "Projection Vectors"
    u = vertexPos - cPos        
    v = cross - cPos
    
    "Project Vector Equation"
    dotProduct = cross * u

    magnitude_squared = cross.length() * cross.length()

    projection_scalar = dotProduct/magnitude_squared

    projection = cross * projection_scalar 

    final = om.MPoint(vertexPos - projection)
    
    mfnObject.setPoint(int(vertexNum),final,om.MSpace.kWorld)

    
    return vertexPos

"""Get MFnMesh"""		    		             
list = om.MSelectionList()
list.add('pPlane1')
dag = list.getDagPath(0)
mfnObject = om.MFnMesh(dag)

"""Get 3 points"""
aPos,bPos,cPos,cross = get_plane(mfnObject, vertex_A = 100,vertex_B = 10100,vertex_C = 0)

"sets up an array of vertex numbers"
selection = [re.findall('\d+', x)[1] for x in (cmds.ls(selection=True, flatten=True))]

for obj in selection:
    project_vertex(mfnObject,cPos,cross,vertexNum = obj)
    
    
