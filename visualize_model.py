import numpy as np
import matplotlib.pyplot as plt

def visualize_onelayer_model(phim, phif):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    nx, ny, nz = phim.shape

    # 基体相
    X, Y, Z = np.where(phim == 1)
    ax.scatter(X, Y, Z, c='gray', alpha=0.05, s=1)

    # 填料相
    X, Y, Z = np.where(phif == 1)
    ax.scatter(X, Y, Z, c='blue', alpha=0.5, s=1)

    # 设置坐标轴的比例
    ax.set_box_aspect((nx, ny, nz))
    ax.view_init(elev=45, azim=-45)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_zlim(0, nz)

    plt.show()


# | 3|层
# | 2|层
# | 1|层
# | 0|层
# |-1|层
# |-2|层
# |-3|层

def visualize_nlayer_model(phime, phife, phimo, phifo):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    nx, ny, nz = phime.shape

    # 偶数层基体相
    X, Y, Z = np.where(phime == 1)
    ax.scatter(X, Y, Z, c='gray', alpha=0.04, s=1)

    # 偶数层填料相
    X, Y, Z = np.where(phife == 1)
    ax.scatter(X, Y, Z, c='blue', alpha=0.5, s=1)

    # 奇数层基体相
    X, Y, Z = np.where(phimo == 1)
    ax.scatter(X, Y, Z, c='yellow', alpha=0.02, s=1)

    # 奇数层填料相
    X, Y, Z = np.where(phifo == 1)
    ax.scatter(X, Y, Z, c='red', alpha=0.5, s=1)

    # 设置坐标轴的比例
    ax.set_box_aspect((nx, ny, nz))
    ax.view_init(elev=45, azim=-45)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_zlim(0, nz)

    plt.show()