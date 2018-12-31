import maya.api.OpenMaya as om2
import maya.cmds as cmds

uDivs = 1
vDivs = 1


indices = []
value = 0

def create_plane(uDivs=3, vDivs=3):
    """
    :param uDivs: faces width, min 1
    :param vDivs: faces height, min 1
    :return: plane
    """

    num_faces = uDivs * vDivs

    poly_counts = [4 for x in range(num_faces)]
    vertices = []

    u_increment = 1.0
    v_increment = 1.0

    name_value = 0

    for v in range(vDivs + 1):

        for u in range(uDivs + 1):

            u_pos = u_increment * u
            v_pos = v_increment * v * -1.0

            name = "loc_{}".format(name_value)
            name_value += 1
            vertices.append(om2.MPoint(u_pos, 0.0, v_pos, 0.0))

            # cmds.spaceLocator(position=(u_pos, 0.0, v_pos), name=name)

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

    mesh.create(vertices, poly_counts, poly_connects)


    print poly_connects

create_plane()



#
#
# poly_counts = [4, 4]
#
# vertices = [om2.MPoint(0, 0, 0, 0),
#           om2.MPoint(1.0, 0, 0, 0),
#           om2.MPoint(0, 1.0, 0, 0),
#           om2.MPoint(1.0, 1.0, 0, 0),
#           om2.MPoint(0, 2.0, 0, 0),
#           om2.MPoint(1.0, 2.0, 0, 0)]
#
# poly_connects = [0, 1, 3, 2,
#                  2, 3, 5, 4]
#
# mesh = om2.MFnMesh()
#
# mesh.create(vertices, poly_counts, poly_connects)

