import pygame
import pymunk.pygame_util

pymunk.pygame_util.positive_y_is_up = False
pygame.init()

WIDTH, HEIGHT = 900, 900
window = pygame.display.set_mode((WIDTH, HEIGHT))

space = pymunk.Space()
space.gravity = 0, 2000
draw_options = pymunk.pygame_util.DrawOptions(window)

def main_ball(radius_value):

    ball_radius = radius_value
    mousex, mousey = pygame.mouse.get_pos()
    ball_position = (mousex, mousey)

    rb_division_value = float(900 / 150)
    red_value = int(mousex//rb_division_value + 85)
    blue_value = int(mousey//rb_division_value + 100)

    ball_color = (red_value, 0, blue_value, 200)   

    if ball_radius <= mousex <= WIDTH - ball_radius and ball_radius <= mousey <= HEIGHT - ball_radius:
        pygame.draw.circle(window, ball_color, ball_position, ball_radius)

    return (ball_color, ball_position)

def dynamic_ball(radius_value):
    max_elasticity = 0.98
    min_elasticity = 0.1
    max_radius = 100
    
    if radius_value > max_radius:
        elasticity = min_elasticity
    else:
        elasticity = max_elasticity - ((max_elasticity - min_elasticity) * (radius_value / max_radius))
    
    # Get ball color and position from another function
    ball_color, ball_position = main_ball(radius_value)
    ball_color, ball_position = main_ball(radius_value)
    mass, radius = 1, radius_value
    ball_moment = pymunk.moment_for_circle(mass, 0, radius)
    ball_body = pymunk.Body(mass, ball_moment)
    ball_body.position = ball_position
    ball_shape = pymunk.Circle(ball_body, radius)
    ball_shape.elasticity = elasticity
    ball_shape.friction = elasticity
    space.add(ball_body, ball_shape)

def draw_dynamic_balls(ball_color):
    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            pos_x, pos_y = shape.body.position
            pygame.draw.circle(window, ball_color, (int(pos_x), int(pos_y)), int(shape.radius))

def walls():
    bottom_wall = pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 5)
    bottom_wall.elasticity = 0.95
    space.add(bottom_wall)

def run():
    run = True
    fps = 120
    clock = pygame.time.Clock()
    radius_value = 25

    pygame.mouse.set_visible(True)
    pygame.mouse.set_cursor(pygame.cursors.diamond)
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    radius_value += 5
                elif event.button == 5:
                    radius_value -= 5
                elif event.button == 1:
                    dynamic_ball(radius_value)


        space.step(1/120)
        window.fill((10,10,8))
        ball_color, ball_position = main_ball(radius_value)
        walls()
        draw_dynamic_balls(ball_color)
        clock.tick(fps)
        pygame.display.update()

    
    pygame.quit()

if __name__ == "__main__":
    run()
