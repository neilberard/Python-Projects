import pymel.core as pm
from libs import lib_av_deformer

sel = pm.ls(selection=True)
print type(sel)

def get_meshes():
    if type(sel) != 'list':
        pm.warning('need vertex selection')
        return
    else:
        print 'good'

get_meshes()

#lib_av_deformer.copy_weights_per_vertid( )
