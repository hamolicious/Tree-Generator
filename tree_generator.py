import pygame
from vector_class import Vector2D as Vec, randint

def map_to_range(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class Branch():
    def __init__(self, pos1, pos2, width):
        self.start = pos1
        self.end = pos2
        self.width = width

class Tree():
    def __init__(self, x, y, depth, max_angle, max_branches, new_branch_chance, start_width, end_width):
        self.pos = Vec(x, y)

        self.max_angle = max_angle
        self.max_branches = max_branches
        self.new_branch_chance = new_branch_chance
        self.start_width = start_width
        self.end_width = end_width
        self.start_depth = depth

        self.branches = [
            Branch( Vec(), Vec(0, -50), self.start_width),
        ]

        self.add_branch(self.start_depth, self.branches[0].end)

    def add_branch(self, depth, pos, angle=-90):
        if depth <= 0:
            return

        new_angle = randint(-self.max_angle, self.max_angle)
        length = randint(10, 20)

        new_pos = Vec.from_angle(new_angle + angle)
        new_pos.mult(length)
        new_pos.add(pos)

        width = map_to_range(depth, 0, self.start_depth, self.end_width, self.start_width)
        self.branches.append( Branch(pos, new_pos, width) )


        self.add_branch(depth-1, new_pos)
        for _ in range(self.max_branches):
            if randint(0, 100) < self.new_branch_chance:
                self.add_branch(depth-1, new_pos)

    def draw(self, screen):
        for branch in self.branches:
            pygame.draw.line(screen, [255, 255, 255], (branch.start + self.pos).get(), (branch.end + self.pos).get(), int(branch.width))





















