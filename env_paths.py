import os

def setup_paths():
    os.environ['NB_ROOT_PATH'] = os.path.dirname(os.path.dirname(__file__)) + '\\Python_Projects'

    nb_plugins_path = os.environ['NB_ROOT_PATH'] + '\\plug-ins'

    if os.environ['MAYA_PLUG_IN_PATH']:
        os.environ['MAYA_PLUG_IN_PATH'] = '{};{};'.format(os.environ['MAYA_PLUG_IN_PATH'], nb_plugins_path)
    else:
        os.environ['MAYA_PLUG_IN_PATH'] = nb_plugins_path

