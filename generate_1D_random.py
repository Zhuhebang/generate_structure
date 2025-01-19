from visualize_model import visualize_onelayer_model
import numpy as np




def generate_1D_random_model(nx, ny, nz, diameter, h, C):
    if diameter == 1:
        radius = 0
        is_line = True
    else:
        radius = diameter // 2
        is_line = False

    volume = nx * ny * nz
    volume_filler = volume * C
    n_rods = int(volume_filler / (np.pi * max(radius, 0.5) ** 2 * h))

    phim = np.zeros((nx, ny, nz), dtype=int)
    phif = np.zeros((nx, ny, nz), dtype=int)

    max_attempts = 10000

    def find_nearest_grid_points(start, end, nx, ny, nz):
        x_values = np.linspace(start[0], end[0], 100)
        y_values = np.linspace(start[1], end[1], 100)
        z_values = np.linspace(start[2], end[2], 100)

        points = np.column_stack((x_values, y_values, z_values))
        points = np.round(points).astype(int)
        points = points[(points[:, 0] >= 0) & (points[:, 0] < nx) &
                        (points[:, 1] >= 0) & (points[:, 1] < ny) &
                        (points[:, 2] >= 0) & (points[:, 2] < nz)]
        return np.unique(points, axis=0)

    def is_point_on_rod(point, center, h, angle_xy, angle_z):
        x, y, z = point - center
        y_rot = y * np.cos(angle_xy) - z * np.sin(angle_xy)
        z_rot = y * np.sin(angle_xy) + z * np.cos(angle_xy)
        x_rot = x * np.cos(angle_z) - y_rot * np.sin(angle_z)
        y_rot = x * np.sin(angle_z) + y_rot * np.cos(angle_z)

        if is_line:
            return np.isclose(x_rot, 0) and np.isclose(z_rot, 0) and abs(y_rot) <= h / 2
        else:
            return x_rot ** 2 + z_rot ** 2 <= radius ** 2 and abs(y_rot) <= h / 2

    for _ in range(n_rods):
        for attempt in range(max_attempts):
            # 随机生成圆柱体中心，确保圆柱体完全在空间内
            center_x = np.random.randint(radius, nx - radius)
            center_y = np.random.randint(radius, ny - radius)
            center_z = np.random.randint(radius, nz - radius)
            center = np.array([center_x, center_y, center_z], dtype=int)

            # 限制夹角小于45度
            angle_xy = np.arccos(np.random.uniform(np.cos(np.pi / 4), 1))
            angle_z = np.random.uniform(0, 2 * np.pi)

            # 计算棒的两端点，确保在边界内
            half_h = h / 2  # 使用h来计算端点距离
            dy = half_h * np.sin(angle_xy)
            dz = half_h * np.cos(angle_xy)
            dx = dy * np.tan(angle_z)

            start = center - np.array([dx, dy, dz])
            end = center + np.array([dx, dy, dz])

            # 确保两端点在边界内
            if (0 <= start[0] < nx - diameter and 0 <= start[1] < ny - diameter and 0 <= start[2] < nz - diameter and
                    0 <= end[0] < nx - diameter and 0 <= end[1] < ny - diameter and 0 <= end[2] < nz - diameter):

                line_points = find_nearest_grid_points(start, end, nx, ny, nz)

                overlap = False
                for point in line_points:
                    if phif[point[0], point[1], point[2]] == 1:
                        overlap = True
                        break

                if not overlap:
                    for point in line_points:
                        phif[point[0], point[1], point[2]] = 1
                    break

            if attempt == max_attempts - 1:
                print(f"Warning: Failed to place all rods. Only placed {_} of {n_rods}.")
                break

    phim = 1 - phif
    return phim, phif



if __name__ == '__main__':
    nx, ny, nz = 50, 50, 30
    diameter = 6  # 棒的底面直径
    h = 15  # 棒的高度
    C = 0.03  # 填充系数

    phim, phif = generate_1D_random_model(nx, ny, nz, diameter, h, C)
    visualize_onelayer_model(phim, phif)