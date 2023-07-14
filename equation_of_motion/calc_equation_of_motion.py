import numpy as np
import matplotlib.pyplot as plt


# ルンゲクッタ法により微分方程式を解く
# びびり振動クラス
class ChatterVibration:
    #  クラス変数
    N = 1000  # サンプル数
    T = 100.0  # 時間幅

    # m*(d2x/dt2) + c*dx/dt + k*x = f
    def __init__(self, m, c, k):
        self.m = m  # 質量
        self.c = c  # ダンパ係数
        self.k = k  # ばね定数

    # u(振動変位)
    # v = du/dt (速度変位)

    # f1(t) = du/dt = v
    def f1(self, t, u, v):
        return v

    # f2(t) = dv/dt = f/m - c/m *v -k/m *u
    def f2(self, t, u, v):
        return (
            self.eforce_equation(t) / self.m
            - (self.c / self.m) * v
            - (self.k / self.m) * u
        )

    # 外力を表す関数
    def eforce_equation(self, t):
        return 0.1 * np.cos(1.0 * t)  # default = 0.1 * np.cos(1.0 * t)

    def calc_vibraiton(self, u0, v0):
        # 区間TをN個に分割した際の微小要素の幅h
        h = float(self.T / self.N)

        # ないとエラー発生
        u = u0
        v = v0

        # 空のリストを作成、初期値を代入
        time, position, velocity, external_force = [], [], [], []
        time.append(0.0)
        position.append(u)
        velocity.append(v)
        external_force.append(self.eforce_equation(0.0))

        # N個の区間それぞれにおけるx,vの近似値を求める
        for i in range(0, self.N):
            t = i * h
            e_force = self.eforce_equation(t)

            # ri1 = dx/dt(t,u,v)
            # ri2 = dv/dt(t,u,v)

            # 点tにおけるx,vの微分係数
            r11 = self.f1(t, u, v)
            r12 = self.f2(t, u, v)

            # tとt+hの中点におけるx,vの微分係数
            r21 = self.f1(t + h / 2.0, u + (h / 2.0) * r11, v + (h / 2.0) * r12)
            r22 = self.f2(t + h / 2.0, u + (h / 2.0) * r11, v + (h / 2.0) * r12)

            # r21,r22の傾きでt+(h/2)進んだ地点の微分係数
            r31 = self.f1(t + h / 2.0, u + (h / 2.0) * r21, v + (h / 2.0) * r22)
            r32 = self.f2(t + h / 2.0, u + (h / 2.0) * r21, v + (h / 2.0) * r22)

            # 点t+hにおけるx,vの微分係数
            r41 = self.f1(t + h, u + h * r31, v + h * r32)
            r42 = self.f2(t + h, u + h * r31, v + h * r32)

            # （ri1 ~ ri4 までを適当に重み付けした平均）×　h
            # 次の点のx,vの値を求める
            u += h * (r11 + 2 * r21 + 2 * r31 + r41) / 6.0
            v += h * (r12 + 2 * r22 + 2 * r32 + r42) / 6.0

            # リストに値を追加
            time.append(t + h)
            position.append(u)
            velocity.append(v)
            external_force.append(e_force)

        # 結果をプロット
        plt.plot(time, position, color="red", linewidth=2, label="y(t)")
        plt.plot(time, external_force, color="green", linewidth=2, label="Cos")
        plt.title("Endmill vibraiton")
        plt.xlabel("Time")
        plt.ylabel("Displacement")
        plt.legend()
        plt.show()

        return time, position, external_force


m = 1
c = 0.2
k = 1
u0 = 1
v0 = 0
