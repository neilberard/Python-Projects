import pymel.core as pymel

ffd = pymel.ls(type='lattice')
for obj in ffd:
    con = obj.listConnections(d=True)
    for i in con:
        
        pymel.rename(i, 'ffd_' + obj)
        
        set = i.message.listConnections(d=True)
        for s in set:
            pymel.rename(s, 'set_' + obj)
            print s