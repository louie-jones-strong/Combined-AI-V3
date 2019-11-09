import enum 

class eRenderType(enum.Enum): 
	Muted = 0
	JustInfo = 1
	ArrayOutput = 2
	TextOutput = 3
	CustomOutput = 4
	RenderOutput = 5
	

def FromInt(value):
	if value == 0:
		return eRenderType.Muted
	if value == 1:
		return eRenderType.JustInfo
	if value == 2:
		return eRenderType.ArrayOutput
	if value == 3:
		return eRenderType.TextOutput
	if value == 4:
		return eRenderType.CustomOutput
	if value == 5:
		return eRenderType.RenderOutput
