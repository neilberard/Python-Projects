import pymel.core as pymel
from python.libs import shapes
from python.libs import lib_network
from python.libs import naming_utils
from python.libs import joint_utils
reload(joint_utils)
reload(shapes)
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CreateCtrl(object):
    """
    Create a controller that can be manipulated by class properties.
    """
    def __init__(self,
                 jnt=None,
                 network=None,
                 tags=None,
                 axis='z',
                 shape='Circle',
                 size=1.0,
                 name='ctrl'):
        """
        :param jnt:
        :param network:
        :param tags:
        """

        # Ctrl Object
        self.object = None
        self.network = network
        self.tags = tags
        self.axis = axis
        self.shape = shape
        self.size = size
        self.jnt = jnt

        if self.jnt:
            self.name = name
            self.ctrl_type = None
            self.children = jnt.getChildren()
            self.parent = jnt.getParent()
            self.matrix = jnt.getMatrix(worldSpace=True)
            self.make_object()

    def make_object(self):
        if not self.shape:
            log.warning('no type specified')
        # Object

        self.object = shapes.make_shape(self.shape, self.name, self.axis)

        if not self.object:
            log.warning('Make Object: No object was returned')
            return None
        # Matrix
        if self.matrix:
            self.object.setMatrix(self.matrix, worldSpace=True)
        # Tags
        if self.tags:
            naming_utils.add_tags(self.object, self.tags)

        self.object.scale.set(self.size, self.size, self.size)
        self.freeze_transforms()

        return self.object

    def freeze_transforms(self):
        pymel.makeIdentity(self.object, apply=True, scale=True)
        pymel.delete(self.object, constructionHistory=True)

    def delete(self):
        try:
            pymel.delete(self.object)
            self.object = None
        except:
            pass


"""USAGE EXAMPLE"""
if __name__ == '__main__':

    # NET
    net = lib_network.create_network_node(name='temp',
                                          tags={'Type': 'IKFK', 'Region': 'Arm', 'Side': 'Left'},
                                          attributes=['IK', 'FK', 'IK_CTRL', 'FK_CTRL', 'POLE', 'OrientConstraint', 'PointConstraint'])

    # IK FK
    fk, ik = joint_utils.build_ik_fk_joints(pymel.ls(type='joint'), net)

    # FK CTRLS
    fk_ctrls = [CreateCtrl(jnt=jnt, network=net, tags={'Type': 'CTRL', 'Utility': 'IK'}, size=0.2, shape='Circle') for jnt in fk]

    # Parent CTRLS
    for a in fk_ctrls:
        for b in fk_ctrls:
            try:
                if a.jnt == b.parent:
                    b.object.setParent(a.object)
            except:
                pass
            try:
                if a.jnt in b.children:
                    a.object.setParent(b.object)
            except:
                pass

    # Parent constraint joints
    for a in fk_ctrls:
        pymel.parentConstraint(a.object, a.jnt)

    for a in fk_ctrls:
        a.object.addAttr('JNT', type='message')
        a.jnt.message.connect(a.object.JNT)

    # joint_utils.create_offset_groups([x.object for x in fk_ctrls])

    objects = [x.object for x in fk_ctrls]

    # Connect Message attr
    for idx, obj in enumerate(objects):
        obj.message.connect(net.FK_CTRL[idx])

    # IK CTRLS
    ikhandle = pymel.ikHandle(startJoint=ik[0], endEffector=ik[-1])[0]
    ikctrl = CreateCtrl(jnt=ikhandle, network=net, shape='Cube01', size=0.3)
    ikctrl.object.message.connect(net.IK_CTRL[0])
    pymel.pointConstraint(ikctrl.object, ikhandle)

    # POLE
    pos, rot = joint_utils.get_pole_position(fk)
    loc = pymel.spaceLocator()
    loc.setTranslation(pos, space='world')
    loc.setRotation(rot)
    loc.message.connect(net.POLE[0])
    pymel.poleVectorConstraint(loc, ikhandle)


















