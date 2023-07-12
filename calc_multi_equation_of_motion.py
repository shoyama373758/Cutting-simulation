import numpy as np
import matplotlib.pyplot as plt

N = 100000  # サンプル数
T = 10  # 時間幅


def f1(u, v):
    return v


def f2(u, v, fx, fy):
    M_inv = np.linalg.inv(M)

    F = np.zeros(len(M))
    F[0] = fx
    F[1] = fy

    return np.dot(M_inv, F) - np.dot(np.dot(C, M_inv), v) - np.dot(np.dot(K, M_inv), u)


def impulse(A=1):
    impulse = np.zeros(N)
    impulse[1] = A
    return impulse


noforce = np.zeros(N)


def sim(u0, v0, fx=noforce, fy=noforce):
    h = float(T / N)
    u, v = u0, v0

    time = []
    x_position = []
    x_velocity = []
    y_position = []
    y_velocity = []

    for i in range(N):
        t = i * h

        time.append(t)
        x_position.append(u[0])
        x_velocity.append(v[0])

        y_position.append(u[1])
        y_velocity.append(v[1])

        if i % 100 == 0:
            print("iteration=", i, "time=", t)

        k11 = f1(u, v)
        k12 = f2(u, v, fx[i], fy[i])

        k21 = f1(u + k11 * (h / 2), v + k12 * (h / 2))
        k22 = f2(u + k11 * (h / 2), v + k12 * (h / 2), fx[i], fy[i])

        k31 = f1(u + k21 * (h / 2), v + k22 * (h / 2))
        k32 = f2(u + k21 * (h / 2), v + k22 * (h / 2), fx[i], fy[i])

        k41 = f1(u + k31 * h, v + k32 * h)
        k42 = f2(u + k31 * h, v + k32 * h, fx[i], fy[i])

        u += (k11 + 2 * k21 + 2 * k31 + k41) * h / 6
        v += (k12 + 2 * k22 + 2 * k32 + k42) * h / 6

    return time, x_position, y_position


# M = np.array([[100, 0], [0, 50]])
# C = np.array([[100, -50], [-50, 50]])
# K = np.array([[6.0e4, -1.0e4], [-1.0e4, 1.0e4]])

# u0 = np.zeros(len(M))
# v0 = np.zeros(len(M))

# impulse = impulse()
# time, x_position, y_position = sim(u0, v0, fx=impulse)

# plt.plot(time, y_position, color="red", linewidth=2, label="y(t)")
# plt.title("Endmill vibraiton")
# plt.xlabel("Time")
# plt.ylabel("Displacement")
# plt.legend()
# plt.show()

M = np.array([[100, 0], [0, 50]])
C = np.array([[100, -50], [-50, 50]])
K = np.array([[6.0e4, -1.0e4], [-1.0e4, 1.0e4]])


u0 = np.array([0.0, 0.0])
v0 = np.array([0.0, 0.0])


impulse = impulse()
time, x_position, y_position = sim(u0, v0, fx=impulse)

plt.plot(time, x_position, color="red", linewidth=2, label="x(t)")
plt.plot(time, y_position, color="green", linewidth=2, label="y(t)")
plt.title("Endmill vibraiton")
plt.xlabel("Time")
plt.ylabel("Displacement")
plt.legend()
plt.show()
