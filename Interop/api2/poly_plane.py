import maya.api.OpenMaya as om2
import maya.cmds as cmds


def create_plane(uDivs=4, vDivs=100, curveName=None):
    """
    :param uDivs: faces width, min 1
    :param vDivs: faces height, min 1
    :return: plane
    """
    if not curveName:
        return

    selList = om2.MGlobal.getSelectionListByName('curve1')
    mfnCurve = om2.MFnNurbsCurve(selList.getDagPath(0))


    num_faces = uDivs * vDivs

    poly_counts = [4 for x in range(num_faces)]
    vertices = []

    u_increment = 1.0
    v_increment = mfnCurve.length() / vDivs


    for v in range(vDivs + 1):

        for u in range(uDivs + 1):

            u_pos = u_increment * u
            v_pos = v_increment * v * -1.0

            #================================================
            # Curve Param
            #================================================
            v_len = v_increment * v
            v_param = mfnCurve.findParamFromLength(v_len)
            v_curve_pos = mfnCurve.getPointAtParam(v_param)

            vertices.append(om2.MPoint(u_pos + v_curve_pos.x, 0.0, v_curve_pos.z, 0.0))


    poly_connects = []
    start = 0

    for v in range(vDivs):
        for u in range(uDivs):

            a = u + start
            b = a + 1
            c = b + uDivs + 1
            d = a + uDivs + 1
            poly_connects.extend([a, b, c, d])
            print [a, b, c, d]

        start += (uDivs + 1)

    mesh = om2.MFnMesh()

    plane = mesh.create(vertices, poly_counts, poly_connects)


    print poly_connects


create_plane(curveName='curve1')





