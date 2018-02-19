

class item_info(object):
    def __init__(self, str_name):
        """
        :param str_name: Name of the object to gather info.
        """
        self.name_list = str_name.split('_')
        self._side = []

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        self.side = value





