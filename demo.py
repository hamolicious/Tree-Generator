import pygame
from time import time
from tree_generator import Tree
from pygame_widgets import Slider, TextBox, Button

# region pygame init
pygame.init()
pygame.font.init()
size = WIDTH, HEIGHT = (600, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

font = pygame.font.SysFont('ariel', 15)

delta_time = 0
frame_start_time = 0
# endregion


# tree params
depth = 10
max_angle = 50
max_branches = 1
new_branch_chance = 20
start_width = 5
end_width = 1

# ui


def draw_ui(element, name, events):
    element.listen(events)
    element.draw()

    label = font.render(f'{name} : {element.getValue()}', True, [150, 0, 0])
    x, y = element.x, element.y

    screen.blit(label, (x, y))


depth_slider = Slider(screen, 10, 10, size[0]-20, 10, initial=10, min=0, max=30, step=1, handleColour=[51, 51, 51])
angle_slider = Slider(screen, 10, 30, size[0]-20, 10, initial=50, min=0, max=180, step=1, handleColour=[51, 51, 51])
branches_slider = Slider(screen, 10, 50, size[0]-20, 10, initial=1, min=0, max=5, step=1, handleColour=[51, 51, 51])
branch_chance_slider = Slider(screen, 10, 70, size[0]-20, 10, initial=20, min=0, max=100, step=1, handleColour=[51, 51, 51])
start_width_slider = Slider(screen, 10, 90, size[0]-20, 10, initial=5, min=0, max=20, step=1, handleColour=[51, 51, 51])
end_width_slider = Slider(screen, 10, 110, size[0]-20, 10, initial=1, min=0, max=20, step=1, handleColour=[51, 51, 51])


def new_tree():
    return Tree(WIDTH/2, HEIGHT-20, depth, max_angle, max_branches, new_branch_chance, start_width, end_width)


tree = new_tree()
key_block = False
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    frame_start_time = time()
    screen.fill(0)
    mouse_press = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # region slider handling
    # depth
    draw_ui(depth_slider, 'Depth', events)
    if depth_slider.getValue() != depth:
        depth = depth_slider.getValue()
        tree = new_tree()

    # angle
    draw_ui(angle_slider, 'Max Angle', events)
    if angle_slider.getValue() != max_angle:
        max_angle = angle_slider.getValue()
        tree = new_tree()

    # branches
    draw_ui(branches_slider, 'Max Branches', events)
    if branches_slider.getValue() != max_branches:
        max_branches = branches_slider.getValue()
        tree = new_tree()

    # branches spawns
    draw_ui(branch_chance_slider, 'Branch Spawn Chance', events)
    if branch_chance_slider.getValue() != new_branch_chance:
        new_branch_chance = branch_chance_slider.getValue()
        tree = new_tree()

    # start width
    draw_ui(start_width_slider, 'Start Width', events)
    if start_width_slider.getValue() != start_width:
        start_width = start_width_slider.getValue()
        tree = new_tree()

    # end width
    draw_ui(end_width_slider, 'End Width', events)
    if end_width_slider.getValue() != end_width:
        end_width = end_width_slider.getValue()
        tree = new_tree()

    # endregion

    if mouse_press[0] == 1 and pygame.Rect(0, 120, size[0], size[1]).collidepoint(mouse_x, mouse_y) and not key_block:
        tree = new_tree()
        key_block = True

    if sum(mouse_press) == 0:
        key_block = False

    tree.draw(screen)

    pygame.display.update()
    clock.tick(fps)
    delta_time = time() - frame_start_time
    pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')
