import pymel.core as pm

i = []

ctrl = pm.ls('Ctrls_Grp')

b = pm.listRelatives('Body_Grp')
ctrl = pm.ls('Ctrls_Grp')


def export_fbx():

    for i in b:
        if i.visibility.get():
            pm.select(i, r=True)
            pm.select('Head_Mesh', add=True)

            if i.find('_Body_M_Mesh') != -1:
                x = i.replace('_Body_M_Mesh', '_M.fbx')
            if i.find('_Body_F_Mesh') != -1:
                x = i.replace('_Body_F_Mesh', '_F.fbx')

            path = 'C:/Users/v-nebera/avatars_p4/rig/bodyshapes_FBX/' + x
            print path
            pm.mel.FBXExport(s=True, f=path)


for i in range(14):
    ctrl[0].Proportion.set(i)
    export_fbx()

for i in range(14):
    ctrl[0].Proportion.set(i)
    export_fbx()
            


