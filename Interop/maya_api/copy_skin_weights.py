import pymel.core as pymel
import maya.OpenMaya as openMaya
import maya.OpenMayaAnim as openMayaAnim


def get_skin_data(mesh):
    if type(mesh) is str:
        mesh = pymel.ls(mesh)[0]
    shapeName = str(mesh)
    clusterName = str(mesh.listHistory(type='skinCluster')[0])

    selList = openMaya.MSelectionList()
    selList.add(clusterName)
    clusterNode = openMaya.MObject()
    selList.getDependNode(0, clusterNode)
    skinFn = openMayaAnim.MFnSkinCluster(clusterNode)
    infDags = openMaya.MDagPathArray()
    skinFn.influenceObjects(infDags)
    infIds = {}
    infs = []

    for x in xrange(infDags.length()):
        infPath = infDags[x].fullPathName()
        infId = int(skinFn.indexForInfluenceObject(infDags[x]))
        infIds[infId] = x
        infs.append(infPath)

    # get the mplug for weight list
    wlPlug = skinFn.findPlug('weightList')
    wPlug = skinFn.findPlug('weights')
    wlAttr = wlPlug.attribute()
    wAttr = wPlug.attribute()
    wInfIds = openMaya.MIntArray()

    weights = {}

    for vId in xrange(wlPlug.numElements()):

        vWeights = {}
        wPlug.selectAncestorLogicalIndex(vId, wlAttr)

        # indice of non zero weights
        wPlug.getExistingArrayAttributeIndices(wInfIds)

        # create a copy of the current plug
        infPlug = openMaya.MPlug(wPlug)

        for infId in wInfIds:
            # tell the infPlug it represents the current influence id
            infPlug.selectAncestorLogicalIndex(infId, wAttr)
            try:
                vWeights[infIds[infId]] = infPlug.asDouble()
            except KeyError:
                # assumes a removed influence
                pass
        weights[vId] = vWeights

    return weights


def set_skin_data(target_mesh, weights):
    """
    :param target_mesh:
    :param weights: dict from get_skin_data
    :return: None
    """

    target_skin = target_mesh.listHistory(type='skinCluster')[0]
    normalize_setting = target_skin.getNormalizeWeights()
    target_skin.setNormalizeWeights(0)

    for vertId, weightData in weights.items():
        wlAttr = '{0}.weightList[{1}]'.format(target_skin, vertId)
        for infId, infValue in weightData.items():
            wAttr = '.weights[{0}]'.format(infId)
            pymel.setAttr(wlAttr + wAttr, infValue)

    pymel.skinPercent(target_skin, normalize=True)

    print 'applying skin weights to ', target_mesh

    target_skin.setNormalizeWeights(normalize_setting)


def copy_weights_to_selected(selection):
    """
    :param selection: Select source object first then targets
    :return:
    """
    if len(selection) < 2:
        print 'Need at least 2 skinned objects selected, source and target(s). Selected object: ',
        selection

    meshes = pymel.selection

    source_mesh = meshes[0]
    target_meshes = [x for x in meshes if meshes.index(x) > 0]
    source_weights = get_skin_data(source_mesh)





