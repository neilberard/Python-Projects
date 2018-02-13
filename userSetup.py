import os

"""Setup paths"""

os.environ['NB_ROOT_PATH'] = os.path.dirname(os.path.dirname(__file__))

nb_plugins_path = os.environ['NB_ROOT_PATH'] + r'\Introp'

if os.environ['MAYA_PLUGINS_PATH']:
    os.environ['MAYA_PLUGINS_PATH'] = ''.format(os.environ['MAYA_PLUGINS_PATH'])
