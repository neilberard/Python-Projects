from Projects.HacknSlash.python.project.libs import consts


class item_info(object):
    def __init__(self, str_name):
        """
        :param str_name: Name of the object to gather info.
        """
        self.name_list = str_name.split('_')
        self._side = []

    @property
    def side(self):
        for name in self.name_list:
            if name in consts.side.values():
                self._side = name
        return self._side

    @side.setter
    def side(self, value):
        self.side = value





