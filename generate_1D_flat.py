from visualize_model import visualize_onelayer_model
import numpy as np
import matplotlib.pyplot as plt
import time

def generate_1D_flat_model(nx, ny, nz, diameter, h, C):
    """
    生成一个1D_flat模型，其中棒体代表填充物，并输出格点信息。
    :param nx, ny, nz: 体积的维度
    :param diameter: 每个棒的直径
    :param h: 每个棒的长度
    :param C: 填料的体积分数
    :return: phim (基体相), phif (填充相)
    """
    if diameter == 1:
        radius = 0
    else:
        radius = int(diameter / 2)
    volume = nx * ny * nz
    volume_filler = volume * C
    n_rods = int(volume_filler / (np.pi * (radius + 0.5)**2 * h))  # 避免除以零，+0.5确保体积计算准确

    print("————generate_1D_flat————")
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
    placed_rods = 0  # 定义放置的棒体的计数器

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
            iteration_count += 1
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
                placed_rods += 1  # 增加成功放置的棒体数量
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
    nx, ny, nz = 100, 100, 100
    diameter = 1
    h = 20
    C = 0.05

    start_time_total = time.time()
    phim, phif = generate_1D_flat_model(nx, ny, nz, diameter, h, C)
    end_time_total = time.time()
    print(f"总体运行时间: {end_time_total - start_time_total:.4f} 秒")
    visualize_onelayer_model(phim, phif)