from visualize_model import visualize_onelayer_model
import numpy as np
import matplotlib.pyplot as plt
import time


def generate_2D_random_model(nx, ny, nz, diameter, h, C):
    """
    生成一个2D_random模型，其中片状体代表填充物，并输出格点信息。
    :param nx, ny, nz: 体积的维度
    :param diameter: 片的直径
    :param h: 片的厚度
    :param C: 填料的体积分数
    :return: phim (基体相), phif (填充相)
    """
    radius = diameter / 2  # 计算半径
    volume = nx * ny * nz
    volume_filler = volume * C
    n_cylinders = int(volume_filler / (np.pi * radius ** 2 * h))  # 计算理论上的圆柱体数量

    print("————generate_2D_random————")
    print(f"该层的三维空间维度: {nx} x {ny} x {nz}")
    print(f"片的直径: {diameter}")
    print(f"片的厚度: {h}")
    print(f"体积分数: {C:.2%}")
    print(f"片数量: {n_cylinders}")
    # input("按回车键继续...")

    phim = np.zeros((nx, ny, nz), dtype=int)
    phif = np.zeros((nx, ny, nz), dtype=int)

    max_attempts = 10000
    iteration_count = 0
    cylinders_count = []
    iterations_count = []
    times = []
    placed_cylinders = 0

    start_time = time.time()

    # 生成网格坐标
    x, y, z = np.indices((nx, ny, nz))

    for _ in range(n_cylinders):
        for attempt in range(max_attempts):
            iteration_count += 1

            # 随机生成圆柱体中心，确保圆柱体完全在空间内
            center_x = np.random.uniform(radius, nx - radius)
            center_y = np.random.uniform(radius, ny - radius)
            center_z = np.random.uniform(h / 2, nz - h / 2)
            center = np.array([center_x, center_y, center_z])

            # 生成随机旋转矩阵
            theta = np.random.uniform(0, 2 * np.pi)  # 绕z轴的旋转
            phi = np.arccos(np.random.uniform(np.cos(np.pi / 4), 1))  # 与z轴的夹角，不超过45度
            psi = np.random.uniform(0, 2 * np.pi)  # 绕新x轴的旋转

            # 生成旋转矩阵
            cos_phi, sin_phi = np.cos(phi), np.sin(phi)
            cos_theta, sin_theta = np.cos(theta), np.sin(theta)
            cos_psi, sin_psi = np.cos(psi), np.sin(psi)

            rotation_matrix = np.array([
                [cos_theta * cos_psi - cos_phi * sin_theta * sin_psi,
                 -cos_theta * sin_psi - cos_phi * sin_theta * cos_psi, sin_phi * sin_theta],
                [sin_theta * cos_psi + cos_phi * cos_theta * sin_psi,
                 -sin_theta * sin_psi + cos_phi * cos_theta * cos_psi, -sin_phi * cos_theta],
                [sin_phi * sin_psi, sin_phi * cos_psi, cos_phi]
            ])

            # 计算每个点相对于圆柱体中心的偏移
            dx = x - center_x
            dy = y - center_y
            dz = z - center_z

            # 应用旋转矩阵（简单实现，仅考虑x和y平面的旋转）
            new_x = dx * np.cos(theta) - dy * np.sin(theta)
            new_y = dx * np.sin(theta) + dy * np.cos(theta)
            new_z = dz * np.cos(phi) - new_x * np.sin(phi)

            # 检查是否在圆柱体内
            mask = (new_x ** 2 + new_y ** 2 <= radius ** 2) & (np.abs(new_z) <= h / 2)

            if not np.any(phif[mask]):  # 没有重叠
                phif[mask] = 1
                placed_cylinders += 1
                break

        # if placed_cylinders % 10 == 0 and placed_cylinders > 0:
        #     current_time = time.time()
        #     elapsed_time = current_time - start_time
        #     cylinders_count.append(placed_cylinders)
        #     iterations_count.append(iteration_count)
        #     times.append(elapsed_time)
        #     print(f"已放置 {placed_cylinders} 个片 - 已用时间: {elapsed_time:.4f} 秒, 迭代次数: {iteration_count}")
        #
        # if attempt == max_attempts - 1:
        #     print(f"警告：无法放置所有圆柱体。仅放置了 {placed_cylinders} 个中的 {n_cylinders} 个。")
        #     break

    end_time = time.time()
    print(f"该层总迭代次数: {iteration_count}")
    print(f"该层总运行时间: {end_time - start_time:.4f} 秒")

    # 绘制折线图
    # fig, ax1 = plt.subplots()
    #
    # color = 'tab:red'
    # ax1.set_xlabel('Number of Cylinders')
    # ax1.set_ylabel('Iterations', color=color)
    # ax1.plot(cylinders_count, iterations_count, color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    #
    # ax2 = ax1.twinx()  # 实例化第二个y轴共用x轴
    # color = 'tab:blue'
    # ax2.set_ylabel('Run Time (seconds)', color=color)
    # ax2.plot(cylinders_count, times, color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    #
    # fig.tight_layout()  # 调整子图参数，使之填充整个图形区域
    # plt.title('Relationship Between Number of Cylinders, Iterations, and Run Time')
    # plt.show()

    phim = 1 - phif
    return phim, phif


if __name__ == '__main__':
    nx, ny, nz = 256, 256, 256
    diameter = 50  # 圆柱底面直径
    h = 2  # 圆柱高度
    C = 0.05  # 填充系数

    start_time_total = time.time()
    phim, phif = generate_2D_random_model(nx, ny, nz, diameter, h, C)
    end_time_total = time.time()
    print(f"总体运行时间: {end_time_total - start_time_total:.4f} 秒")
    # visualize_onelayer_model(phim, phif)