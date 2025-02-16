from read_csv import dataframe_to_objects, read_csv_to_dataframe
from assign_layers import assign_layers_infor
from generate_0D import generate_0D_model
from generate_1D_flat import generate_1D_flat_model
from generate_1D_random import generate_1D_random_model
from generate_2D_flat import generate_2D_flat_model
from generate_2D_random import generate_2D_random_model
from visualize_model import visualize_nlayer_model
import numpy as np
import os
import time

nx = 256
ny = 256
nz = 256

file_path = 'structure.csv'
dataframe = read_csv_to_dataframe(file_path)  # 读取 CSV 为 DataFrame

if dataframe is not None:
    objects = dataframe_to_objects(dataframe)  # 将 DataFrame 转换为对象字典

    for obj_id, obj in objects.items():
        # print(f"ID={obj_id} 的所有属性：")
        # print(f"{obj.n_layer}")

        layers = assign_layers_infor(obj.n_layer, obj.ELF_shape, obj.ELF_d, obj.ELF_h, obj.ELF_ori, obj.ELF_initC, obj.ELF_grad,
        obj.OLF_shape, obj.OLF_d, obj.OLF_h, obj.OLF_ori, obj.OLF_initC, obj.OLF_grad)

        # 计算第x层的phi
        # ori=0:flat ori=1:random
        # 0球、1线、2片
        def calculate_layers_phi(nx, ny, x, layers):
            phim = np.zeros((nx, ny, layers[x]['nz']), dtype=int)
            phif = np.zeros((nx, ny, layers[x]['nz']), dtype=int)
            # 如果为球
            if layers[x]['shape'] == 0:
                phim, phif = generate_0D_model(nx, ny, layers[x]['nz'], layers[x]['d'], layers[x]['C'])
            # 如果为线且平行分布
            elif layers[x]['shape'] == 1 and layers[x]['ori'] == 0:
                phim, phif = generate_1D_flat_model(nx, ny, layers[x]['nz'], layers[x]['d'], layers[x]['h'],
                                                    layers[x]['C'])
            # 如果为线且随机分布
            elif layers[x]['shape'] == 1 and layers[x]['ori'] == 1:
                phim, phif = generate_1D_random_model(nx, ny, layers[x]['nz'], layers[x]['d'], layers[x]['h'],
                                                      layers[x]['C'])
            # 如果为片且平行分布
            elif layers[x]['shape'] == 2 and layers[x]['ori'] == 0:
                phim, phif = generate_2D_flat_model(nx, ny, layers[x]['nz'], layers[x]['d'], layers[x]['h'],
                                                    layers[x]['C'])
            # 如果为片且随机分布
            elif layers[x]['shape'] == 2 and layers[x]['ori'] == 1:
                phim, phif = generate_2D_random_model(nx, ny, layers[x]['nz'], layers[x]['d'], layers[x]['h'],
                                                    layers[x]['C'])
            return phim, phif
        # print(layers)  # 查看 layers 列表的内容
        # print(type(layers[0]))  # 查看第一个元素的类型
        # 循环遍历 layers 中的每个字典
        # 遍历 layers 字典中的每个键值对
        for index, layer in layers.items():
            print(f"Layer {index}:")
            for key, value in layer.items():
                print(f"  {key}: {value}")
            print()  # 输出空行分隔每个层
        phime = np.zeros((nx, ny, nz), dtype=int)
        phife = np.zeros((nx, ny, nz), dtype=int)
        phimo = np.zeros((nx, ny, nz), dtype=int)
        phifo = np.zeros((nx, ny, nz), dtype=int)

        start_time_1 = time.time()

        # 1层情况
        if obj.n_layer == 1:
            phime, phife = calculate_layers_phi(nx, ny, 0, layers)
        # 3层情况
        elif obj.n_layer == 3:
            phimo[:,:,0:85], phifo[:,:,0:85] = calculate_layers_phi(nx, ny, -1, layers)
            phime[:, :,85:171], phife[:, :,85:171] = calculate_layers_phi(nx, ny, 0, layers)
            phimo[:, :,171:256], phifo[:, :,171:256] = calculate_layers_phi(nx, ny, 1, layers)
        # 5层情况
        elif obj.n_layer == 5:
            phime[:, :, 0:51], phife[:, :, 0:51] = calculate_layers_phi(nx, ny, -2, layers)
            phimo[:, :, 51:102], phifo[:, :, 51:102] = calculate_layers_phi(nx, ny, -1, layers)
            phime[:, :, 102:154], phife[:, :, 102:154] = calculate_layers_phi(nx, ny, 0, layers)
            phimo[:, :, 154:205], phifo[:, :, 154:205] = calculate_layers_phi(nx, ny, 1, layers)
            phime[:, :, 205:256], phife[:, :, 205:256] = calculate_layers_phi(nx, ny, 2, layers)
        # 7层情况
        elif obj.n_layer == 7:
            phimo[:, :, 0:37], phifo[:, :, 0:37] = calculate_layers_phi(nx, ny, -3, layers)
            phime[:, :, 37:73], phife[:, :, 37:73] = calculate_layers_phi(nx, ny, -2, layers)
            phimo[:, :, 73:110], phifo[:, :, 73:110] = calculate_layers_phi(nx, ny, -1, layers)
            phime[:, :, 110:146], phife[:, :, 110:146] = calculate_layers_phi(nx, ny, 0, layers)
            phimo[:, :, 146:183], phifo[:, :, 146:183] = calculate_layers_phi(nx, ny, 1, layers)
            phime[:, :, 183:219], phife[:, :, 183:219] = calculate_layers_phi(nx, ny, 2, layers)
            phimo[:, :, 219:256], phifo[:, :, 219:256] = calculate_layers_phi(nx, ny, 3, layers)

        end_time_1 = time.time()
        execution_time_1 = end_time_1 - start_time_1
        print(f"生成结构数据的总执行时间: {execution_time_1:.6f} 秒")
        # 可视化
        #visualize_nlayer_model(phime, phife, phimo, phifo)

        start_time_2 = time.time()
        # 输出结构
        # nx, ny, nz, phime, phife, phimo, phifo,未命名为obj.ID
        # 或者在前几行先输出基体相和填料相的物理参数，在fortran读的时候先读物理参数，再读取结构
        output_dir = "./output"
        with open(os.path.join(output_dir, f"{obj.ID}.txt"), 'w') as f:
            # # 写入前四行空行
            # for _ in range(4):
            #     f.write("\n")
            #
            # # 写入其他需要的数据
            # f.write("Some additional data or header if needed\n")

            # 写入表头
            f.write("x y z phime phife phimo phifo\n")

            # 将每个格点的坐标和相应的四个相写入文件
            for i in range(nx):
                for j in range(ny):
                    for k in range(nz):
                        # 格点坐标为 (i, j, k) 对应的值
                        f.write(f"{i} {j} {k} {phime[i, j, k]} {phife[i, j, k]} {phimo[i, j, k]} {phifo[i, j, k]}\n")

            end_time_2 = time.time()
            execution_time_2 = end_time_2 - start_time_2
            print(f"输出结构文件的执行时间: {execution_time_2:.6f} 秒")