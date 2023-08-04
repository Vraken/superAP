class sourceInfo:
    def __init__(self, label, refId, link=0, avatar="📖"):
        self.__label = label
        self.__refId = refId
        self.__link = link
        self.__avatar = avatar

    @property
    def label(self):
        return self.__label

    @property
    def refId(self):
        return self.__refId

    @property
    def link(self):
        return self.__link

    @property
    def avatar(self)-> str:
        return self.__avatar