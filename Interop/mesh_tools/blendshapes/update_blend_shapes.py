import pymel.core as pm
from PyQt5 import configure

configure

import os

omit_list = ('NoseVolume', 'Head_Mesh_Open', 'Head_Mesh_Fix', 'Head_Mesh', 'EarVolumes')

target_objs = pm.fileDialog2(fm=4, ff='*.obj, *.Obj')

final_list = target_objs
for obj in omit_list:
    for i in target_objs:
        if i.find(obj) != -1:
            print i
            final_list.remove(i)

final_list.sort()
meshes = []
original_object_sets = pm.ls(type='objectSet')


def import_file(current_file):
    pm.importFile(obj_file, force=True, options='mo=0')
    base_name = os.path.basename(current_file)
    return base_name.replace('.obj', '')

for obj_file in final_list:
    all_transforms_before = pm.ls(type='mesh')
    mesh_name = import_file(current_file=obj_file)
    imported_objects = [x for x in pm.ls(type='mesh') if x not in all_transforms_before]
    imported_object_sets = [x for x in pm.ls(type='objectSet') if x not in original_object_sets]
    pm.delete(imported_object_sets)
    pm.rename(imported_objects[0].getParent(), mesh_name)
    meshes.append(mesh_name)


pm.select(meshes)


