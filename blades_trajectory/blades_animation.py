import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

D = 2  # 工具直径
rotation_speed = 6000  # 回転速度
feed_speed = 100  # 送り速度
theta_0 = 0  # 初期角度
R = D / 2  # 工具半径

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.set_ylim(-2, 2)


ims = []

T = 10  # 時間幅（ｓ）
N = 100000  # Ｔをいくつに分けるかdefault=100000
h = float(T / N)

for i in range(1000):
    t = i * h
    theta = np.radians(theta_0 + np.degrees((rotation_speed / 60) * 2 * np.pi * t))

    x = R * np.sin(theta) + feed_speed * t
    y = R * np.cos(theta)

    x2 = R * np.sin(theta + np.pi) + feed_speed * t
    y2 = R * np.cos(theta + np.pi)

    im = plt.plot(x, y, color="b", marker="o", markersize=10)
    im2 = plt.plot(x2, y2, color="r", marker="o", markersize=10)

    ims.append(im)
    ims.append(im2)

ani = animation.ArtistAnimation(fig, ims, interval=10)
plt.show()
