class NavItem:
    def __init__(self, title: str, url: str, icon: str = None):
        self.__title = title
        self.__url = url
        self.__icon = icon

    def __eq__(self, other):
        if not isinstance(other, NavItem):
            return False
        return self.title == other.title

    @property
    def title(self) -> str:
        return self.__title

    @property
    def url(self) -> str:
        return self.__url

    @property
    def icon(self) -> str:
        return self.__icon

