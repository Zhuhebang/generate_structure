from visualize_model import visualize_onelayer_model
import numpy as np
import matplotlib.pyplot as plt
import time


def generate_2D_flat_model(nx, ny, nz, diameter, h, C):
    radius = diameter / 2
    volume = nx * ny * nz
    volume_filler = volume * C
    n_cylinders = int(volume_filler / (np.pi * radius ** 2 * h))

    print("————generate_2D_flat————")
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

    start_time = time.time()
    placed_cylinders = 0

    for _ in range(n_cylinders):
        for attempt in range(max_attempts):
            iteration_count += 1
            center_x = np.random.uniform(radius, nx - radius)
            center_y = np.random.uniform(radius, ny - radius)
            center_z = np.random.uniform(h / 2, nz - h / 2)

            # 使用布尔索引优化重叠检测
            x, y, z = np.indices((nx, ny, nz))
            mask = ((x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2) & \
                   (np.abs(z - center_z) <= h / 2)

            if not np.any(phif[mask]):  # 如果没有重叠
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

    end_time = time.time()
    print(f"该层总迭代次数: {iteration_count}")
    print(f"该层总运行时间: {end_time - start_time:.4f} 秒")

    # 绘制折线图
    # fig, ax1 = plt.subplots()
    # color = 'tab:red'
    # ax1.set_xlabel('Number of Cylinders')
    # ax1.set_ylabel('Iterations', color=color)
    # ax1.plot(cylinders_count, iterations_count, color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    #
    # ax2 = ax1.twinx()
    # color = 'tab:blue'
    # ax2.set_ylabel('Run Time (seconds)', color=color)
    # ax2.plot(cylinders_count, times, color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    #
    # fig.tight_layout()
    # plt.title('Relationship Between Number of Cylinders, Iterations, and Run Time')
    # plt.show()

    phim = 1 - phif
    return phim, phif


if __name__ == '__main__':
    nx, ny, nz = 256, 256, 256
    diameter = 50
    h = 2
    C = 0.05

    start_time_total = time.time()
    phim, phif = generate_2D_flat_model(nx, ny, nz, diameter, h, C)
    end_time_total = time.time()
    print(f"总体运行时间: {end_time_total - start_time_total:.4f} 秒")
    # visualize_onelayer_model(phim, phif)