import pymel.core as pymel
import maya.OpenMaya as OpenMaya

face_selection = pymel.selected(flatten=True)
mesh = pymel.PyNode('pSphere1')
mesh_mfn = mesh.getShape().__apimfn__()


def get_average_normal(face_selection):

    average_normal = OpenMaya.MVector(0, 0, 0)
    for face in face_selection:
        average_normal += face.getNormal()

    average_normal /= len(face_selection)
    average_normal.normalize()
    return average_normal


def get_average_pos(border_vertex_selection):

    average_pos = OpenMaya.MVector(0, 0, 0)

    for vtx in border_vertex_selection:
        pos = vtx.getPosition()
        average_pos += OpenMaya.MVector(pos[0], pos[1], pos[2])

    average_pos /= len(border_vertex_selection)
    return average_pos


def project_vertex():
    sel = pymel.selected()
    mfn = mesh.getShape().__apimfn__()
    points = OpenMaya.MPointArray()
    mfn.getPoints(points)
    new_points = OpenMaya.MPointArray()
    new_points.copy(points)

    norm = get_average_normal(face_selection)
    pymel.runtime.ConvertSelectionToVertexPerimeter()
    pos = get_average_pos(pymel.selected())

    pymel.select(sel)
    pymel.runtime.ConvertSelectionToVertices()
    vert_selection = pymel.selected(flatten=True)
    pymel.select(sel)



    for vtx in vert_selection:
        idx = vtx.index()

        vertexPos = points[idx]
        "Projection Vectors"
        #cross = norm + pos
        ''' u is the vertex vector, u is the projection plane normal'''
        v = OpenMaya.MVector(vertexPos) - pos
        u = norm

        dotProduct = u * v

        magnitude_squared = u * u

        projection_scalar = dotProduct / magnitude_squared
        projection = u * projection_scalar

        final = vertexPos - projection

        new_points.set(final, idx)

    return new_points


finalArray = project_vertex()

mesh_mfn.setPoints(finalArray)



