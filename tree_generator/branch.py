from __future__ import annotations
from random import randint
from vector import Vec2d, Color
from math import radians
from .util import get_spread_random_value
import pygame


class Branch:
	color = Color(60, 30, 15).get()
	width = 10

	def __init__(self, start: Vec2d, angle: float, length: float) -> None:
		self.start = start.copy()
		self.angle = angle
		self.length = length
		self.width = Branch.width

		self.children = []

	def get_all_children(self, list=None):
		if list is None:
			list = []

		for child in self.children:
			list += child.get_children()
			child.get_all_children(list)

		return list

	def get_children(self) -> list[Branch]:
		return self.children

	def get_end(self, at: float=1.0) -> Vec2d:
		return Vec2d.from_angle(radians(self.angle)) \
			.mult(self.length * at) \
			.add(self.start)

	def attach_children(self, children: list[Branch]) -> None:
		self.children += children

	def display(self, screen: pygame.Surface) -> None:
		pygame.draw.line(screen, Branch.color, self.start.as_ints(), self.get_end().as_ints(), max(1, int(self.width)))

		for child in self.children:
			child.display(screen)
