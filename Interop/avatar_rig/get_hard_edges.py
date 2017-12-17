import maya.cmds as cmds
'''Get hard edges, this is sloppy by selecting edges,
but seems to be the easiest way I have found today'''


def getInfo(sel):

    edgeCount = cmds.polyEvaluate(sel, e=True)
    cmds.select(str(sel[0]) + '.e[0:' + str(edgeCount) + ']')

    '''limit selection to hard edges with poly constraint'''
    cmds.polySelectConstraint(t=0x8000,sm=1,m=2)
    getHardEdges = cmds.ls(sl=True)
    cmds.select(r=True)

    ''' turns off poly constraint'''
    cmds.polySelectConstraint(t=0x8000,sm=1,m=0)
    cmds.select(sel,r=True)
    '''seperating hard edge number''' 
    a = [x.split('[')[1]for x in getHardEdges]
    hardEdges = [x.strip(']')for x in a]
    
    return hardEdges, edgeCount
    

'''Find meshes by matching vertex count'''

def get_target_meshes(baseObject):
    
    meshes = cmds.ls(type='transform')
    baseCount = cmds.polyEvaluate(baseObject,v=True)
    

    targets = []
    
    for i in meshes:
        if cmds.polyEvaluate(i,v=True) == baseCount:
            '''Exclude baseObject from targets list'''
            if i.find(str(baseObject[0])) == -1:
                targets.append(i)
    return targets


def apply_hard_soft_edges():
    '''grabs target meshes to match hard soft edges'''
    targets = get_target_meshes(baseObject = cmds.ls(sl=True))
    
    hardEdges,edgeCount = getInfo(sel = cmds.ls(sl=True))  
    
    for obj in targets:
        '''set all edges to 180'''
        cmds.polySoftEdge(str(obj) + '.e[0:' + str(edgeCount) + ']',angle=180,ch=1 )
        print obj
        for edge in hardEdges:
            cmds.polySoftEdge(str(obj) + '.e[0:' + str(edge) + ']',angle=0,ch=1 )
                

apply_hard_soft_edges()




