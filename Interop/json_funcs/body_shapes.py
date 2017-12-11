import json
import maya.api.OpenMaya as om2
import pymel.core as pymel
import match_vertex_position

import av_tool_consts as consts
import os


MESH_DATA_PATH = os.path.join(consts.TOOL_PATH, 'libs/mesh_point_data.json')
body_mesh_group = pymel.ls(consts.BODY_MESH_GRP_NAME)


def export_body_data():
    mesh_data = {}

    for i in body_mesh_group[0].listRelatives(children=True):
        # serializing MPoint values.
        mesh_data[str(i)] = [list(x) for x in match_vertex_position.get_vtx_pos(i)]

    print mesh_data.keys()

    with open(MESH_DATA_PATH, 'w') as mesh_data_json:
        json.dump(mesh_data, mesh_data_json)


def import_body_data():
    with open(MESH_DATA_PATH, 'r') as mesh_data_json:
        mesh_data_read = json.load(mesh_data_json)
    # converting data to API 2.0 Mesh Points
    new_dict = dict((key, om2.MPointArray(mesh_data_read[key])) for key in mesh_data_read.keys())

    return new_dict
