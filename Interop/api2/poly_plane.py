import maya.api.OpenMaya as om2
import maya.cmds as cmds


def create_plane(width=2.0, uDivs=3, vDivs=100, curveName=None):
    """
    :param uDivs: faces width, min 1
    :param vDivs: faces height, min 1
    :return: plane
    """
    if not curveName:
        return

    up_vector = om2.MVector(0, 1.0, 0)

    selList = om2.MGlobal.getSelectionListByName('curve1')
    mfnCurve = om2.MFnNurbsCurve(selList.getDagPath(0))

    num_faces = uDivs * vDivs

    poly_counts = [4 for x in range(num_faces)]
    vertices = []

    u_increment = width / uDivs
    v_increment = mfnCurve.length() / vDivs

    u_offset = (width / 2.0) * -1


    for v in range(vDivs + 1):

        # ================================================
        # Curve Param
        # ================================================
        v_len = v_increment * v
        v_param = mfnCurve.findParamFromLength(v_len)
        v_curve_pos = mfnCurve.getPointAtParam(v_param, om2.MSpace.kWorld)

        # ================================================
        # Curve Direction
        # ================================================
        if v < vDivs:
            v_len_b = v_len + v_increment
            v_param_b = mfnCurve.findParamFromLength(v_len_b)
            v_curve_pos_b = mfnCurve.getPointAtParam(v_param_b, om2.MSpace.kWorld)
            dir_vector = om2.MVector(v_curve_pos_b) - om2.MVector(v_curve_pos)
            dir_vector.normalize()
            cross = up_vector ^ dir_vector

        else:
            v_len_b = v_len - v_increment
            v_param_b = mfnCurve.findParamFromLength(v_len_b)
            v_curve_pos_b = mfnCurve.getPointAtParam(v_param_b, om2.MSpace.kWorld)
            dir_vector = om2.MVector(v_curve_pos_b) - om2.MVector(v_curve_pos)
            dir_vector.normalize()
            cross = dir_vector ^ up_vector


        for u in range(uDivs + 1):
            u_pos = (u_increment * u) + u_offset
            final_pos = om2.MVector(v_curve_pos) + (cross * u_pos)
            vertices.append(om2.MPoint(final_pos))


    poly_connects = []
    start = 0

    for v in range(vDivs):
        for u in range(uDivs):

            a = u + start
            b = a + 1
            c = b + uDivs + 1
            d = a + uDivs + 1
            poly_connects.extend([a, b, c, d])


        start += (uDivs + 1)

    mesh = om2.MFnMesh()

    plane = mesh.create(vertices, poly_counts, poly_connects)



create_plane(curveName='curve1')





