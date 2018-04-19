import pymel.core as pm
import maya.OpenMaya as OpenMaya
import pymel.core.runtime as pmr
start_time = cmds.timerX()

#pmr.ConvertSelectionToVertexPerimeter()

sel = OpenMaya.MSelectionList()
OpenMaya.MGlobal.getActiveSelectionList(sel)



path, comp = sel.getComponent(0)
iter = OpenMaya.MItMeshVertex(path, comp)
mesh = OpenMaya.MFnMesh(path)

pointPosArray = mesh.getPoints()
normalArray = mesh.getNormals()
vertexArray = mesh.getPoints(OpenMaya.MSpace.kWorld)


"""Get selection average normal and position"""

def get_average_vector():
    
    averageNormal = OpenMaya.MVector(0, 0, 0)
    averagePosition = OpenMaya.MVector(0, 0, 0)
    norm = []
    pos = []

    while not iter.isDone():

        averageNormal[0] += normalArray[iter.index()][0]
        averageNormal[1] += normalArray[iter.index()][1]
        averageNormal[2] += normalArray[iter.index()][2]
    
        averagePosition[0] += iter.position()[0]
        averagePosition[1] += iter.position()[1]
        averagePosition[2] += iter.position()[2]
        
        iter.next()

    pos = averagePosition/iter.count()
    norm = averageNormal/iter.count()
    return pos,norm

def project_vertex():
    
    pos,norm = get_average_vector()
    iter.reset()

    while not iter.isDone():
        vertexPos = vertexArray[iter.index()]
        "Projection Vectors"
        cross = norm + pos
        ''' u is the vertex vector, u is the projection plane normal'''
        v = OpenMaya.MVector(vertexPos) - pos
        u = norm
        
        dotProduct = u * v

        magnitude_squared = u * u

        projection_scalar = dotProduct/magnitude_squared
        projection = u * projection_scalar
        
        final = vertexPos - projection

        vertexArray[iter.index()] = final
        iter.next()
    return vertexArray
    
finalArray = project_vertex()       

mesh.setPoints(finalArray)   

print 'Duration = %f seconds' %cmds.timerX(st=start_time)