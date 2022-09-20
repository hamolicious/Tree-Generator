import pygame
from vector import Color
from time import time
from tree_generator import TreeGenerator

#region pygame init
pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
clock, fps = pygame.time.Clock(), 0

delta_time = 0 ; frame_start_time = 0
#endregion

def create_tree_surface():
	tree = TreeGenerator(100, leaf_colors=[
		Color.from_hex('#ffb0bf').get(),
		Color.from_hex('#ff82bd').get(),
		Color.from_hex('#d74ac7').get(),
		Color.from_hex('#a825ba').get(),
		Color.from_hex('#682b9c').get(),
	])
	surface = tree.bake()
	return surface

num_trees = 10
display_tree_for = 1
end_time = 0

start_tree_generation = time()
trees = [create_tree_surface() for _ in range(num_trees)]
end_tree_generation = time()

print(f'Average time to generate 1 tree: {(end_tree_generation - start_tree_generation) / num_trees} seconds')

current_tree = trees[0]
index = 0

while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
				pygame.quit()
				quit()
	frame_start_time = time()
	screen.fill([100, 100, 200])

	mouse_pos   = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()
	key_press   = pygame.key.get_pressed()

	if time() > end_time:
		index += 1
		if index == len(trees) : index = 0
		current_tree = trees[index]
		end_time = time() + display_tree_for

	screen.blit(
		pygame.transform.scale(current_tree, (600, 600)),
		(0, 0)
	)

	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')