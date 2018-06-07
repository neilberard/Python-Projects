import pymel.core as pymel

pymel.mel.eval('CreateWrap;')

pymel.deformer('pSphere2',type='wrap')

src = pymel.PyNode('src')

if not pymel.attributeQuery('influence', n=src, exists=True):
    src.addAttr('influence', keyable=True, defaultValue=2)
    
if not pymel.attributeQuery('smoothness', n=src, exists=True):
    src.addAttr('smoothness', keyable=True, defaultValue=0)

if not pymel.attributeQuery('dropoff', n=src, exists=True):
    src.addAttr('dropoff', keyable=True, defaultValue=0)