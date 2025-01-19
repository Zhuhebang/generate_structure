from visualize_model import visualize_onelayer_model
import numpy as np
import matplotlib.pyplot as plt


def generate_2D_flat_model(nx, ny, nz, diameter, h, C):
    radius = diameter / 2  # 计算半径
    volume = nx * ny * nz
    volume_filler = volume * C
    n_cylinders = int(volume_filler / (np.pi * radius ** 2 * h))  # 计算理论上的圆柱体数量，但这里只是估算

    phim = np.zeros((nx, ny, nz), dtype=int)
    phif = np.zeros((nx, ny, nz), dtype=int)

    max_attempts = 10000

    for _ in range(n_cylinders):
        for attempt in range(max_attempts):
            # 随机生成圆柱体中心，确保圆柱体完全在空间内
            center_x = np.random.uniform(radius, nx - radius)
            center_y = np.random.uniform(radius, ny - radius)
            center_z = np.random.uniform(h / 2, nz - h / 2)
            center = np.array([center_x, center_y, center_z])

            # 检查新圆柱体是否与已有的圆柱体重叠
            overlap = False
            for i in range(nx):
                for j in range(ny):
                    for k in range(nz):
                        if phif[i, j, k] == 1:  # 检查已填充的点
                            dist = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
                            if dist <= radius and abs(k - center_z) <= h / 2:  # 使用浮点数比较
                                overlap = True
                                break
                    if overlap:
                        break
                if overlap:
                    break

            if not overlap:
                # 标记填料相
                for i in range(nx):
                    for j in range(ny):
                        dist = np.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
                        if dist <= radius:
                            z_start = max(0, int(center_z - h / 2))
                            z_end = min(nz, int(center_z + h / 2))
                            for k in range(z_start, z_end):
                                phif[i, j, k] = 1
                break
            if attempt == max_attempts - 1:
                print(f"Warning: Failed to place all cylinders. Only placed {_} of {n_cylinders}.")
                break

    phim = 1 - phif
    return phim, phif



if __name__ == '__main__':
    nx, ny, nz = 50, 50, 30
    diameter = 10  # 圆柱底面直径（比h大）
    h = 2  # 圆柱高度
    C = 0.05  # 填充系数

    phim, phif = generate_2D_flat_model(nx, ny, nz, diameter, h, C)
    visualize_onelayer_model(phim, phif)