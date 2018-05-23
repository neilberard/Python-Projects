import pymel.core as pymel
from python.libs import naming_utils


def get_network_node(src_obj, node_type):
    for connection in src_obj.listConnections():
        if connection.hasAttr('Type') and connection.Type.get() == node_type:
            return connection


def get_message_connection(src_obj):
    print src_obj.message.listConnections(plugs=True)


def create_network_node(name, tags, attributes=None):
    """

    :param name: str
    :param tags: dict{'Region': 'Arm', 'Side': 'R', 'Type': 'IK'}
    :param attributes: list['_IK', '_FK', _IKCTRL, _FKCTRL]
    :return: network
    """
    if pymel.objExists(name):
        network = pymel.PyNode(name)
    else:
        network = pymel.createNode('network')
        pymel.rename(network, name)

    naming_utils.add_message_attr(network, attributes)
    naming_utils.add_tags(network, tags)

    return network