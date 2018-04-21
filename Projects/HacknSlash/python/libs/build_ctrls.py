import logging
import pymel.core as pymel
import maya.OpenMaya as om
from python.libs import consts, naming_utils
from python.libs import shapes
from python.libs import joint_utils
from python.libs import lib_network
reload(shapes)
reload(naming_utils)
reload(consts)
reload(joint_utils)
reload(lib_network)

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
        :param axis: 'X', 'Y', 'Z', Use Z to align with limb, Y to align to world
        """

        # Ctrl Object
        self.object = None
        self.network = network
        self.tags = tags
        self.axis = axis
        self.shape = shape
        self.size = size
        self.jnt = jnt
        self.matrix = [1.0, 0.0, 0.0, 0.0,
                       0.0, 1.0, 0.0, 0.0,
                       0.0, 0.0, 1.0, 0.0,
                       0.0, 0.0, 0.0, 1.0]
        self.name = name

        if self.jnt:
            self.ctrl_type = None
            self.children = jnt.getChildren()
            self.parent = jnt.getParent()
            self.matrix = jnt.getMatrix(worldSpace=True)
            self.make_object()

        else:
            self.make_object()

        if self.object and self.network:
            naming_utils.add_tags(self.object, {'Network': self.network.name()})


    @property
    def message(self):
        return self.object.message

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

    def get_ctrl_distance(self):
        """Retun average distance"""

        jnt_vector = om.MVector(self.jnt.getTranslation(space='world'))
        distance_tally = []

        if self.parent:
            parent_vector = om.MVector(self.parent.getTranslation(space='world')) - jnt_vector
            distance_tally.append(parent_vector.length())

        if self.children:
            child_vector = om.MVector(self.children[0].getTranslation(space='world')) - jnt_vector
            distance_tally.append(child_vector.length())

        if len(distance_tally) > 0:
            return sum(distance_tally)/len(distance_tally)

        else:
            return None

    def freeze_transforms(self):
        pymel.makeIdentity(self.object, apply=True, scale=True)
        pymel.delete(self.object, constructionHistory=True)

    def delete(self):
        try:
            pymel.delete(self.object)
            self.object = None
        except:
            pass


class ControlBuilder(object):
    """
    This class is intended to iterate on a dict of CreateCtrl class instances and values.
    """

    def __init__(self, joints=None, network=None, ctrl_type=None):
        self.joints = joints
        self.network = network
        self.parent_constraint = True
        self.ctrls = {}


    def set_ctrl_list(self):
        self.ctrls = {}

        # If nothing is selected, will return a single instance.
        if not self.joints:
            self.ctrls['base'] = CreateCtrl()
        else:
            for jnt in self.joints:
                self.ctrls[jnt.name()] = CreateCtrl()

    def set_ctrl_sizes(self, size=10):
        for x in self.ctrls.values():
            print x.get_ctrl_distance()

        # for ctrl_instance in self.ctrls:
        #     try:
        #         self.ctrls[ctrl_instance].size = self._joint_info[ctrl_instance]['distance_sum'] * (size / 100.00)
        #     except:
        #         self.ctrls[ctrl_instance].size = (size / 10.00)

    def set_ctrl_axis(self, axis):
        for ctrl_instance in self.ctrls:
            self.ctrls[ctrl_instance].axis = axis

    def set_ctrl_names(self):
        for ctrl_instance in self.ctrls:
            info = naming_utils.ItemInfo(ctrl_instance)  # Grabbing the object base and or jnt name.
            log.info(info.base_name)
            self.ctrls[ctrl_instance].name = naming_utils.concatenate([info.side,
                                                                       info.base_name,
                                                                       info.joint_name,
                                                                       info.index,
                                                                       consts.ALL['CTRL']])

    def publish_ctls(self):
        """
        If joints or objects are listed, this will parent constrain them to the corresponding controllers.
        The self._ctrls dict is flushed to release the controllers from the tool.
        """

        # Parent controllers
        for ctrl_instance in self.ctrls:
            self.ctrls[ctrl_instance].freeze_transforms()
            if self._joint_info:  # If no joints are listed, skip.
                # Find the parent controller by name and parent the control to it.
                if self.parent_constraint:
                    pymel.parentConstraint(self.ctrls[ctrl_instance].object, self._joint_info[ctrl_instance]['jnt'])

                if self._joint_info[ctrl_instance]['jnt_parent']:

                    try:
                        info = naming_utils.ItemInfo(self._joint_info[ctrl_instance]['jnt_parent'])
                        ctrl_parent = naming_utils.concatenate([info.side,
                                                                info.base_name,
                                                                info.joint_name,
                                                                info.index,
                                                                consts.ALL['CTRL']])



                        # todo: write a parent setter in the base class.
                        pymel.parent(self.ctrls[ctrl_instance].object, ctrl_parent)

                    except Exception as ex:
                        # log.error(ex)
                        pass

                # find the children controllers and parent them to the control.
                for child in self._joint_info[ctrl_instance]['jnt_children']:
                    try:
                        info = naming_utils.ItemInfo(child)
                        ctrl_child = naming_utils.concatenate([info.side,
                                                               info.base_name,
                                                               info.joint_name,
                                                               info.index,
                                                               consts.ALL['CTRL']])
                    except:
                        pass  # todo: Add support for non joint objects

                    try:
                        # todo: write a parent setter in the base class.
                        pymel.parent(ctrl_child, self.ctrls[ctrl_instance].object)

                    except Exception as ex:
                        # log.error(ex)
                        pass

                log.info([self._joint_info[ctrl_instance]['jnt_parent'], ':jnt_parent'])

        # Add Tags
        try:
            for ctrl_instance in self.ctrls:
                naming_utils.add_tags(self.ctrls[ctrl_instance].object,
                                      {'Region': info.region,
                                       'Name': info.base_name,
                                       'Joint': info.joint_name,
                                       'Index': info.index,
                                       'Side': info.side,
                                       'Type': consts.ALL['CTRL'],
                                       'Utility': consts.ALL['FK']})
        except:
            pass

        # Add offsets
        for ctrl_instance in self.ctrls:
            joint_utils.create_offset_groups(self.ctrls[ctrl_instance].object)

        # Removing controls
        for ctrl_instance in self.ctrls:
            self.ctrls[ctrl_instance] = None  # Release the ctrl from the dict.

    def delete_ctrls(self):
        if not self.ctrls:
            return

        for ctrl_instance in self.ctrls.values():
            if ctrl_instance:
                ctrl_instance.delete()  # deleting the shape
            del ctrl_instance  # deleting the class instance

        self.ctrls = {}  # resetting the dict


"""TEST CODE"""

if __name__ == '__main__':

    ctrls = CreateCtrl(jnt=pymel.selected()[0])
    print ctrls.get_ctrl_distance()









