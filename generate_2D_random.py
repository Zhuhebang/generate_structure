from visualize_model import visualize_onelayer_model
import numpy as np
import matplotlib.pyplot as plt



def generate_2D_random_model(nx, ny, nz, diameter, h, C):
    radius = diameter / 2  # 计算半径
    volume = nx * ny * nz
    volume_filler = volume * C
    n_cylinders = int(volume_filler / (np.pi * radius ** 2 * h))  # 计算理论上的圆柱体数量，但这里只是估算

    phim = np.zeros((nx, ny, nz), dtype=int)
    phif = np.zeros((nx, ny, nz), dtype=int)

    max_attempts = 10000

    def is_point_inside_rotated_cylinder(point, center, radius, h, angle_xy, angle_z):
        x, y, z = point - center
        # 旋转到标准位置，首先绕Z轴旋转，然后绕Y轴旋转
        x_rot = x * np.cos(angle_z) - y * np.sin(angle_z)
        y_rot = x * np.sin(angle_z) + y * np.cos(angle_z)
        z_rot = z * np.cos(angle_xy) - x_rot * np.sin(angle_xy)
        x_rot = x_rot * np.cos(angle_xy) + z * np.sin(angle_xy)

        # 检查点是否在圆柱体内，考虑浮点精度
        return x_rot ** 2 + y_rot ** 2 <= (radius + 1e-6) ** 2 and abs(z_rot) <= (h / 2 + 1e-6)

    def fill_grid_with_cylinder(phif, center, radius, h, angle_xy, angle_z):
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    point = np.array([i, j, k], dtype=float) + 0.5  # 格点中心
                    if is_point_inside_rotated_cylinder(point, center, radius, h, angle_xy, angle_z):
                        phif[i, j, k] = 1

    for _ in range(n_cylinders):
        for attempt in range(max_attempts):
            # 随机生成圆柱体中心，确保圆柱体完全在空间内
            center_x = np.random.uniform(radius, nx - radius)
            center_y = np.random.uniform(radius, ny - radius)
            center_z = np.random.uniform(h / 2, nz - h / 2)
            center = np.array([center_x, center_y, center_z])

            # 随机生成角度
            angle_xy = np.random.uniform(0, 2 * np.pi)  # 绕y轴旋转可以是任意角度
            max_angle = np.pi / 4  # 45度等于π/4弧度
            angle_z = np.arccos(np.random.uniform(np.cos(max_angle), 1))  # 确保法线与Z轴的夹角不超过45度

            # 检查新圆柱体是否与已有的圆柱体重叠
            overlap = False
            for i in range(nx):
                for j in range(ny):
                    for k in range(nz):
                        if phif[i, j, k] == 1:  # 检查已填充的点
                            if is_point_inside_rotated_cylinder(np.array([i, j, k]) + 0.5, center, radius, h, angle_xy, angle_z):
                                overlap = True
                                break
                    if overlap:
                        break
                if overlap:
                    break

            if not overlap:
                fill_grid_with_cylinder(phif, center, radius, h, angle_xy, angle_z)
                break
            if attempt == max_attempts - 1:
                print(f"Warning: Failed to place all cylinders. Only placed {_} of {n_cylinders}.")
                break

    phim = 1 - phif
    return phim, phif



if __name__ == '__main__':
    nx, ny, nz = 50, 50, 20
    diameter = 10  # 圆柱底面直径（比h大）
    h = 1  # 圆柱高度
    C = 0.002  # 填充系数

    phim, phif = generate_2D_random_model(nx, ny, nz, diameter, h, C)
    visualize_onelayer_model(phim, phif)