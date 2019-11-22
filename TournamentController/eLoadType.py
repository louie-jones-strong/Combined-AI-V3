import enum


class eLoadType(enum.Enum):
	Null = 0
	Load = 1
	NotLoad = 2


def FromInt(value):
	if value == 0:
		return eLoadType.Null
	if value == 1:
		return eLoadType.Load
	if value == 2:
		return eLoadType.NotLoad
