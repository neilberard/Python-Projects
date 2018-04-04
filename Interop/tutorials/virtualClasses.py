'''
A “virtual class” is a sub or leaf class of an existing PyNode,
defined by a user and registered within PyMEL’s PyNode factory.
Thus PyNode and any other pymel command that returns PyNodes will
return an instance of this class when called.  An example is a MetaNode.
We could have a virtual class called MetaNode that is derived from
pymel.core.nodetypes.Network, so rather than having to list all the
network nodes in a scene and cull out the MetaNodes, we can simply
ask pymel for a list of our MetaNodes.

In the attached code sample vclassample.py, we define two virtual
classes, MyVirtualNode and MyVirtualSubNode, which are derived from network nodes.
'''

import vclasssample as vcs

# create an instance of MyVirtualNode
myNode = vcs.MyVirtualNode(n='myNode')

# create an instance of MyVirtualSubNode
mySubNode = vcs.MyVirtualSubNode(n='mySubNode')

# list and filter by class type
nodes = [i for i in pm.ls(typ='network') if isinstance(i,vcs.MyVirtualNode)]
nodes
# Result: [nt.MyVirtualNode(u'myNode'), nt.MyVirtualSubNode(u'mySubNode')] #

# list with the virtual classes built-in list() method
nodes = vcs.MyVirtualNode.list()
nodes
# Result: [nt.MyVirtualNode(u'myNode'), nt.MyVirtualSubNode(u'mySubNode')] #

# virtual classes behave like other PyNodes
myNode.listAttr()
# Result: [Attribute(u'myNode.message'),
Attribute(u'myNode.caching'),
Attribute(u'myNode.isHistoricallyInteresting'),
Attribute(u'myNode.nodeState'),
Attribute(u'myNode.binMembership'),
Attribute(u'myNode.affects'),
Attribute(u'myNode.affectedBy'),
Attribute(u'myNode.myName'),
Attribute(u'myNode.myString'),
Attribute(u'myNode.myFloat'),
Attribute(u'myNode.myConnection')] #

myNode.myConnection.connect(mySubNode.myConnection)
