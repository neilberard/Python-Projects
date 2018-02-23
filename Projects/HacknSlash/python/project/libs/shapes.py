import pymel.core as pymel


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
def make_circle():
    circle = pymel.circle(normal=(1, 0, 0))[0]
    return circle

@maintain_selection
def make_cube_ctrl(name):
    pos = [(-1, 1, 1), (-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1), (-1, -1, 1), (-1, -1, -1),
           (-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (1, -1, 1),
           (1, -1, -1)]
    knot = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    ctrl = pymel.curve(n=name, d=1, p=pos, k=knot)
    return ctrl

@maintain_selection
def make_ik_fk_swich_ctrl(name, size, offset):
    pos = [(-9.088573, 11.596919, 0), (-9.088573, 18.149395, 0), (-8.178507, 18.149395, 0), (-8.178507, 11.596919, 0),
           (-9.088573, 11.596919, 0), (-6.449382, 11.596919, 0), (-6.449382, 18.149395, 0),
           (-5.539316, 18.149395, 0), (-5.539316, 14.917238, 0), (-5.539316, 11.596919, 0), (-6.449382, 11.596919, 0),
           (-5.539316, 11.596919, 0), (-5.539316, 14.925771, 0), (-2.900124, 18.149395, 0), (-1.958775, 18.149395, 0),
           (-4.511226, 15.030996, 0), (-1.523649, 11.596919, 0), (-2.718112, 11.596919, 0), (-5.539316, 14.917238, 0),
           (-2.718112, 11.596919, 0), (-1.523649, 11.596919, 0), (-0.533953, 11.596919, 0), (-0.533953, 18.149395, 0),
           (3.106311, 18.149395, 0), (3.106311, 17.421343, 0), (0.376113, 17.421343, 0), (0.376113, 15.237184, 0),
           (2.671186, 15.237184, 0), (2.671186, 14.50913, 0), (0.376113, 14.50913, 0), (0.376113, 11.596919, 0),
           (-0.533953, 11.596919, 0), (0.376113, 11.596919, 0), (4.380404, 11.596919, 0), (4.380404, 18.149395, 0),
           (5.29047, 18.149395, 0), (5.29047, 14.917238, 0), (7.929662, 18.149395, 0), (8.871011, 18.149395, 0),
           (6.318559, 15.030996, 0), (9.306136, 11.596919, 0), (8.111673, 11.596919, 0), (5.29047, 14.925771, 0),
           (5.29047, 11.596919, 0), (4.380404, 11.596919, 0)]

    knot = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44)
    ctrl = pymel.curve(n=name, d=1, p=pos, k=knot)
    set_transform(ctrl, size, offset)
    return ctrl

@maintain_selection
def make_diamond_ctrl(name):
    ctrl = pymel.curve(n=name, d=1, p=[(0, 0, 1), (0, 1, 0), (0, 0, -1), (0, -1, 0), (0, 0, 1)], k=[0, 1, 2, 3, 4])
    return ctrl

@maintain_selection
def make_foot_ctrl(name):
    ctrl = pymel.circle(r=1, nr=(0, 1, 0), n=name)[0]
    pos = [(8.0, 0.0, -9.0), (-19.0, 0.0, -4.0), (-22.0, 0.0, -3.0), (-23.0, 0.0, 0.0),
           (-22.0, 0.0, 3.0), (-19.0, 0.0, 4.0), (8.0, 0.0, 9.0), (12.0, 0.0, 0.0)]

    for i in range(len(ctrl.cv)):
        pymel.move(ctrl.cv[i], pos[i], ws=True)

    ctrl.setScale([.1, .1, .1])
    pymel.makeIdentity(ctrl, apply=True)

    return ctrl


def set_transform(ctrl, size, offset):
    if len(str(size).split(',')) == 1:
        size = size, size, size

    ctrl.scale.set(size)
    ctrl.translate.set(offset)

    pymel.makeIdentity(ctrl, a=True, t=1, r=1, s=1, n=0, pn=1)
    ctrl.scalePivot.translate.set(0, 0, 0)
    ctrl.rotatePivot.translate.set(0, 0, 0)

def make_shape(type, name):

    if type == 'Circle':
        return make_circle()

    if type == 'Diamond':
        return make_diamond_ctrl(name)

    if type == 'Foot':
        return make_foot_ctrl(name)

    if type == 'Cube':
        return make_cube_ctrl(name)


