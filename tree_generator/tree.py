from math import ceil
from random import randint, Random
from vector import Vec2d
from .branch import Branch
from .leaf import Leaf
import pygame
from .util import get_spread_random_value

class TreeGenerator:
	def __init__(self, root_len: float, **kwargs) -> None:
		self.delta_angle        = kwargs.get('delta_angle', 22)
		self.delta_len          = kwargs.get('delta_len', 0.75)
		self.min_branch_len     = kwargs.get('min_branch_len', 5)
		self.min_angle          = kwargs.get('min_angle', -10)
		self.max_angle          = kwargs.get('max_angle',  10)
		self.delta_branch_width = kwargs.get('delta_branch_width', 0.8)
		self.seed               = kwargs.get('seed', randint(0, 100000000))
		self.leaf_colors        = kwargs.get('leaf_colors', None)

		self.rng = Random(self.seed)

		self.starting_branch = Branch(Vec2d.zero(), -90, root_len)

	def __make_branch_from(self, branch: Branch, delta_angle: float, width: float) -> Branch:
		child = Branch(
			branch.get_end(get_spread_random_value(self.rng)),
			branch.angle + delta_angle + self.rng.randint(self.min_angle, self.max_angle),
			branch.length * self.delta_len
		)
		child.width = width

		branch.attach_children([child])
		return child

	def calculate_branches_with_current_settings(self):
		start_length = self.starting_branch.length
		end_length = self.min_branch_len
		branch_count = 1

		while start_length > end_length:
			start_length *= self.delta_len
			branch_count = (branch_count << 1) + 1
		print(branch_count, bin(branch_count))
		return branch_count

	def __make_branches(self):
		stack = [self.starting_branch]

		while len(stack) > 0:
			current_branch = stack.pop()

			left_branch = self.__make_branch_from(
				current_branch,
				-self.delta_angle,
				current_branch.width * self.delta_branch_width
			)

			right_branch = self.__make_branch_from(
				current_branch,
				+self.delta_angle,
				current_branch.width * self.delta_branch_width
			)

			if left_branch.length > self.min_branch_len : stack.append(left_branch)
			if right_branch.length > self.min_branch_len : stack.append(right_branch)

	def __generate_leaves(self, screen: pygame.Surface):
		branches = self.starting_branch.get_all_children()
		for b in branches:
			if len(b.children) == 0 : continue
			l = Leaf(
				b.get_end(),
				b.get_end().add(Vec2d.random_unit().mult(5)),
				self.leaf_colors
			)
			l.display(screen)

	def bake(self) -> pygame.Surface:
		self.__make_branches()
		branches = self.starting_branch.get_all_children()

		max_x = 0
		max_y = 0
		min_x = 99**99
		min_y = 99**99

		for b in branches:
			max_x = max(b.get_end().x, max_x)
			max_y = max(b.get_end().y, max_y)
			min_x = min(b.get_end().x, min_x)
			min_y = min(b.get_end().y, min_y)

		width = ceil(abs(min_x - max_x) + 100)
		height = ceil(abs(min_y - max_y) + 100)

		screen =  pygame.Surface(
			(width, height), pygame.SRCALPHA
		)
		screen.fill([0, 0, 0, 0])
		self.starting_branch.start = Vec2d(width/2, height)

		self.__make_branches()
		self.starting_branch.display(screen)

		self.__generate_leaves(screen)

		return screen







