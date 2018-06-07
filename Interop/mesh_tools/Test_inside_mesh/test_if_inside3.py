import maya.api.OpenMaya as om2
import pymel.core as pm

"""-------CONSTANTS-------"""
#: Where to find collision objects to test.
collision_group = "CollisionSpheres"

#: Time line increments to test. If set to 1, tool will test for every frame.
increment_value = 10

#: Amount off clipping that can be ignored.
clipping_threshold = 3

#: Set to 14 to cycle through all proportions
body_proportion_variants = 1

#: Output path
path = pm.mel.eval('getenv "AVATARS_V3_PERFORCE_DEPOT"')

#: Object center max test distance, this should help speed up test
max_distance = 20

""" end """


def get_mesh(mesh_name, return_type):

    """
    :param mesh_name: Requires mesh name as string value return
    :param return_type: returned type 'mesh','vertex','transform'
    :return: Maya API function based on type. None if null. 
    
    """ 
    selection_list = om2.MSelectionList()
    selection_list.add(mesh_name)
    dag_path = selection_list.getDagPath(0)

    if dag_path is None:
        return None
    
    if return_type == 'mesh':
        mesh = om2.MFnMesh(dag_path)
        return mesh
    
    if return_type == 'vertex':
        vertex = om2.MItMeshVertex(dag_path)
        return vertex
    
    if return_type == 'transform':
        transform = om2.MFnTransform(dag_path)
        return transform
    else:
        return None


def get_clipping_vertices(object_b, point_pos):
    """
    :param object_b: MfnMesh to get closest point and normal.
    :param point_pos: object_a vertex position to test if clipping.
    "return: True is vertex is clipping.
    """ 
    
    object_b_vertex = object_b.getClosestPointAndNormal(point_pos, space=om2.MSpace.kWorld)
    object_b_vertex_normal = om2.MVector(object_b_vertex[1])
    clipping_normal = om2.MVector(object_b_vertex[0] - point_pos)
    clipping_normal.normalize()
    dot_product = (clipping_normal * object_b_vertex_normal)
    if dot_product > 0:
        return True


def check_object_clipping(object_a, object_b):
    """
    :param object_a: MItmeshVertex,check if vertices are inside objectB.
    :param object_b: MFnMesh of object testing against.
    :return clipping value
    """
    
    clipping_value = 0.0
    
    while not object_a.isDone():
        point_pos = om2.MPoint(object_a.position(space=om2.MSpace.kWorld))
        if get_clipping_vertices(object_b, point_pos):
            clipping_value += 1                
        object_a.next()
    
    if clipping_value == 0:
        return None

    if clipping_value > 0:
        clipping_percent = (clipping_value / object_a.count()) * 100
        return int(clipping_percent)


def check_object_distance(mesh_a, mesh_b):

     if om2.MVector(mesh_a.boundingBox.center - mesh_b.boundingBox.center).length() > max_distance:
         return False
     return True


def gather_collision_spheres(group):
    """
    :param group: Name of group collision spheres children of.
    :returns: clipping percent, clipping objects, or None.
    """

    collision_spheres = pm.listRelatives(group, c=True, type='transform')
    if collision_spheres is None:
        return
    """
    For each base mesh, loop though query(q) meshes to determine if clipping with base(b).
    Could be sped up if checking only objects that are near each other.
    """
    for b in range(len(collision_spheres)):
        for q in range(len(collision_spheres)):
            if q + 1 < len(collision_spheres) and (q+1 != b):

                query_vertices = get_mesh(str(collision_spheres[b]), 'vertex')
                query_mesh = get_mesh(str(collision_spheres[b]), 'mesh')
                base_mesh = get_mesh(str(collision_spheres[q + 1]), 'mesh')

                if check_object_distance(query_mesh, base_mesh):
                    clipping = check_object_clipping(object_a=query_vertices, object_b=base_mesh)
                    if clipping is not None:
                        return clipping, collision_spheres[q + 1], collision_spheres[b]


def get_avatar_rig(name):
    """
    :param name: string of ctrl name
    :return: rig ctrl
    """
    avatar_rig_ctrl = pm.ls(name)
    if avatar_rig_ctrl is None:
        return None
    return avatar_rig_ctrl[0]


def cycle_time_line(rig_ctrl, increment):
    """
    :param rig_ctrl: pynode of the rig ctrl to change proportion
    :param increment: time line increment to cycle test. 1 will test every frame
    Loops though timeline. Will print out clipping info and take a screen shot if clipping is above threshold
    """

    #: Query time line length
    anim_time = int(pm.playbackOptions(q=True, animationEndTime=True))

    #: retrieves scene base name
    scene_name = pm.system.sceneName().basename().replace('.ma', '')

    #: Get sting name of proportion set.
    proportion = rig_ctrl.getAttr('Proportion', asString=True)

    for i in range(int(anim_time / increment)):

        time = pm.currentTime(i * increment)

        clipping = gather_collision_spheres(group=collision_group)

        if clipping and clipping[0] > clipping_threshold:

            #: Output name of image
            image_output = '{}--{}--{}-{}Percent_Clipping_With-{}--FRAME'.format(scene_name, proportion, clipping[1],
                                                                                 clipping[0], clipping[2])

            #: Output log info
            output_log = '{0}\n{1}\n{2} {3}\n{4}\n{5} {6}'.format(50 * "-", scene_name, clipping[0],
                                                                  "Percent is Clipping", proportion,
                                                                  clipping[1], clipping[2])

            pm.playblast(filename=str(path) + "/clipping/" + image_output, startTime=time, endTime=time, format='image',
                         compression='jpg', quality=100, viewer=False, framePadding=0, widthHeight=(1024, 1024),
                         showOrnaments=False, clearCache=True, percent=100, forceOverwrite=True)

            print output_log

    pm.currentTime(0)


def main():
    """
    Call functions to loop though proportions and timeline.
    """
    #: opens up text file
    pm.cmdFileOutput(o=str(path) + "/clipping_output.txt")

    avatar_rig_ctrl = get_avatar_rig('*:Ctrls_Grp')
    for i in range(body_proportion_variants):
        avatar_rig_ctrl.setAttr('Proportion', i)
        cycle_time_line(avatar_rig_ctrl, increment=increment_value)

    #: closes text file, DO THIS AFTER LOOPING THROUGH ALL SCENES
    pm.cmdFileOutput(ca=True)

main()


print "done"
