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
		img = pygame.transform.scale(self.Image, [self.Scale[0]*2, self.Scale[1]*2])

		pos = [self.Pos[0]-self.Scale[0]/2, self.Pos[1]-self.Scale[1]/2]
		window.blit(img, pos)
		return
