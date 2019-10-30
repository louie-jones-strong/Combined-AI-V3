import pygame
import RenderEngine.PieceBase as Piece
import RenderEngine.Shape as Shape


def LoadImage(path):
	return pygame.image.load(path)


class ImagePiece(Piece.PieceBase):

	def __init__(self, pos, scale, image, rotate=0, infoObject=None):
		super().__init__(pos, scale, Shape.Square(), rotate, infoObject)
		self.Image = image
		return

	def Draw(self, window):
		window.blit(self.Image, self.Pos)
		return
