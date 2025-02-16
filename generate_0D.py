from visualize_model import visualize_onelayer_model
import numpy as np
import matplotlib.pyplot as plt
import time


def generate_0D_model(nx, ny, nz, diameter, C):
    """
    生成一个0D模型，其中球体代表填充物，并输出格点信息。
    :param nx, ny, nz: 体积的维度
    :param diameter: 每个球体的直径
    :param C: 填料的体积分数
    :return: phim (基体相), phif (填充相)
    """
    radius = diameter / 2
    volume_per_sphere = (4 / 3) * np.pi * radius ** 3

    volume = nx * ny * nz
    volume_filler = volume * C
    n_spheres = int(volume_filler / volume_per_sphere)

    print("————generate_0D————")
    # 打印三维空间的格点信息和体积分数及填料数量
    print(f"该层的三维空间维度: {nx} x {ny} x {nz}")
    print(f"球体的直径: {diameter}")
    print(f"体积分数: {C:.2%}")
    print(f"球体的数量: {n_spheres}")
    # 暂停程序，等待用户按下回车键
    # input("按回车键继续...")

    phim = np.ones((nx, ny, nz), dtype=int)
    phif = np.zeros((nx, ny, nz), dtype=int)
    spheres = []

    start_time = time.time()
    iteration_count = 0
    spheres_count = []
    iterations_count = []
    times = []

    for i in range(n_spheres):
        max_attempts = 10000
        for attempt in range(max_attempts):
            iteration_count += 1
            x = np.random.randint(int(radius), nx - int(radius)) if diameter > 1 else np.random.randint(0, nx)
            y = np.random.randint(int(radius), ny - int(radius)) if diameter > 1 else np.random.randint(0, ny)
            z = np.random.randint(int(radius), nz - int(radius)) if diameter > 1 else np.random.randint(0, nz)
            center = np.array([x, y, z])

            if not any(np.linalg.norm(center - s) < diameter for s in spheres):
                spheres.append(center)
                if diameter == 1:
                    phif[center[0], center[1], center[2]] = 1
                    phim[center[0], center[1], center[2]] = 0
                else:
                    for i in range(max(0, x - int(radius)), min(nx, x + int(radius) + 1)):
                        for j in range(max(0, y - int(radius)), min(ny, y + int(radius) + 1)):
                            for k in range(max(0, z - int(radius)), min(nz, z + int(radius) + 1)):
                                if np.linalg.norm([i - x, j - y, k - z]) <= radius:
                                    phif[i, j, k] = 1
                                    phim[i, j, k] = 0
                break  # 成功放置球体后退出内部循环
            if attempt == max_attempts - 1:
                print(f"警告：无法放置所有球体。仅放置了 {len(spheres)} 个中的 {n_spheres} 个。")
                break  # 如果尝试次数用尽，退出内部循环

        # 每成功添加10个球体记录数据并输出
        # if (len(spheres)) % 10 == 0:
        #     current_time = time.time()
        #     elapsed_time = current_time - start_time
        #     spheres_count.append(len(spheres))
        #     iterations_count.append(iteration_count)
        #     times.append(elapsed_time)
        #     print(f"已放置 {len(spheres)} 个球体 - 已用时间: {elapsed_time:.4f} 秒, 迭代次数: {iteration_count}")

    end_time = time.time()
    print(f"该层总迭代次数: {iteration_count}")
    print(f"该层总运行时间: {end_time - start_time:.4f} 秒")

    # 绘制折线图
    # fig, ax1 = plt.subplots()
    #
    # color = 'tab:red'
    # ax1.set_xlabel('Number of Spheres')
    # ax1.set_ylabel('Iterations', color=color)
    # ax1.plot(spheres_count, iterations_count, color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    #
    # ax2 = ax1.twinx()  # Instantiate a second y-axis that shares the same x-axis
    # color = 'tab:blue'
    # ax2.set_ylabel('Run Time (seconds)', color=color)
    # ax2.plot(spheres_count, times, color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    #
    # fig.tight_layout()  # Adjust the plot layout so that the plot fits well in the figure area
    # plt.title('Relationship Between Number of Spheres, Iterations, and Run Time')
    # plt.show()

    return phim, phif


if __name__ == '__main__':
    start_time_total = time.time()
    phim, phif = generate_0D_model(256, 256, 256, 2, 0.05)
    end_time_total = time.time()
    print(f"总体运行时间: {end_time_total - start_time_total:.4f} 秒")
    #visualize_onelayer_model(phim, phif)