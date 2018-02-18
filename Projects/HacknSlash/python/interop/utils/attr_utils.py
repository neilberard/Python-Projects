import pymel.core as pymel
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def unlock_attributes(nodes=None):

    """
    :param nodes: Either PyNode or List of PyNodes.
    """
    if not nodes:
        log.warning('Need selected object(s).')

    if not isinstance(nodes, list):
        nodes = list(nodes)

    for obj in nodes:
        for attr in obj.listAttr():
            try:
                attr.set(lock=False)
            except:
                pass


