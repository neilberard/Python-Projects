import pymel.core as pm

def delete_unknown():
    
    unknown = pm.ls(type = 'unknown')
    plugs = pm.unknownPlugin(q=True,l=True)

    if len(unknown) > 0:    
       pm.lockNode(unknown,l=False )
       pm.delete(unknown)


    if plugs is not None:
        for p in plugs:
            pm.unknownPlugin(p,r=True)


def nameRef():
    all_ref = pm.listReferences()
    print all_ref[0]
 
    refNode = pm.referenceQuery(all_ref[0],rfn=True)
    refPath = pm.referenceQuery(all_ref[0],f=True,un=True)
              
    if refPath != '$AVATARS_V3_PERFORCE_DEPOT/rig/Avatar_Rig.ma':
        print 'FIX PATH'
        pm.system.cmds.file('$AVATARS_V3_PERFORCE_DEPOT/rig/Avatar_Rig.ma',loadReference= refNode,type= "mayaAscii",options ="v=0")
               
    for ref in all_ref:
        if ref.namespace == 'Avatar_Rig':
               print 'already good'
        else: 
            ref.namespace = 'Avatar_Rig'
     
        
def nameNode():
    
    sel = pm.ls('*RN')
    
    pm.lockNode(sel, lock=False)

    pm.rename(sel, 'Avatar_RigRN')

    pm.lockNode('*RN', lock=True)


path = (pm.system.cmds.file(query=True, loc=True).replace((pm.system.cmds.file(query=True,sn=True,shn=True)),''))

list = pm.system.cmds.getFileList(folder=path,fs='*ma')

nameRef()
nameNode()
delete_unknown()

for obj in list:
    delete_unknown()
    nameRef()
    nameNode()
    print (path + obj)
    pm.system.cmds.file(save=True,force=True)   
    pm.system.cmds.file((path + obj),open=True,force=True,lrd='all')

    




