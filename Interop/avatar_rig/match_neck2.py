import pymel.core as pymel


# Specifying matching vertex numbers for Avatars

bodyVertices = [38, 1579, 1228, 1227, 1704, 52, 1675, 1612, 293, 1580, 1673, 295, 1555, 1552, 294, 1553, 10,
                3254, 1995, 3253, 3256, 1996, 3374, 3281, 1994, 3313, 3376, 1753, 3405, 2928, 2929, 3280]
headVertices = [299, 1007, 630, 1006, 631, 1005, 633, 1004, 632, 1003, 648, 1002, 629, 1001, 628, 1000, 298,
                2000, 1666, 2001, 1667, 2002, 1686, 2003, 1670, 2004, 1671, 2005, 1669, 2006, 1668, 2007]

sel = pymel.selected()


def get_sel():

    if pymel.polyEvaluate(sel[0], v=True) == 2076:
        head = sel[0]
        body = sel[1]
    else:
        head = sel[1]
        body = sel[0]
            
    return head, body


def get_vtx_pos():

    source_vertices = []
    target_vertices = []

    for index in range(len(headVertices)):
        source_vertex = pymel.ls(str(get_sel()[0]) + 'Shape.vtx[' + str(headVertices[index]) + ']')
        target_vertex = pymel.ls(str(get_sel()[1]) + 'Shape.vtx[' + str(bodyVertices[index]) + ']')

        source_vertices.append(source_vertex)
        target_vertices.append(target_vertex)

    return source_vertices, target_vertices


def set_vtx_pos():
    source_vtx = get_vtx_pos()[0]
    target_vtx = get_vtx_pos()[1]

    for index in range(len(source_vtx)):
        target_vtx[index][0].setPosition(source_vtx[index][0].getPosition())
        print source_vtx[index][0]
        print target_vtx[index][0]


set_vtx_pos()
