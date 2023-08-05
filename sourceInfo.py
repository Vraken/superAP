gtResources = "https://raw.githubusercontent.com/Vraken/superAP/master/"


class sourceInfo:
    def __init__(self, label, refId, tags: list, link=0, avatar="📖"):
        self.__label = label
        self.__refId = refId
        self.__tags = tags
        self.__link = link
        if "resources" in avatar:
            self.__avatar = gtResources + "/" + avatar
        else:
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
    def avatar(self) -> str:
        return self.__avatar

    @property
    def tags(self) -> list:
        return self.__tags
