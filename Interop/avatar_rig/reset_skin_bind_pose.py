import pymel.core as pymel
import match_vertex_position

reload(match_vertex_position)
original_vertex_position = {}


def reset_bind_pose(skin):
    """
    Reset the PreBind Matrix for skin
    :param skin: Pymel SkinCluster Node
    :return:
    """
    influences = skin.matrix.listConnections()
    dag_poses = skin.listConnections(type='dagPose', destination=False)

    for index in range(len(influences)):
        """
        Resetting Skin Defomation 
        """
        inverse_matrix = influences[index].getAttr('worldInverseMatrix')

        connections = influences[index].listConnections(plugs=True)
        for plug in connections:
            if plug.find('{}.matrix'.format(skin)) != -1:
                split01 = plug.split('[')[1]
                bind_index = int(split01.split(']')[0])
                # bind_index = int(re.findall('\d+', str(plug))[0])

        # This only works if the influence count has never changed
        skin.bindPreMatrix[bind_index].set(inverse_matrix, type='matrix')
        """
        Resetting Bind Pose, If you hit go to Bind Pose, the skeleton will now go to this pose. 
        """
        if len(dag_poses) > 0:
            for dag in dag_poses:
                pass
                pymel.animation.dagPose(dag, influences[index], reset=True)


def undo_set_vtx_pos(a=True):
    """
    Undo bake mesh position.
    :param original_pos: dict with meshes and mesh pointsvtx
    :param mesh:
    :return:
    """

    for i in pymel.selected():
        if i in original_vertex_position:
            match_vertex_position.set_vtx_pos(i, original_vertex_position[i])


def run(bake_geo=True, use_selection=True, *args):
    """
    :param bake_geo: Keeps vertex pos when resetting bind pose.
    :param use_selection: If false, function will require a list of transforms in *args
    :param args: list of transforms
    :return: None
    """

    if use_selection:
        selection = pymel.selected()
    else:
        selection = args

    for i in selection:

        if bake_geo:
            vtx_pos = match_vertex_position.get_vtx_pos(i)

        skin_cluster = i.listHistory(type='skinCluster')

        if len(skin_cluster) > 0:
            reset_bind_pose(skin_cluster[0])
        if bake_geo:
            original_vertex_position[i] = match_vertex_position.get_vtx_pos(i)
            match_vertex_position.set_vtx_pos(i, vtx_pos)

        print i, " RESET SKIN COMPLETED"


def button_run(a=True):
    run(bake_geo=True)


def button_run_no_bake(b=True):
    run(bake_geo=False)

def create_window():

    windowName = "Reset Skin Bind Pose"

    if pymel.window(windowName, exists=True):
        pymel.deleteUI(windowName)

    window = pymel.window(windowName, t=windowName, widthHeight=(400, 150))
    pymel.columnLayout(adjustableColumn=True)
    pymel.text('Select object you wish to reset')
    pymel.button(label='Reset and Bake Geo', command=button_run)
    pymel.button(label='Reset', command=button_run_no_bake)
    pymel.button(label='Undo', command=undo_set_vtx_pos)
    pymel.showWindow(window)



