import pymel.core as pymel
from project.maya.lib.avatar import lib_av_naming
from project.maya.lib.avatar import av_tool_consts


body_meshes = pymel.listRelatives('Body_Grp')


def export_fbx():

    for mesh in body_meshes:

        info = lib_av_naming.Asset_Name(mesh)

        if info.proportion == 'Base':
            continue

        head_name = lib_av_naming.concatenate_str_from_list(['Head',
                                                             info.proportion,
                                                             info.gender,
                                                             ])

        head = pymel.PyNode(head_name)

        try:
            mesh.visibility.disconnect()
            mesh.visibility.set(1)
            head.visibility.set(1)
        except:
            pass

        pymel.select(mesh, r=True)
        pymel.select(head_name, add=True)

        file_name = []

        if mesh.find('_Body_M_Mesh') != -1:
            file_name = mesh.replace('_Body_M_Mesh', '_M.fbx')
        if mesh.find('_Body_F_Mesh') != -1:
            file_name = mesh.replace('_Body_F_Mesh', '_F.fbx')

        path = 'C:/Users/v-nebera/avatars_p4/rig/bodyshapes_FBX/' + file_name

        pymel.mel.FBXExport(s=True, f=path)


if __name__ == '__main__':
    export_fbx()




