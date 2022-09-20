from vector import Vec2d, Color
from .branch import Branch
from math import radians
import pygame


class FractalTree:
	def __init__(self, root_pos: Vec2d, root_len: float) -> None:
		self.delta_angle = 45
		self.delta_len = 0.6
		self.min_branch_len = 10

		self.starting_branch = Branch(Vec2d(root_pos).copy(), -90, root_len)

	def __make_branch_from(self, branch: Branch, delta_angle: float) -> Branch:
		child = Branch(
			branch.get_end(),
			branch.angle + delta_angle,
			branch.length * self.delta_len
		)

		branch.attach_children([child])
		return child

	def make_branches(self):
		stack = [self.starting_branch]

		while len(stack) > 0:
			current_branch = stack.pop()

			left_branch = self.__make_branch_from(current_branch,  -self.delta_angle)
			right_branch = self.__make_branch_from(current_branch, +self.delta_angle)

			if left_branch.length > self.min_branch_len : stack.append(left_branch)
			if right_branch.length > self.min_branch_len : stack.append(right_branch)

	def display(self, screen: pygame.Surface) -> None:
		self.starting_branch.display(screen)

