import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from time import time
from tree_generator import TreeGenerator, FractalTree

#region pygame init
pygame.init()
size = (1200, 600)
screen = pygame.display.set_mode(size)
clock, fps = pygame.time.Clock(), 0

delta_time = 0 ; frame_start_time = 0
#endregion

def create_slider(name, init_, min_, max_, step, _counter=[]):
	start_y = 30
	increm_y = 50

	slider = Slider(screen, 900, (len(_counter) * increm_y) + start_y, 200, 25,
		initial=init_,
		min=min_,
		max=max_,
		step=step,
	)
	output = TextBox(screen, 600, (len(_counter) * increm_y) + start_y, 200, 25,
		fontSize=25,
		colour=[100, 100, 200],
		borderThickness=0
	)
	output.disable()

	_counter.append(slider)

	return (slider, output, name)

delta_angle = create_slider('Branch angle offset', 22, 5, 90, 1)
delta_len = create_slider('Branch length decrease', 0.75, 0, 1, 0.01)
min_branch_len = create_slider('Minimum branch length', 5, 1, 99, 1)
min_angle = create_slider('Min angle randomness', -10, -90, 90, 1)
max_angle = create_slider('Max angle randomness',  10, -90, 90, 1)
delta_branch_width = create_slider('Branch shrink percentage', 0.8, 0, 1, 0.01)
init_length = create_slider('Trunk length', 100, 5, 600, 1)

sliders = [
	delta_angle,
	delta_len,
	min_branch_len,
	min_angle,
	max_angle,
	delta_branch_width,
	init_length,
]

def draw_widgets(collection: list):
	for slider, output, name in collection:
		output.setText(f'{name}: {slider.getValue():,.3f}')

def create_tree_surface():
	tree = TreeGenerator(
		root_len           = init_length[0].getValue(),
		delta_angle        = delta_angle[0].getValue(),
		delta_len          = delta_len[0].getValue(),
		min_branch_len     = min_branch_len[0].getValue(),
		min_angle          = min_angle[0].getValue(),
		max_angle          = max_angle[0].getValue(),
		delta_branch_width = delta_branch_width[0].getValue(),
	)
	surface = tree.bake()
	return surface

get_values = lambda: [slider[0].getValue() for slider in sliders]
values = []
tree = create_tree_surface()

while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
				print(tree.seed)
				pygame.quit()
				quit()
	frame_start_time = time()
	screen.fill([100, 100, 200])

	mouse_pos   = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()
	key_press   = pygame.key.get_pressed()

	if min_angle[0].getValue() > max_angle[0].getValue():
		min_angle[0].setValue(max_angle[0].getValue())

	if max_angle[0].getValue() < min_angle[0].getValue():
		max_angle[0].setValue(min_angle[0].getValue())

	if values != get_values():
		tree = create_tree_surface()
		values = get_values()

	x_buffer = abs(tree.get_size()[0] - 600) / 2
	y_buffer = abs(tree.get_size()[1] - 600) / 2

	screen.blit(tree, (x_buffer, y_buffer))
	draw_widgets(sliders)

	pygame.display.set_icon(pygame.Surface.subsurface(screen, (0, 0, 600, 600)))
	pygame_widgets.update(events)
	pygame.display.update()
	clock.tick(fps)
	delta_time = time() - frame_start_time
	pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')