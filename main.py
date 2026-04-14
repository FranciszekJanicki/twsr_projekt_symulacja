import numpy as np
import matplotlib.pyplot as plt

R = 5.0
center = np.array([0.0, 0.0])

dt = 0.05

state = np.array([R + 2.0, 0.0, np.pi/2])

k_r = 1.2
k_theta = 3.0

plt.ion()
fig, ax = plt.subplots()

theta_circle = np.linspace(0, 2*np.pi, 200)
circle_x = R * np.cos(theta_circle)
circle_y = R * np.sin(theta_circle)

ax.plot(circle_x, circle_y)
traj_line, = ax.plot([], [])
robot_point, = ax.plot([], [], marker='o')

ax.set_aspect('equal', adjustable='box')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_title("Real-Time Robot Animation")

trajectory = []

# czas symulacji
for _ in range(800):
    x, y, theta = state
    
    pos = np.array([x, y])
    vec = pos - center
    dist = np.linalg.norm(vec)
    radial_error = dist - R
    
    tangent = np.array([-vec[1], vec[0]])
    tangent = tangent / np.linalg.norm(tangent)
    desired_theta = np.arctan2(tangent[1], tangent[0])
    
    v = 1.0
    omega = k_theta * (desired_theta - theta) - k_r * radial_error
    omega = np.clip(omega, -2.0, 2.0)
    
    x += v * np.cos(theta) * dt
    y += v * np.sin(theta) * dt
    theta += omega * dt
    state = np.array([x, y, theta])
    
    trajectory.append([x, y])
    traj = np.array(trajectory)
    
    traj_line.set_data(traj[:,0], traj[:,1])
    robot_point.set_data([x], [y])
    
    plt.draw()
    plt.pause(0.01)

plt.ioff()
plt.show()