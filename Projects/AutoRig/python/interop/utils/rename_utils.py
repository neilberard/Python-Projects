import maya.cmds as cmds
import pymel.core as pymel


def addSuffix(*args):
    suffix = cmds.textField("AddSuffix", query=True, text=True)
    for item in pymel.selected():
        item.rename(item.name().replace(item.name(), item.name() + suffix))
        # item.rename(item.name().replace(item.name()findName,replaceName))


def replaceName(*args):
    findName = cmds.textField("Find", query=True, text=True)
    replaceName = cmds.textField("Replace", query=True, text=True)

    for item in pymel.selected():
        item.rename(item.name().replace(findName, replaceName))


def reName(*args):
    newName = cmds.textField("Rename", query=True, text=True)

    myList = cmds.ls(sl=True)

    for x, obj in enumerate(myList):
        cmds.rename(obj, "%s%d" % (newName, x))

    print textInput


windowName = "renameObj"

if cmds.window(windowName, exists=True):
    cmds.deleteUI(windowName)

window = cmds.window(windowName, t=windowName, widthHeight=(300, 200))

cmds.columnLayout(adjustableColumn=True)
cmds.text("Find")
cmds.textField("Find")
cmds.text("Replace")
cmds.textField("Replace")
cmds.button(label='Replace', command=replaceName)

cmds.text("AddSuffix")
cmds.textField("AddSuffix")
cmds.button(label='Add Suffix', command=addSuffix)

cmds.text("Rename")
cmds.textField("Rename")
cmds.button(label='Rename', command=reName)

cmds.setParent('..')
cmds.showWindow(window)