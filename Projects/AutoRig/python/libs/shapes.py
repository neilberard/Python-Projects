import pymel.core as pymel
import os
import re
import siteCustomize

shapes_dir = siteCustomize.ROOT_DIR + '\\shapes'

shape_files = os.listdir(shapes_dir)


def remove_file_extension():
    return [x.replace('.ma', '') for x in shape_files]
    pass


def maintain_selection(func):
    def wrapper(*args, **kwargs):
        selection = pymel.selected()
        try:
            return func(*args, **kwargs)
        except:
            pass
        finally:
            pymel.select(selection)
    return wrapper

@maintain_selection
def make_shape(shape_type='Circle', name='Placeholder', transform=None):
    """
    Read maya ascii file and split it up by the contained mel commands.
    For every command that sets the attribute of a nurbs curve- Create a nurbs curve and set it's
    vertices based on that set attr mel command.
    This function also creates a single transform to parent the nurbs curves under.

    :param shape_type: Shape that we want to make. IE: Circle.
    :param name: Name of the new shape.
    :param transform: Transform PyNode to attach shape too.
    :return: transform node of the shape.
    """

    for shape in shape_files:
        if shape_type + '.ma' == shape:
            shape_file = os.path.join(shapes_dir, shape)

            if transform:
                transform_node = transform

            else:
                transform_node = pymel.createNode('transform', name=name)
            with open(shape_file, 'r') as s:
                mel_data = s.read().split(';')
                for mel_command in mel_data:
                    if mel_command.find('setAttr ".cc" -type "nurbsCurve"') != -1:
                        shape = pymel.createNode('nurbsCurve', name=name + 'Shape', parent=transform_node)
                        pymel.mel.eval('setAttr -k off ".v";')
                        pymel.mel.eval(mel_command + ';')

            # set_transform(transform_node, axis)

            return transform_node
    return None


def set_transform(ctrl, axis):

    if axis == 'x':
        ctrl.setRotation((90, 0, 0))

    if axis == 'y':
        ctrl.setRotation((0, 0, 0))

    if axis == 'z':
        ctrl.setRotation((0, 0, 90))

    pymel.makeIdentity(ctrl, a=True, t=1, r=1, s=1, n=0, pn=1)
    ctrl.scalePivot.translate.set(0, 0, 0)
    ctrl.rotatePivot.translate.set(0, 0, 0)


