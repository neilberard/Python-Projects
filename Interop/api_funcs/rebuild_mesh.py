from api_funcs import core as api_core
import maya.api.OpenMaya as om2

reload(api_core)
plane_mesh = api_core.get_mesh(mesh_name='pPlane1', return_type='mesh')
plane_face2 = api_core.get_mesh(mesh_name='pPlane2', return_type='face')

polygon_connects = om2.MIntArray()
polygon_counts = om2.MIntArray([4, 4, 4, 4])
face_ids = om2.MIntArray()
vertex_pos = om2.MPointArray()
face_connects = om2.MIntArray()

# build arrays
while not plane_face2.isDone():
    face_ids.append(plane_face2.faceId())
    vertex_pos.append(plane_face2.position(space=om2.MSpace.kWorld))
    face_connects.append(plane_face2.vertexId())

    plane_face2.next()

print face_ids
print vertex_pos
print face_connects

"""
for i in range(len(face_ids)):
    if face_ids[i] == 1:
        face_ids.insert(face_ids[i],0)
        face_ids.remove(i+1)
        face_connects.insert(face_connects[i],0)
        face_connects.remove(i+1)
        vertex_pos.insert(vertex_pos[i],0)
        vertex_pos.remove(i+1)

"""

plane_mesh.createInPlace(vertex_pos, polygon_counts, face_connects)

