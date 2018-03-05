import logging
import pymel.core as pymel
import maya.OpenMaya as om
from Projects.HacknSlash.python.project.libs import consts
from Projects.HacknSlash.python.project.libs import naming_utils
from Projects.HacknSlash.python.project.libs import shapes
from Projects.HacknSlash.python.project.libs import joint_utils
reload(shapes)
reload(naming_utils)
reload(consts)
reload(joint_utils)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CreateCtrl(object):
    """
    Create a controller that can be manipulated by class properties.
    """
    def __init__(self):

        self._name = 'Placeholder'
        self._type = None
        self._object = None
        self._size = 1
        self._matrix = None
        self._axis = 'x'

    def make_object(self):
        # todo: Add a feature for importing shapes
        if not self._type:
            log.warning('no type specified')

        self._object = shapes.make_shape(self._type, self._name, self._axis)
        if not self._object:
            log.warning('No object was returned')
            return None

        if self._matrix:
            self._object.setMatrix(self._matrix, worldSpace=True)

    @property
    def object(self):
        return self._object

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        try:
            self._object.setScale([value, value, value])
        except:
            pass

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = matrix

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, axis):
        self._axis = axis

    def freeze_transforms(self):
        pymel.makeIdentity(self._object, apply=True, scale=True)
        pymel.delete(self._object, constructionHistory=True)

    def delete(self):
        try:
            pymel.delete(self._object)
            self._object = None
        except:
            pass


