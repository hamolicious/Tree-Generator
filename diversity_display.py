from dataclasses import dataclass
from secrets import choice
from vector import Vec2d, Color
import os
import pygame
from tree_generator import TreeGenerator
from time import time

#region pygame init
pygame.init()
size = (1200, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

delta_time = 0 ; frame_start_time = 0
#endregion


colors = [
	[
		Color.from_hex('#8fb569').get(),
		Color.from_hex('#a7ab59').get(),
		Color.from_hex('#99943c').get(),
		Color.from_hex('#7a6f18').get(),
		Color.from_hex('#7a6507').get(),
	],
	[
		Color.from_hex('#1c0818').get(),
		Color.from_hex('#350d24').get(),
		Color.from_hex('#4c1026').get(),
		Color.from_hex('#681225').get(),
		Color.from_hex('#810e23').get(),
		Color.from_hex('#941416').get(),
	],
	[
		Color.from_hex('#05020d').get(),
		Color.from_hex('#12021a').get(),
		Color.from_hex('#1d072a').get(),
		Color.from_hex('#260f3f').get(),
		Color.from_hex('#381e5e').get(),
		Color.from_hex('#4d3981').get(),
		Color.from_hex('#6660a3').get(),
	]
]



if not os.path.exists('trees') : os.mkdir('trees')
images = []
for i in range(10):
	t = TreeGenerator(100, leaf_colors=choice(colors))
	images.append(t.bake())
	pygame.image.save(images[-1], f'trees/tree-{i}.png')

trees = []
@dataclass
class Tree:
	image: pygame.Surface
	pos: Vec2d

for _ in range(30):
	trees.append(Tree(choice(images), Vec2d.random_pos().mult(size[0], size[1] * 0.25)))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
	frame_start_time = time()
	screen.fill([100, 100, 200])

	mouse_pos   = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()
	key_press   = pygame.key.get_pressed()

	pygame.draw.rect(screen, [0, 100, 0], (0, size[1] * 0.25, size[0], size[1]))

	for t in trees:
		t.pos.iadd(-20 * delta_time, 0)
		screen.blit(t.image, t.pos.as_ints())

		if t.pos.x < -t.image.get_size()[0]:
			t.pos.x = size[0] + t.image.get_size()[0]

	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')