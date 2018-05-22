import pymel.core as pymel
import siteCustomize
import os
from shelves import shelf_builder

script_path = os.path.join(siteCustomize.ROOT_DIR,'shelves')


mspath = os.getenv('MAYA_SCRIPT_PATH')

new_path = "{};{}".format(mspath, script_path)
os.environ["MAYA_SCRIPT_PATH"] = new_path


pymel.evalDeferred('shelf_builder.customShelf()')