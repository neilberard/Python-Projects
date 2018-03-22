
ALL = {}


#Base Names
REGIONS = ['Arm', 'Foot', 'Hand', 'Leg', 'Side', 'Torso']

ARM = ['Shoulder', 'Elbow', 'Wrist']

FOOT = ['Ball', 'Toe', 'Foot']

HAND = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

LEG = ['Hip', 'Knee', 'Ankle']

SIDE = ['L', 'R']

TORSO = ['Pelvis', 'Spine', 'Chest', 'Clavicle']

# KEYS for item Tags.
TAGS = ['Side', 'Region', 'Type', 'Utility']

# To prevent a conflict with Left and Right naming, use numbers for indexes above 11.
INDEX = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

TYPE = ['GRP', 'JNT', 'CTRL', 'HDL', 'Offset', 'Annotation', 'LOC', 'Utility', 'Condition', 'Constraint',
        'Main', 'Switch']

UTILITY = ['IK', 'FK', 'IKFK']  # What does the object deal with

IK = ['Hand', 'Pole', 'Foot']

ALL = {'Ankle': 'Ankle',
       'Annotation': 'Annotation',
       'Arm': 'Arm',
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
       'Leg': 'Leg',
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
       'Torso': 'Torso',
       'Utility': 'Utility',
       'Wrist': 'Wrist',
       }

"""test Code"""

# NETWORK




if __name__ == '__main__':
        import itertools
        items = list(set(itertools.chain(TORSO, ARM, LEG, HAND, SIDE, TYPE, IK)))
        items.sort()

        for i in items:
                print "'{}': '{}',".format(i, i)


