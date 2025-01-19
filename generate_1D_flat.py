from visualize_model import visualize_onelayer_model
import numpy as np


def generate_1D_flat_model(nx, ny, nz, diameter, h, C):
    if diameter == 1:
        radius = 0
    else:
        radius = int(diameter / 2)
    volume = nx * ny * nz
    volume_filler = volume * C
    n_rods = int(volume_filler / (np.pi * (radius + 0.5)**2 * h))  # 避免除以零，+0.5确保体积计算准确

    phim = np.zeros((nx, ny, nz), dtype=int)
    phif = np.zeros((nx, ny, nz), dtype=int)

    max_attempts = 10000

    def is_point_inside_circle(y, z, center_y, center_z, radius):
        if radius == 0:
            return y == center_y and z == center_z
        else:
            return (y - center_y)**2 + (z - center_z)**2 <= radius**2

    def mark_circle(phif, i, center_y, center_z, radius, ny, nz):
        # 标记整个圆柱体底面，但只在边界内
        for j in range(max(0, center_y - radius), min(ny, center_y + radius + 1)):
            for k in range(max(0, center_z - radius), min(nz, center_z + radius + 1)):
                if is_point_inside_circle(j, k, center_y, center_z, radius):
                    phif[i, j, k] = 1

    for _ in range(n_rods):
        for attempt in range(max_attempts):
            # 确保整个棒能在空间内放置完整
            center_x = np.random.randint(0, max(1, nx - h + 1))  # 确保棒长度可以完整放置
            center_y = np.random.randint(radius, ny - radius)  # 确保底面半径可以完整放置
            center_z = np.random.randint(radius, nz - radius)  # 确保底面半径可以完整放置
            center = np.array([center_x, center_y, center_z], dtype=int)

            # 安全距离
            safe_dist = radius + 1  # 确保棒之间有一定的间隔

            overlap = False
            # 检查整个棒的长度范围内的重叠
            for i in range(center_x, center_x + h):
                for j in range(max(0, center_y - safe_dist), min(ny, center_y + safe_dist + 1)):
                    for k in range(max(0, center_z - safe_dist), min(nz, center_z + safe_dist + 1)):
                        if phif[i, j, k] == 1 and is_point_inside_circle(j, k, center_y, center_z, safe_dist):
                            overlap = True
                            break
                    if overlap:
                        break
                if overlap:
                    break

            if not overlap:
                # 标记整个棒的长度
                for i in range(center_x, center_x + h):
                    mark_circle(phif, i, center_y, center_z, radius, ny, nz)
                break
            if attempt == max_attempts - 1:
                print(f"Warning: Failed to place all rods. Only placed {_} of {n_rods}.")
                break

    phim = 1 - phif
    return phim, phif




if __name__ == '__main__':
    nx, ny, nz = 50, 50, 20
    diameter = 2  # 棒的底面直径
    h = 10  # 棒的高度（沿X轴方向）
    C = 0.02  # 填充系数

    phim, phif = generate_1D_flat_model(nx, ny, nz, diameter, h, C)
    visualize_onelayer_model(phim, phif)