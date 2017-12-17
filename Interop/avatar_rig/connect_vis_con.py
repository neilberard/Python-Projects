import pymel.core as pymel
import av_tool_consts as consts
reload(consts)
"""
For use on AVATAR RIG only
Attempts to connect VIS CONDITION nodes to visibility SELECTED objects based on Names.
Example: If selected object name contains "Average_F", tool will connect
that VIS CONDITION to the visibility of that object. 
"""
conditions = []


def connect():
    proportions = []
    proportions.extend([x + '_M' for x in consts.MALE_BODY_PROPORTION.keys()])
    proportions.extend([x + '_F' for x in consts.FEMALE_BODY_PROPORTION.keys()])

    namespace = ''

    if pymel.namespace(exists=':Avatar_Rig'):
        namespace = 'Avatar_Rig:'

    sel = pymel.selected()

    for i in proportions:
        items = '{0}{1}*Vis_Cond'.format(namespace, i)
        print items, 'CONDITION'
        conditions.extend(pymel.ls(items))
        print conditions

    for con in conditions:
        remove_namespace = con.replace(namespace, '')

        base_name = remove_namespace.replace('_Vis_Cond', '')

        #stupid code to deal with body shapes cause who needs naming conventions?

        base_name = base_name.replace('_F', '_Body_F')
        base_name = base_name.replace('_M', '_Body_M')


        for s in sel:
            if s.find(base_name) != -1:
                con.outColor.outColorR.connect(s.visibility, force=True)
                print base_name, s




