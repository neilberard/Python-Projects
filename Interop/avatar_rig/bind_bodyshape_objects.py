import pymel.core as pymel

"""
USE WITH AVATAR_RIG

First selected object needs to be skinned.

Script will bind body shape meshes to the rig using the influences from the first 
selected mesh. This is to ensure influence count will match.
"""

selection = pymel.selected()
ctrl = pymel.ls('Ctrls_Grp')

base_skin = selection[0].listHistory(type='skinCluster')[0]
base_shape = selection[0].getChildren()[0]
base_shape.numVertices()
base_influences = base_skin.getInfluence()

for i in range(14):

    ctrl[0].Proportion.set(i)
    print i
    for obj in selection:
        if obj.visibility.get() and obj is not selection[0]:
            if len(obj.listHistory(type='skinCluster')) < 1:
                pymel.skinCluster(obj, base_influences, tsb=True, mi=4, omi=True)

