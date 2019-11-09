import pygame
import RenderEngine.Piece.PieceBase as Piece


class PolygonPiece(Piece.PieceBase):

	def __init__(self, pos, scale, points, color, fill=True, rotate=0, infoObject=None):
		super().__init__(pos, scale, points, rotate, infoObject)

		self.Color = color
		self.Fill = fill
		return

	def Draw(self, window):
		borderColor = [0, 0, 0]

		points = self.GetRotatedPoints()

		if self.Fill and len(points) >= 3:
			pygame.gfxdraw.filled_polygon(window, points, self.Color)

		if len(points) >= 3:
			pygame.gfxdraw.aapolygon(window, points, borderColor)
		elif len(points) == 2:
			pygame.gfxdraw.line(window, int(points[0][0]), int(
				points[0][1]), int(points[1][0]), int(points[1][1]), borderColor)
		return
