import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

D = 2  # 工具直径
rotation_speed = 6000  # 回転速度
feed_speed = 10  # 送り速度
theta_0 = 0  # 初期角度
R = D / 2  # 工具半径

fig, ax = plt.subplots()
ax.set_aspect("equal", "datalim")
# ax.set_ylim(-2, 2)


x = []
y = []
x2 = []
y2 = []

T = 10  # 時間幅（ｓ）
N = 100000  # Ｔをいくつに分けるかdefault=100000
h = float(T / N)

for i in range(1000):
    t = i * h
    theta = np.radians(theta_0 + np.degrees((rotation_speed / 60) * 2 * np.pi * t))

    x_tmp = R * np.sin(theta) + feed_speed * t
    y_tmp = R * np.cos(theta)

    x2_tmp = R * np.sin(theta + np.pi) + feed_speed * t
    y2_tmp = R * np.cos(theta + np.pi)

    x.append(x_tmp)
    y.append(y_tmp)

    x2.append(x2_tmp)
    y2.append(y2_tmp)


plt.plot(x, y, color="b")
plt.plot(x2, y2, color="r")
plt.show()
