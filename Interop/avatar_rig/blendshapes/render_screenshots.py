import pymel.core as pm
"""Cycles through shapes in Face_Blnd node and renders out playblasts"""


"""CONSTANTS"""
blendName = pm.aliasAttr('Face_Blnd', query=True)
time = pm.currentTime()
path = pm.mel.eval('getenv "AVATARS_V3_PERFORCE_DEPOT"')
timeline_length = 200

def cycle_blendshapes(reset=True):

    for i in range(len(blendName) / 2):

        target_name = blendName[(i * 2)]

        if check_target(target_name):
            if reset:
                print "reset!"
                pm.setAttr('Face_Blnd.' + target_name, 0)
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
    print final_path

    pm.setAttr('Face_Blnd.' + target_name, 1)

    pm.playblast(filename=final_path, startTime=0, endTime=0, format='qt', compression='h263',
                 quality=100, viewer=False, framePadding=0, widthHeight=(1024, 1024), showOrnaments=False,
                 clearCache=True, percent=100)

    pm.setAttr('Face_Blnd.' + target_name, 0)

cycle_blendshapes(reset=True)


