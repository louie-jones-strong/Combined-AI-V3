import RenderEngine.Piece.ImagePiece as ImagePiece

class CardPieceMaker:

	def __init__(self):
		self.CardCache = {}
		return

	def GetCard(self, Suit, Value, pos, scale, rotate=0, showFace=False):
		if showFace:
			key = "CardBack"
		else:
			key = str(Suit)+"_"+str(Value)

		if key in self.CardCache:
			image = self.CardCache[key]

		else:
			path = "Assets\\Images\\Cards\\"
			path += str(key) + ".png"
			image = ImagePiece.LoadImage(path)
			self.CardCache[key] = image

		return ImagePiece.ImagePiece(pos, scale, image, rotate)
