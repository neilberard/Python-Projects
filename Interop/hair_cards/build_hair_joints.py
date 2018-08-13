import pymel.core as pymel
import pymel.core.datatypes as dt
import operator


def build_matrix(a, b, c):
    """
    :param a: x_axis pos
    :param b: y_axis pos
    :param c: base pos
    :return: transform matrix
    """
    x = a - c
    y = b - c
    z = x ^ y

    pos = c + (x * .5)  # Center of hair card width

    x.normalize()
    y.normalize()
    z.normalize()

    return dt.Matrix(x, y, z, [pos.x, pos.y, pos.z])


def build_card_joint_chain(card):
    """
    :param card: Hair card: plane with divisions, must have uvs.
    :return: joint chain
    """
    uv_list = []

    # Sort UV base of values of both axis
    for vtx in card.vtx[:]:
        uv_list.append([vtx.getUVs()[0][0], vtx.getUVs()[1][0], vtx])

    uv_list.sort(key=operator.itemgetter(0, 1))

    # Get number of columns
    column_count = 0
    for idx in uv_list:
        if uv_list[0][1] == idx[1]:
            column_count += 1

    # Need logic for multiple rows,
    row_length = len(uv_list) / column_count
    offset_length = row_length * (column_count - 1)

    hair_joints = []

    for i in range(row_length):
        c = uv_list[i][2].getPosition(space='world')
        a = uv_list[i + offset_length][2].getPosition(space='world')

        # If at the end of the list, get previous pos instead and reverse Y vector.
        if i + 2 > row_length:
            b = uv_list[i - 1][2].getPosition(space='world')
            matrix = build_matrix(a, b, c)
            matrix[1:3] *= -1

        else:
            b = uv_list[i + 1][2].getPosition(space='world')
            matrix = build_matrix(a, b, c)

        hair_joint = pymel.joint()
        hair_joint.setMatrix(matrix, worldSpace=True)
        hair_joint.setRadius(0.2)

        # moving joint rotation into joint orientation.
        pymel.makeIdentity(hair_joint, apply=True, translate=True, rotate=True, scale=True)
        hair_joints.append(hair_joint)

    return hair_joints


# Example use
if __name__ == '__main__':
    sel = pymel.selected()
    pymel.select(None)

    for obj in sel:
        build_card_joint_chain(obj)
        pymel.select(None)

    pymel.select(sel)