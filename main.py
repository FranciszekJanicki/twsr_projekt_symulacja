import pygame
import numpy as np
import sys

R = 1.0
center = np.array([0.0, 0.0])
dt = 0.05

state = np.array([R + 2.0, 0.0, np.pi/2])

k_r = 0.5
k_theta = 0.3
k_i = 0.5

integral_error = 0.0
trajectory = []

SCALE = 40
WIDTH, HEIGHT = 800, 800

def to_screen(x, y):
    return int(WIDTH/2 + x*SCALE), int(HEIGHT/2 - y*SCALE)

def angle_diff(a, b):
    return np.arctan2(np.sin(a - b), np.cos(a - b))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((30, 30, 30))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x, y, theta = state
    
    pos = np.array([x, y])
    vec = pos - center
    dist = np.linalg.norm(vec)
    radial_error = dist - R
    
    integral_error += radial_error * dt
    integral_error = np.clip(integral_error, -5.0, 5.0)
    
    tangent = np.array([-vec[1], vec[0]])
    tangent /= np.linalg.norm(tangent)
    desired_theta = np.arctan2(tangent[1], tangent[0])
    
    v = 1.0
    
    omega = (
        k_theta * angle_diff(desired_theta, theta)
        - k_r * radial_error
        - k_i * integral_error
    )
    omega = np.clip(omega, -2.0, 2.0)
    
    # ruch
    x += v * np.cos(theta) * dt
    y += v * np.sin(theta) * dt
    theta += omega * dt
    state = np.array([x, y, theta])
    
    trajectory.append((x, y))

    pygame.draw.circle(screen, (100, 100, 255), to_screen(0, 0), int(R*SCALE), 1)
    
    if len(trajectory) > 1:
        pts = [to_screen(px, py) for px, py in trajectory]
        pygame.draw.lines(screen, (0, 255, 0), False, pts, 2)
    
    rx, ry = to_screen(x, y)
    pygame.draw.circle(screen, (255, 100, 100), (rx, ry), 6)
    
    arrow_len = 0.8
    ax = x + arrow_len * np.cos(theta)
    ay = y + arrow_len * np.sin(theta)
    pygame.draw.line(screen, (255, 255, 0), (rx, ry), to_screen(ax, ay), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()