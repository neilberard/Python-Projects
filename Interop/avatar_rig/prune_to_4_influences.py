import maya.cmds as cmds


'''Prunes weights of smallest infuences if count is higher than 4 on a 
selected object. Will print out vtx number if greater than 4 influences'''

sel = cmds.ls(sl=True)

def pruneWeights(vtxIndexList, sel, skin):
        
    for vtxNum in vtxIndexList:
    
        vtx = sel + '.vtx[' + str(vtxNum) + ']'
        
        if skin > 0:     
            
            infCount = cmds.skinPercent( skin[0],vtx, ignoreBelow=0.00000001, query=True, value=True )
            
            max = 0; 
            
            while len(infCount) > 4 and max<100:
                print len(infCount), vtx
                max += 1
                pruneVal = min(infCount)
        
                cmds.skinPercent( skin[0],vtx, pruneWeights=pruneVal + .05)      
                infCount = cmds.skinPercent( skin[0],vtx, ignoreBelow=0.00000001, query=True, value=True )

    print 'Max skin influences pruned to 4 or less', sel         
            
            
#gets skinClusters for selected objects           
    
def getInf(sel):
    for obj in sel:
        shapeNode = cmds.listRelatives(obj,s=True, ni=True)
        skin = cmds.listConnections(shapeNode, t='skinCluster')
        vtxIndexList = cmds.getAttr( obj+".vrts", multiIndices=True )                
        pruneWeights(vtxIndexList, obj, skin)
 
            
getInf(sel)