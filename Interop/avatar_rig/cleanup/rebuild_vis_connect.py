import pymel.core as pymel

from project.maya.lib.avatar import avatar_connect_visibility

sel = pymel.selected()
for i in sel:
    connections = i.visibility.listConnections()
    i.visibility.disconnect()
    
    for con in connections:
        if not con.isReferenced():
            pymel.delete(con)
            
    
avatar_connect_visibility.run('Avatar_Rig:',sel)
