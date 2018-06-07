import maya.cmds as cmds
import pymel.core as pm
from libs import lib_av_deformer as funcs

'''
Transfer weights of selected vertices to similar meshes(same vert count)
Make sure to have vertices you wish to transfer selected before running.

NOTE: This was written in Pymel, so the script will run very slow if there
are is a large selection of vertices. I intend to update with Maya Api in 
the future.

'''
def get_vertex_specs(sel):

    skin = sel[0].listHistory(type='skinCluster')









def get_vertex_info(sel):
    
    baseVerts = []
    shape = pm.listRelatives(sel[0],p=True)
    baseObj = pm.listRelatives(shape,p=True)
    skC = str(sel[0].listHistory(type='skinCluster')[0])
    baseCount = pm.polyEvaluate(baseObj,v=True)

    vtxInf = pm.skinPercent(skC, v, query=True, ib=0.0000001, t=None)
    vtxVal = pm.skinPercent(skC, v, query=True, ib=0.0000001, v=True)

    for vtx in sel:
        print vtx
        
        for v in vtx:
            print skC
            
            vtxNum = v.replace(str(shape) + '.vtx','')
            print vtxNum

            '''Query vertex influence name'''

            '''Query vertex influence value'''

            all = (vtxNum,vtxInf,vtxVal)
            baseVerts.append(all)
    
    return baseVerts,baseObj,baseCount


'''find similar meshes in the scene based on vert count'''
def get_target_meshes(baseCount,baseObject):
    
    mesh = pm.ls(type='transform')

    targets = []
    
    for i in mesh:
        if pm.polyEvaluate(i,v=True) == baseCount:
            '''Exclude baseObject from targets list'''
            if i.find(str(baseObject[0])) == -1:
                targets.append(i)
    return targets

'''Remove weights from target verts'''
def remove_vertex_weight(baseVerts,target):
    
    targetSkc = funcs.get_skin_cluster(target)
    '''TURN OFF normalize skin weights'''
    targetSkc.normalizeWeights.set(0)
    
    print target
    
    for i in range(len(baseVerts)):
                       
        targetVtx = str(target) + 'Shape.vtx' + str(baseVerts[i][0])
        targetInf = pm.skinPercent(targetSkc, targetVtx, query=True, ib=0.0000001,t=None)
        
        '''Iterate through target vertex influences and sets them to zero.'''
        
        if targetInf is not None:
            for inf in range(len(targetInf)):
                pm.skinPercent(targetSkc,targetVtx,transformValue=[targetInf[inf],0])
        
        for inf in range(len(baseVerts[i][1])):
            pm.skinPercent(targetSkc,targetVtx,transformValue=[baseVerts[i][1][inf],baseVerts[i][2][inf]])
    '''TURN ON normalize skin weights'''        
    targetSkc.normalizeWeights.set(1)                        


'''needs vertex selection of a skinned object''' 
sel = pm.ls(sl=True)

'''get vert number,vert influnces,influence values'''
baseVerts,baseObject,baseCount = (get_vertex_info(sel))

"""

targets = get_target_meshes(baseCount,baseObject)


for obj in targets:
    remove_vertex_weight(baseVerts,obj)

"""
                
   

