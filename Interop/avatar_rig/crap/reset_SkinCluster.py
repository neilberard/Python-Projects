import av_tool_funcs as funcs
import maya.api.OpenMaya as om
import pymel.core as pymel
import maya.cmds as cmds


"Copy vertex position from 1st selected item to 2nd selected item"

def getVtxPos(base) :
           
    mfnObject = om.MFnMesh(base)
    return mfnObject.getPoints()
		    		             
def setVtxPos(target,vertexPos):
                
    mfnObject = om.MFnMesh(target)
    mfnObject.setPoints(vertexPos)
    
def resetSkinCluster( skin ):
    '''
    Bakes the current pose of the skeleton into the skinCluster - ie whatever
    the current pose is becomes the bindpose
    '''
    #nInf = len( cmds.listConnections( '%s.matrix' % skin, destination=False ) )
    Inf = cmds.skinCluster(skin,q=True,inf=True)
    nInf = len(Inf)
    slotNJoint = []
	
    for n in range(nInf):
        x = '%s.matrix[ %d ]' % (skin, n)
        			
        jnt = cmds.listConnections( x, destination=False )

        if jnt is not None:
            slotNJoint = jnt[0]
            matrixAsStr = ' '.join( map( str, cmds.getAttr( '%s.worldInverseMatrix' % slotNJoint ) ) )
            melStr = 'setAttr -type "matrix" %s.bindPreMatrix[ %d ] %s' % (skin, n, matrixAsStr)
            maya.mel.eval( melStr )
            newPose = cmds.listConnections(skin,d=False,type='dagPose')
            
            if newPose is not None:
                for dPose in newPose:
                    cmds.dagPose(slotNJoint, reset=True, n=dPose)
                                  
meshes = pymel.listRelatives('Meshes', c=True)

for mesh in meshes:
    selList = om.MGlobal.getSelectionListByName(str(mesh))
    base = selList.getDagPath(0)
    vertexPos = getVtxPos(base) 
    meshSkin = funcs.get_skin_cluster(mesh)

    if meshSkin is not None:
        print 'Reset Skin Bind Pose for ' + str(mesh)
             
    resetSkinCluster(str(meshSkin))
    setVtxPos(base,vertexPos)









