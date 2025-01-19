from visualize_model import visualize_onelayer_model
import numpy as np
import matplotlib.pyplot as plt


def generate_0D_model(nx, ny, nz, diameter, C):
    """
    生成一个0D模型，其中球体代表填充物。

    :param nx, ny, nz: 体积的维度
    :param diameter: 每个球体的直径
    :param C: 填充物的体积分数
    :return: phim (基体相), phif (填充相)
    """
    radius = diameter / 2  # 计算半径

    # 计算每颗球的体积，即使直径为1
    volume_per_sphere = (4 / 3) * np.pi * radius ** 3

    volume = nx * ny * nz
    volume_filler = volume * C
    n_spheres = int(volume_filler / volume_per_sphere)

    phim = np.ones((nx, ny, nz), dtype=int)  # 初始状态全为基体相
    phif = np.zeros((nx, ny, nz), dtype=int)  # 初始无填充物
    spheres = []

    for _ in range(n_spheres):
        max_attempts = 1000
        for attempt in range(max_attempts):
            # 随机生成球体中心，确保球体完全在空间内
            x = np.random.randint(int(radius), nx - int(radius)) if diameter > 1 else np.random.randint(0, nx)
            y = np.random.randint(int(radius), ny - int(radius)) if diameter > 1 else np.random.randint(0, ny)
            z = np.random.randint(int(radius), nz - int(radius)) if diameter > 1 else np.random.randint(0, nz)
            center = np.array([x, y, z])

            # 检查新球体是否与已有的球体重叠
            if not any(np.linalg.norm(center - s) < diameter for s in spheres):
                spheres.append(center)

                # 当直径为1时，每个格点就是一个球
                if diameter == 1:
                    phif[center[0], center[1], center[2]] = 1
                    phim[center[0], center[1], center[2]] = 0
                else:
                    # 标记填充相
                    for i in range(max(0, x - int(radius)), min(nx, x + int(radius) + 1)):
                        for j in range(max(0, y - int(radius)), min(ny, y + int(radius) + 1)):
                            for k in range(max(0, z - int(radius)), min(nz, z + int(radius) + 1)):
                                if np.linalg.norm([i - x, j - y, k - z]) <= radius:
                                    phif[i, j, k] = 1
                                    phim[i, j, k] = 0  # 更新基体相为0
                break  # 成功放置球体，退出尝试循环
            # 如果尝试次数用尽，则退出循环，避免死循环
            if attempt == max_attempts - 1:
                print(f"警告：无法放置所有球体。仅放置了 {len(spheres)} 个中的 {n_spheres} 个。")
                break

    return phim, phif




def visualize_0D_model(phim, phif):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 获取三维数组的维度
    nx, ny, nz = phim.shape

    # 基体相
    X, Y, Z = np.where(phim == 1)
    ax.scatter(X, Y, Z, c='gray', alpha=0.1, s=1)

    # 填料相
    X, Y, Z = np.where(phif == 1)
    ax.scatter(X, Y, Z, c='blue', alpha=0.5, s=1)

    # 设置坐标轴的比例
    ax.set_box_aspect((nx, ny, nz))  # 设置盒子比例

    # 调整视角，使z轴看起来不过分拉长
    ax.view_init(elev=45, azim=-45)  # 调整视角角度，elev为仰角，azim为方位角

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 设置轴的范围来保持比例
    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_zlim(0, nz)

    plt.show()

if __name__ == '__main__':
    # 示例调用，填入半径为2的球体到50x50x10的空间中
    phim, phif = generate_0D_model(50, 50, 10, 4, 0.01)
    visualize_onelayer_model(phim, phif)