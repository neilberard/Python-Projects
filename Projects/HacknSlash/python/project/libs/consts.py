
ALL = {}


#Base Names

TORSO = ['Pelvis', 'Spine', 'Chest', 'Clavicle']

ARM = ['Shoulder', 'Elbow', 'Wrist', 'Pole']

LEG = ['Hip', 'Knee', 'Ankle', 'Ball', 'Toe', 'Foot']

HAND = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky', 'Hand']

SIDE = ['L', 'R']

# To prevent a conflict with Left and Right naming, use numbers for indexes above 11.
INDEX = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

TYPE = ['GRP', 'JNT', 'IK', 'FK', 'CTRL', 'HDL', 'Offset', 'Annotation', 'LOC', 'Utility', 'Condition', 'Constraint',
        'Main', 'Switch', 'IKFK']

IK = ['Hand', 'Pole', 'Foot']

ALL = {'Ankle': 'Ankle',
       'Annotation': 'Annotation',
       'Ball': 'Ball',
       'CTRL': 'CTRL',
       'Chest': 'Chest',
       'Clavicle': 'Clavicle',
       'Condition': 'Condition',
       'Constraint': 'Constraint',
       'Elbow': 'Elbow',
       'FK': 'FK',
       'Foot': 'Foot',
       'GRP': 'GRP',
       'HDL': 'HDL',
       'Hand': 'Hand',
       'Hip': 'Hip',
       'IK': 'IK',
       'IKFK': 'IKFK',
       'Index': 'Index',
       'JNT': 'JNT',
       'Knee': 'Knee',
       'L': 'L',
       'LOC': 'LOC',
       'Main': 'Main',
       'Middle': 'Middle',
       'Offset': 'Offset',
       'Pelvis': 'Pelvis',
       'Pinky': 'Pinky',
       'Pole': 'Pole',
       'R': 'R',
       'Ring': 'Ring',
       'Shoulder': 'Shoulder',
       'Spine': 'Spine',
       'Switch': 'Switch',
       'Thumb': 'Thumb',
       'Toe': 'Toe',
       'Utility': 'Utility',
       'Wrist': 'Wrist',
       }

"""Test Code"""
if __name__ == '__main__':
        import itertools
        items = list(set(itertools.chain(TORSO, ARM, LEG, HAND, SIDE, TYPE, IK)))
        items.sort()

        for i in items:
                print "'{}': '{}',".format(i, i)


