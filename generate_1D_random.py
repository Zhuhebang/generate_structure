from visualize_model import visualize_onelayer_model
import numpy as np
import matplotlib.pyplot as plt
import time


def generate_1D_random_model(nx, ny, nz, diameter, h, C):
    """
    生成一个1D_random模型，其中棒体代表填充物，并输出格点信息。
    :param nx, ny, nz: 体积的维度
    :param diameter: 每个棒的直径
    :param h: 每个棒的长度
    :param C: 填料的体积分数
    :return: phim (基体相), phif (填充相)
    """

    if diameter == 1:
        radius = 0
        is_line = True
    else:
        radius = diameter // 2
        is_line = False

    volume = nx * ny * nz
    volume_filler = volume * C
    n_rods = int(volume_filler / (np.pi * max(radius, 0.5) ** 2 * h))

    print("————generate_1D_random————")
    # 打印三维空间的格点信息和体积分数及填料数量
    print(f"该层的三维空间维度: {nx} x {ny} x {nz}")
    print(f"棒的直径: {diameter}")
    print(f"棒的长度: {h}")
    print(f"体积分数: {C:.2%}")
    print(f"棒的数量: {n_rods}")
    # 暂停程序，等待用户按下回车键
    # input("按回车键继续...")

    phim = np.zeros((nx, ny, nz), dtype=int)
    phif = np.zeros((nx, ny, nz), dtype=int)

    max_attempts = 10000
    iteration_count = 0
    rods_count = []
    iterations_count = []
    times = []

    start_time = time.time()
    placed_rods = 0

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

    def is_point_on_rod(point, center, h, direction):
        # direction 是单位向量，表示棒的方向
        relative_point = point - center
        # 投影到棒方向上的距离
        projection = np.dot(relative_point, direction)
        # 垂直于棒方向的距离
        perpendicular_dist = np.linalg.norm(relative_point - projection * direction)

        if is_line:
            return np.isclose(perpendicular_dist, 0) and abs(projection) <= h / 2
        else:
            return perpendicular_dist <= radius and abs(projection) <= h / 2

    def generate_random_direction(min_angle, max_angle):
        # 使用球面坐标生成随机方向
        # min_angle 和 max_angle 是与z轴的夹角范围（弧度）
        # 极角 theta (与z轴夹角) 在 [min_angle, max_angle] 之间
        cos_theta_min = np.cos(min_angle)
        cos_theta_max = np.cos(max_angle)
        cos_theta = np.random.uniform(cos_theta_max, cos_theta_min)
        theta = np.arccos(cos_theta)

        # 方位角 phi 在 [0, 2π] 之间
        phi = np.random.uniform(0, 2 * np.pi)

        # 转换为笛卡尔坐标系的单位向量
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        return np.array([x, y, z])

    for _ in range(n_rods):
        for attempt in range(max_attempts):
            iteration_count += 1
            # 随机生成圆柱体中心，确保圆柱体完全在空间内
            center_x = np.random.randint(radius, nx - radius)
            center_y = np.random.randint(radius, ny - radius)
            center_z = np.random.randint(radius, nz - radius)
            center = np.array([center_x, center_y, center_z], dtype=int)

            # 生成随机方向，与z轴夹角在45度到135度之间
            min_angle = np.pi / 4  # 45度
            max_angle = 3 * np.pi / 4  # 135度
            direction = generate_random_direction(min_angle, max_angle)

            # 计算棒的两端点，确保在边界内
            half_h = h / 2
            start = center - half_h * direction
            end = center + half_h * direction

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
                    placed_rods += 1
                    break

            if attempt == max_attempts - 1:
                print(f"Warning: Failed to place all rods. Only placed {placed_rods} of {n_rods}.")
                break

        # 每成功添加10个棒体记录数据并输出
        # if placed_rods % 10 == 0 and placed_rods > 0:
        #     current_time = time.time()
        #     elapsed_time = current_time - start_time
        #     rods_count.append(placed_rods)
        #     iterations_count.append(iteration_count)
        #     times.append(elapsed_time)
        #     print(f"已放置 {placed_rods} 个棒体 - 已用时间: {elapsed_time:.4f} 秒, 迭代次数: {iteration_count}")

    end_time = time.time()
    print(f"该层总迭代次数: {iteration_count}")
    print(f"该层总运行时间: {end_time - start_time:.4f} 秒")

    # 绘制折线图
    # fig, ax1 = plt.subplots()
    #
    # color = 'tab:red'
    # ax1.set_xlabel('Number of Rods')
    # ax1.set_ylabel('Iterations', color=color)
    # ax1.plot(rods_count, iterations_count, color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    #
    # ax2 = ax1.twinx()  # 实例化第二个y轴共用x轴
    # color = 'tab:blue'
    # ax2.set_ylabel('Run Time (seconds)', color=color)
    # ax2.plot(rods_count, times, color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    #
    # fig.tight_layout()  # 调整子图参数，使之填充整个图形区域
    # plt.title('Relationship Between Number of Rods, Iterations, and Run Time')
    # plt.show()

    phim = 1 - phif
    return phim, phif


if __name__ == '__main__':
    nx, ny, nz = 256, 256, 256
    diameter = 1
    h = 100
    C = 0.05

    start_time_total = time.time()
    phim, phif = generate_1D_random_model(nx, ny, nz, diameter, h, C)
    end_time_total = time.time()
    print(f"总体运行时间: {end_time_total - start_time_total:.4f} 秒")
    # visualize_onelayer_model(phim, phif)