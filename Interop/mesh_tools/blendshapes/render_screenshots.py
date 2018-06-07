import pymel.core as pymel
"""Cycles through shapes in Face_Blnd node and renders out playblasts"""


"""CONSTANTS"""
blendName = pymel.aliasAttr('Face_Blnd', query=True)
time = pymel.currentTime()
#path = pymel.mel.eval('getenv "AVATARS_V3_PERFORCE_DEPOT"')
path = 'C:/Users/v-nebera/Desktop/strips_test'
timeline_length = 200
ctrl_grp = pymel.PyNode('Ctrls_Grp')


def cycle_though_body_shape():
    for i in ctrl_grp.Proportion.getEnums():
        ctrl_grp.Proportion.set(i)
        screen_shot(i)


def cycle_blendshapes(reset=True):

    for i in range(len(blendName) / 2):

        target_name = blendName[(i * 2)]

        if check_target(target_name):
            if reset:
                print "reset!"
                pymel.setAttr('Face_Blnd.' + target_name, 0)
            else:
                screen_shot(target_name)

    if reset:
        cycle_blendshapes(reset=False)
    else:
        return


def check_target(target_name):
    if target_name.find('Eye') != -1 \
            and target_name.find('Pose') == -1:
            #or target_name.find('Nose_') != -1 \
            #or target_name.find('Ears_') != -1 \
            #or target_name.find('Jaw_') != -1 \
            #or target_name.find('Mouth_') != -1 \

        return True
    else:
        return False


def screen_shot(target_name):
    final_path = str(path) + "/ScreenShot/" + target_name

    pymel.playblast(filename=final_path, startTime=0, endTime=0, format='image', compression='png',
                    quality=100, viewer=False, framePadding=0, widthHeight=(2000, 2000), showOrnaments=False,
                    clearCache=True, percent=100)



cycle_though_body_shape()