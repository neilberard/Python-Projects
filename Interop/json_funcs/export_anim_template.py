import pymel.core as pymel
import json

def manage_ik_data(ref, ik_data, to_delete, anim_ctrls, baked_only_jnts):
    """
    This function will manage the ik data to ensure that the needed information will be exported in the fbx or
    in the JSON file generated with the animation fbx. The data include space keys, ik/fk switch keys and will
    also check if certain keys would need to be delete before the export.

    :param ref: The reference on which we want to manage the data
    :param ik_data: List containing ik data. Act like a reference
    :param to_delete: List containing object to delete. Act like a reference
    :param anim_ctrls: List containing ik ctrls to export. Act like a reference
    :param baked_only_jnts: List containing objs that should only be baked, but not expored. Act like a reference

    :return: The function will return the constraint target that come from another reference and also the target
             that are not coming from any reference and that should be exported. It will also return the ik keys,
             space keys and foot roll attributes keys needed to be exported in the JSON file
    """

    key_data = {'Controls': []}
    foot_roll_data = {
        'LeftFootProperties': [],
        'RightFootProperties': []
    }

    start_time = int(pymel.playbackOptions(q=True, min=True))
    end_time = int(pymel.playbackOptions(q=True, max=True))
    for network, ik_ctrl_data in ik_data.iteritems():
        attr_ctrl = ik_ctrl_data[0]
        ik_ctrl = ik_ctrl_data[1]
        ik_swivel = ik_ctrl_data[2]
        if attr_ctrl and ik_ctrl and ik_swivel:
            # Look for the space attribute and rename it if needed
            if hasattr(ik_ctrl, consts.ADD_SPACE_SWITCH_NAME):
                pymel.renameAttr(ik_ctrl.attr(consts.ADD_SPACE_SWITCH_NAME), consts.SPACE_SWITCH_NAME)

            # Remove the possible children from the ik_swivel which is only a line for visibility
            to_delete.extend(ik_swivel.listRelatives(type='transform'))

            # Ensure that the attribute have a key on frame 0
            ik_fk_attr = attr_ctrl.attr(self.IK_FK_ATTR_NAME)

            # Transfert the ikfk attribute to the ik ctrl to transfert it to the engine
            ikfk_keys = pymel.keyframe(attr_ctrl, q=True, attribute=self.IK_FK_ATTR_NAME, vc=True)
            ikfk_keys_time = pymel.keyframe(attr_ctrl, q=True, attribute=self.IK_FK_ATTR_NAME,
                                            tc=True)
            ikfk_value = attr_ctrl.getAttr(self.IK_FK_ATTR_NAME)
            ikfk_tangent_ix = pymel.keyTangent(attr_ctrl, at=self.IK_FK_ATTR_NAME, q=True, ix=True)
            ikfk_tangent_iy = pymel.keyTangent(attr_ctrl, at=self.IK_FK_ATTR_NAME, q=True, iy=True)
            ikfk_tangent_ox = pymel.keyTangent(attr_ctrl, at=self.IK_FK_ATTR_NAME, q=True, ox=True)
            ikfk_tangent_oy = pymel.keyTangent(attr_ctrl, at=self.IK_FK_ATTR_NAME, q=True, oy=True)

            if not ikfk_tangent_ix:
                ikfk_tangent_ix = []

            if not ikfk_tangent_iy:
                ikfk_tangent_iy = []

            if not ikfk_tangent_ox:
                ikfk_tangent_ox = []

            if not ikfk_tangent_oy:
                ikfk_tangent_oy = []

            # Do not really add the keyframe in maya but fake it in the data to prevent problem with anim layer
            if not pymel.keyframe(attr_ctrl, q=True, attribute=self.IK_FK_ATTR_NAME, time=0):
                ikfk_keys_time.insert(0, 0.0)
                ikfk_keys.insert(0, ik_fk_attr.get(time=0))
                ikfk_tangent_ix.insert(0, 1.0)
                ikfk_tangent_iy.insert(0, 0.0)
                ikfk_tangent_ox.insert(0, 1.0)
                ikfk_tangent_oy.insert(0, 0.0)

            # Always export the ik ctrl even if there is no animation on it
            anim_ctrls.append(ik_ctrl)
            anim_ctrls.append(ik_swivel)
            # If there is not keys, check the value of the ik/fk
            if not ikfk_keys:
                if ikfk_value >= 1:
                    # We still need to export the first frame of the fk, so bake it anyway
                    # baked_only_jnts.extend(network.input.get()[0:2])
                    pass
                else:
                    # Make sure the ik ctrl will be at the same position than the fk at first frame
                    ikfkTools.snap_ik_to_fk(ik_ctrl)
                    pymel.setKeyframe(ik_ctrl, time=0)
                    pymel.setKeyframe(ik_swivel, time=0)
                # Patch the values to at least export one key in JSON format
                ikfk_keys = [ikfk_value]
                ikfk_keys_time = [pymel.currentTime()]
            else:
                # Check if everything is in fk or a blend of ikfk
                if all(ikfk_keys):
                    # We will still want to bake the fk, because we need it to match the ik on frame where ik is
                    # set to ik. If we would like to only have key on the fk when there is a key in the ik/fk switch
                    # attribute, we would need to remove key after the bake part
                    # baked_only_jnts.extend(network.input.get()[0:2])
                    pass
                else:
                    # In this case, not ik keys have been set
                    if not any(ikfk_keys):
                        # Make sure the ik ctrl will be at the same position than the fk at first frame
                        if ikfk_keys_time[-1] > start_time + 1:
                            pymel.cutKey(ik_ctrl, time=(start_time + 1, ikfk_keys_time[-1]))
                            pymel.cutKey(ik_swivel, time=(start_time + 1, ikfk_keys_time[-1]))
                        else:
                            pymel.cutKey(ik_ctrl, time=(start_time + 1, end_time))
                            pymel.cutKey(ik_swivel, time=(start_time + 1, end_time))
                        ikfkTools.snap_ik_to_fk(ik_ctrl)
                        pymel.setKeyframe(ik_ctrl, time=0)
                        pymel.setKeyframe(ik_swivel, time=0)

            # Create the needed attribute on the ctrl
            if not ik_ctrl.hasAttr(self.IK_FK_ATTR_NAME):
                pymel.addAttr(ik_ctrl, longName=self.IK_FK_ATTR_NAME, type='float', k=True, h=False)

            # Build the key info for ikfk switch that will be stock in JSON format in an attribute
            ctrl_data = {'ControlName': ik_ctrl.stripNamespace().encode(),
                         'Keys': []}
            for i, (anim_time, value) in enumerate(zip(ikfk_keys_time, ikfk_keys)):
                # Skip any frame that would not be in the range of the animation
                if anim_time < float(start_time) or anim_time > float(end_time):
                    continue
                # Set the key on the attribute added
                pymel.setKeyframe(ik_ctrl, at=self.IK_FK_ATTR_NAME, t=anim_time, v=value)
                # We need to make sure the ik ctrl will be snap all place the ctrl is in fk

                inX = ikfk_tangent_ix[i]
                inY = ikfk_tangent_iy[i]
                outX = ikfk_tangent_ox[i]
                outY = ikfk_tangent_oy[i]
                time_sec = anim_time / consts.ANIM_FRAME_RATE
                ctrl_data['Keys'].append({unicode("time"): round(Decimal(time_sec), 2),
                                          unicode("value"): value,
                                          unicode("inX"): inX,
                                          unicode("inY"): inY,
                                          unicode("outX"): outX,
                                          unicode("outY"): outY})
            key_data['Controls'].append(ctrl_data)

            # Check for footroll data
            property_name, data = get_foot_roll_data(ik_ctrl)
            if property_name:
                foot_roll_data[property_name] = data

    return key_data, foot_roll_data
