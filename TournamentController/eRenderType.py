import enum 

class eRenderType(enum.Enum): 
	Null = 0
	Muted = 1
	JustInfo = 2
	ArrayOutput = 3
	TextOutput = 4
	CustomOutput = 5
	RenderOutput = 6
	

def FromInt(value):
	if value == 0:
		return eRenderType.Null
	if value == 1:
		return eRenderType.Muted
	if value == 2:
		return eRenderType.JustInfo
	if value == 3:
		return eRenderType.ArrayOutput
	if value == 4:
		return eRenderType.TextOutput
	if value == 5:
		return eRenderType.CustomOutput
	if value == 6:
		return eRenderType.RenderOutput
