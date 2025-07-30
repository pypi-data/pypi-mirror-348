from enum import IntFlag


class OSI(IntFlag):
    APPLICATION = 0b1000000
    PRESENTATION = 0b100000
    SESSION = 0b10000
    TRANSPORT = 0b1000
    NETWORK = 0b100
    DATA_LINK = 0b10
    PHYSICAL = 0b1
    NONE = 0

    def __str__(self):
        return "" if self == 0 else self.name

    def __sub__(self, other):
        return self.__class__(super(OSI, self).__sub__(other))

    def __add__(self, other):
        return self.__class__(super(OSI, self).__sub__(other))
