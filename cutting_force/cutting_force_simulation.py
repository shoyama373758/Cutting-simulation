import numpy as np
import matplotlib.pyplot as plt

N = 1000  # 何個の要素に分けるか
# 切削係数
K_tc = 1000
K_rc = 700
K_ac = 100
# 切れ刃と被削材の摩擦力係数
K_te = 10
K_re = 5
K_ae = 0

D = 2  # 工具直径（㎜）
num_blades = 2  # 刃数
twist_angle = 30  # ねじれ角（degree）
axial_depth = 2  # 軸方向切り込み深さ（㎜）
fz = 0.5  # 一刃あたりの送り量（mm / 刃）→ 次の刃が来るまでの横移動量
theta_0 = 0  # エンドミル先端の刃の初期角度（degree）
processing_time = 0.2  # 加工時間（s）
rotation_speed = 6000  # エンドミルの回転速度（rpm）
feed_speed = 0.25  # エンドミルの送り速度（㎜/s）
# 工具半径 (mm)
R = D / 2
# ねじれ角の変化率
twist_angle_rate = np.pi * np.tan(np.radians(twist_angle)) / (2 * R)
# 微小部分の厚み
dz = axial_depth / N


# 微小要素におけるx, y, z方向それぞれの切削力を計算
def calc_cutting_force(theta_list):
    F_xj = F_yj = F_zj = 0
    for theta in theta_list:
        F_xj += (
            -K_te * np.cos(theta)
            - K_tc * fz * np.sin(theta) * np.cos(theta)
            - K_re * np.sin(theta)
            - K_rc * fz * (np.sin(theta) ** 2)
        ) * dz
        F_yj += (
            K_te * np.sin(theta)
            + K_tc * fz * (np.sin(theta) ** 2)
            - K_re * np.cos(theta)
            - K_rc * fz * np.sin(theta) * np.cos(theta)
        ) * dz
        F_zj += (-K_ae - K_ac * fz * np.sin(theta)) * dz
    return F_xj, F_yj, F_zj


# 切り込み深さ全体におけるx, y, z方向それぞれの切削力を計算
def calc_sum_cutting_force(theta_0):
    F_x = F_y = F_z = 0
    for i in range(1, N + 1):
        z = axial_depth * i / N
        angle_radian = twist_angle_rate * z + np.radians(theta_0)
        angle_degree = np.degrees(angle_radian)
        angle_list_degree = [angle_degree % 360]
        for _ in range(num_blades - 1):
            angle_degree = angle_degree + 360 / num_blades
            angle_list_degree.append(angle_degree % 360)
        hitting_angle_list_degree = []
        for angle in angle_list_degree:
            if angle >= 0 and angle <= 180:
                hitting_angle_list_degree.append(angle)
        hitting_angle_list_radian = np.radians(hitting_angle_list_degree)
        temp_Fx, temp_Fy, temp_Fz = calc_cutting_force(hitting_angle_list_radian)
        F_x += temp_Fx
        F_y += temp_Fy
        F_z += temp_Fz
    return F_x, F_y, F_z


time = []
Fx = []
Fy = []
Fz = []

time_T = 10  # s
time_N = 100000

h = float(time_T / time_N)

for i in range(time_N):
    print(i)
    t = i * h
    time.append(t)
    theta_0 += np.degrees((rotation_speed / 60) * h * np.pi * 2)
    theta_0 %= 360
    F_x, F_y, F_z = calc_sum_cutting_force(theta_0)
    Fx.append(F_x)
    Fy.append(F_y)
    Fz.append(F_z)


# plt.plot(time, Fx, label="Fx")
# plt.plot(time, Fy, label="Fy")
# plt.plot(time, Fz, label="Fz")
# plt.xlabel("Time[s]")
# plt.ylabel("Cutting Force[N]")
# plt.title("Cutting Force and Time")
# plt.legend()
# plt.show()


"""
degree = [n for n in range(361)]
for j in degree:
    theta_0 = j
    F_x, F_y, F_z = calc_sum_cutting_force(theta_0)
    Fx.append(F_x)
    Fy.append(F_y)
    Fz.append(F_z)
# 結果のプロット
plt.plot(degree, Fx, label="Fx")
plt.plot(degree, Fy, label="Fy")
plt.plot(degree, Fz, label="Fz")
plt.xlabel("Rotation angle")
plt.ylabel("Cutting Force")
plt.title("Cutting Force and Rotation Angle")
plt.legend()
plt.show()
"""
