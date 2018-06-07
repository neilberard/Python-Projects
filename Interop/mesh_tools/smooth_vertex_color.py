import pymel.core as pm
import maya.api.OpenMaya as Om2
import api_funcs
import distance_falloff
reload(distance_falloff)

start_time = pm.timerX()


mesh = api_funcs.get_mesh('pSphere1', 'mesh')
api_vertex = api_funcs.get_mesh('pSphere1', 'vertex')
mesh_vector_array = Om2.MVectorArray(mesh.getPoints())
color_array = mesh.getVertexColors()
vtx = mesh.numVertices
vertices = [x for x in range(vtx)]
final_color_array = color_array

max_dist = .5


def smooth_vertex_with_falloff():


    #dist = Om2.MVector()
    for vtx_a in xrange(vtx):
        near_colors = Om2.MColorArray()
        near_distances = []
        for vtx_b in xrange(vtx):
            dist = mesh_vector_array[vtx_a] - mesh_vector_array[vtx_b]
            if dist.length() < max_dist:
                near_distances.append(dist.length())
                near_colors.append(color_array[vtx_b])

        final_color_array[vtx_a] = distance_falloff.get_falloff(near_distances, near_colors)

    return final_color_array


def smooth_vertex_color():

    for i in xrange(vtx):

        b = Om2.MColor()
        color_num = 0
        api_vertex.setIndex(i)
        connected = api_vertex.getConnectedVertices()

        for vertex in range(len(connected)):
            color_num += 1
            b += color_array[connected[vertex]]

        final_color_array[i] = b / color_num

    return final_color_array

mesh.setVertexColors(smooth_vertex_with_falloff(), vertices)
#mesh.setVertexColors(smooth_vertex_color(), vertices)
    
print "done"
print 'Duration = %f seconds' %pm.timerX(st=start_time)
    