class ControlBuilder(object):
    """
    This class is intended to iterate on a dict of CreateCtrl class instances and values.
    """

    def __init__(self, joints=None):
        self.parent_constraint = True
        self._joints = joints
        self._ctrls = {}
        self._joint_info = {}

    @property
    def joints(self):
        return self.joints()

    @joints.setter
    def joints(self, joints):
        self._joints = joints
        self.set_ctrl_dict()
        self.set_joint_dict()

    def set_ctrl_dict(self):
        self._ctrls = {}

        # If nothing is selected, will return a single instance.
        if not self._joints:
            self._ctrls['base'] = CreateCtrl()
        else:
            for jnt in self._joints:
                self._ctrls[jnt.name()] = CreateCtrl()

    def set_joint_dict(self):
        """
        :return: skeleton_info{jnt_info:{'jnt_matrix': list, 'jnt_children': list,'jnt_parent': parent}}
        """
        self._joint_info = {}

        for jnt in self._joints:
            jnt_info = {'jnt': jnt,
                        'jnt_matrix': jnt.getMatrix(worldSpace=True),
                        'jnt_children': jnt.getChildren(),
                        'jnt_parent': jnt.getParent()}
            self._joint_info[jnt.name()] = jnt_info

    def create_ctrls(self):
        for ctrl_instance in self._ctrls.values():
            ctrl_instance.make_object()

    def get_ctrl_distance(self):
        """Retun average distance"""

        distance_tally = []

        for index in self._joint_info:

            jnt_vector = om.MVector(self._joint_info[index]['jnt'].getTranslation(space='world'))

            if self._joint_info[index]['jnt_parent']:
                jnt_parent_vector = om.MVector(self._joint_info[index]['jnt_parent'].getTranslation(space='world'))

                distanceA = om.MVector(jnt_parent_vector - jnt_vector)

                log.info(distanceA.length())
                distance_tally.append(distanceA.length())
                self._joint_info[index]['distance_sum'] = distanceA.length()

            for child in self._joint_info[index]['jnt_children']:
                child_vector = om.MVector(child.getTranslation(space='world'))
                distanceB = om.MVector(jnt_vector - child_vector)
                distance_tally.append(distanceB.length())

            if len(distance_tally) == 0:
                log.info('Could not gather distance')
                return

            self._joint_info[index]['distance_sum'] = sum(distance_tally)/len(distance_tally)

    def set_ctrl_sizes(self, size=10):

        for ctrl_instance in self._ctrls:
            try:
                self._ctrls[ctrl_instance].size = self._joint_info[ctrl_instance]['distance_sum'] * (size/100.00)
            except:
                self._ctrls[ctrl_instance].size = (size/10.00)

    def set_ctrl_axis(self, axis):
        for ctrl_instance in self._ctrls:
            self._ctrls[ctrl_instance].axis = axis

    def set_ctrl_types(self, ctrl_type):
        for ctrl_instance in self._ctrls:
            self._ctrls[ctrl_instance].type = ctrl_type

    def set_ctrl_matrices(self):
        if not self._joints:
            return
        for ctrl_instance in self._ctrls:
            self._ctrls[ctrl_instance].matrix = self._joint_info[ctrl_instance]['jnt_matrix']

    def set_ctrl_names(self):
        for ctrl_instance in self._ctrls:
            info = naming_utils.ItemInfo(ctrl_instance)  # Grabbing the object base and or jnt name.
            log.info(info.base_name)
            self._ctrls[ctrl_instance].name = naming_utils.concatenate([info.side,
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
        for ctrl_instance in self._ctrls:
            self._ctrls[ctrl_instance].freeze_transforms()
            if self._joint_info:  # If no joints are listed, skip.
                # Find the parent controller by name and parent the control to it.
                if self.parent_constraint:
                    pymel.parentConstraint(self._ctrls[ctrl_instance].object, self._joint_info[ctrl_instance]['jnt'])

                if self._joint_info[ctrl_instance]['jnt_parent']:

                    try:
                        info = naming_utils.ItemInfo(self._joint_info[ctrl_instance]['jnt_parent'])
                        ctrl_parent = naming_utils.concatenate([info.side,
                                                                info.base_name,
                                                                info.joint_name,
                                                                info.index,
                                                                consts.ALL['CTRL']])

                        # todo: write a parent setter in the base class.
                        pymel.parent(self._ctrls[ctrl_instance].object, ctrl_parent)

                    except Exception as ex:
                        # log.error(ex)
                        pass

                # find the children controllers and parent them to the control.
                for child in self._joint_info[ctrl_instance]['jnt_children']:
                    info = naming_utils.ItemInfo(child)
                    ctrl_child = naming_utils.concatenate([info.side,
                                                           info.base_name,
                                                           info.joint_name,
                                                           info.index,
                                                           consts.ALL['CTRL']])

                    try:
                        # todo: write a parent setter in the base class.
                        pymel.parent(ctrl_child, self._ctrls[ctrl_instance].object)

                    except Exception as ex:
                        # log.error(ex)
                        pass

                log.info([self._joint_info[ctrl_instance]['jnt_parent'], ':jnt_parent'])

        # Add offsets
        for ctrl_instance in self._ctrls:
            joint_utils.create_offset_groups(self._ctrls[ctrl_instance].object)

        # Removing controls
        for ctrl_instance in self._ctrls:
            self._ctrls[ctrl_instance] = None  # Release the ctrl from the dict.

    def delete_ctrls(self):
        if not self._ctrls:
            return

        for ctrl_instance in self._ctrls.values():
            if ctrl_instance:
                ctrl_instance.delete()  # deleting the shape
            del ctrl_instance  # deleting the class instance

        self._ctrls = {}  # resetting the dict








# def build_fk_ctrls(joints, ctrl_type='circle', ctrl_name='Fk', ctrl_size=1):
#     """
#
#     :param joints:
#     :param ctrl_type:
#     :param ctrl_name:
#     :param ctrl_size:
#     :return:
#     """
#     fk_ctrls = []
#     hierarchy = {}
#
#     for jnt in joints:
#         ctrl_name = jnt.name() + '_FK'  # todo: add a naming function.
#         # Getting joint info.
#         jnt_matrix = jnt.getMatrix(worldSpace=True)
#         jnt_children = jnt.getChildren()
#         jnt_parent = jnt.getParent()
#
#         # Making controller.
#         ctrl = create_ctrl(ctrl_type, ctrl_size, ctrl_name=ctrl_name)
#         ctrl.setMatrix(jnt_matrix, worldSpace=True)
#         pymel.parentConstraint([ctrl, jnt])
#         fk_ctrls.append(ctrl)
#
#         # Rebuild hierarchy
#
#         if jnt_parent:
#             parent_ctrl_name = ctrl_name.replace(jnt.name(), jnt_parent.name())  # Trying to find name of parent ctrl
#             try:
#                 parent_ctrl = pymel.PyNode(parent_ctrl_name)
#                 ctrl.setParent(parent_ctrl)
#             except pymel.MayaNodeError:
#                 pass
#
#         if jnt_children:
#             for jnt_child in jnt_children:
#                 child_ctrl_name = ctrl_name.replace(jnt.name(), jnt_child.name())  # Trying to find name of child ctrl
#                 try:
#                     child_ctrl = pymel.PyNode(child_ctrl_name)
#                     child_ctrl.setParent(ctrl)
#                 except pymel.MayaNodeError:
#                     pass
#
#         return fk_ctrls



"""TEST CODE"""

if __name__ == '__main__':

    vector = om.MVector(1, 0, 0)

    ctrl_builder = ControlBuilder(pymel.selected())
    ctrl_builder.set_ctrl_types('Circle')
    ctrl_builder.get_ctrl_distance()


    ctrl_builder.create_ctrls()
    ctrl_builder.set_ctrl_sizes()






    # jnt_dict = get_joint_hierarchy(joints=pymel.selected())
    # ctrls = build_ctrls(joints=pymel.selected())
    #
    # for obj in ctrls:
    #     print jnt_dict[obj]['jnt_matrix']
    #
    #     ctrls[obj].type = 'Diamond'
    #     ctrls[obj].matrix = jnt_dict[obj]['jnt_matrix']
    #     ctrls[obj].make_object()

        # obj.type = 'Circle'
        # obj.make_object()










