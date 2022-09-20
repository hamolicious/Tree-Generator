from math import radians
from random import randint
from secrets import choice
import pygame
from vector import Vec2d


class Leaf:
	def __init__(self, home: Vec2d, pos: Vec2d, colors=None) -> None:
		self.shape = [
			Vec2d(-0.5, -0.5),
			Vec2d( 0.5, -0.5),
			Vec2d(-0.5,  0.5),
		]
		self.scale = randint(2, 4)
		self.pos = pos.copy()
		self.home = home.copy()
		self.rotation = randint(0, 360)
		self.colors = ['white'] if colors == None else colors

	def get_color(self):
		return choice(self.colors)

	def display(self, screen: pygame.Surface) -> None:
		polygon = []
		for v in self.shape:
			v.rotate(self.rotation)
			polygon.append(v \
				.mult(self.scale) \
				.add(self.pos) \
				.as_ints()
			)

		pygame.draw.polygon(screen, self.get_color(), polygon)
		pygame.draw.line(screen, self.get_color(), self.home.as_ints(), self.pos.as_ints(), 1)




