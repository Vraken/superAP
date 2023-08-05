class tagWithColor:
    def __init__(self, label, color):
        self.__label = label
        self.__color = color

    @property
    def label(self):
        return self.__label

    @property
    def color(self):
        return self.__color
