import pymel.core as pm
import av_tool_consts as consts
import json_funcs
import os

sel = pm.selected(flatten=True)

num_a = [x.split('[')[1] for x in sel]
num_b = [int(x.split(']')[0]) for x in num_a]


TAILOR_TOOL_DATA_PATH = os.path.join(consts.TOOL_PATH, 'libs/tailortool_data.json_funcs')

with open(TAILOR_TOOL_DATA_PATH, 'r') as tailor_tool_json:
    data = json_funcs.load(tailor_tool_json)

for idx, (color_name, color_data) in enumerate(data.iteritems()):
    print color_name

new = data['COLOR_02']['m_indices']

print new

for i in new:
    print i


for i in num_b:
    new.append(i)

new.sort()

print new
data['COLOR_02']['m_indices'] = new

with open(TAILOR_TOOL_DATA_PATH, 'w') as tailor_tool_json:
    json_funcs.dump(data, tailor_tool_json)