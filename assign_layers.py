
def assign_layers_infor(
        n_layer, ELF_shape, ELF_d, ELF_h, ELF_ori, ELF_initC, ELF_grad,
        OLF_shape, OLF_d, OLF_h, OLF_ori, OLF_initC, OLF_grad
):
    """
    计算每层的信息，包括形状、尺寸、体积分数和厚度。

    :param n_layer: 总层数（如 1, 3, 5, 7）
    :param ELF_shape: 偶数层填料的形状 (0=球形, 1=圆柱形)
    :param ELF_d: 偶数层填料的直径
    :param ELF_h: 偶数层填料的高度（仅圆柱形有效）
    :param ELF_ori: 偶数层填料的方向
    :param ELF_initC: 偶数层的初始体积分数
    :param ELF_grad: 偶数层体积分数的梯度
    :param OLF_shape: 奇数层填料的形状
    :param OLF_d: 奇数层填料的直径
    :param OLF_h: 奇数层填料的高度（仅圆柱形有效）
    :param OLF_ori: 奇数层填料的方向
    :param OLF_initC: 奇数层的初始体积分数
    :param OLF_grad: 奇数层体积分数的梯度
    :return: 包含每层信息的字典
    """
    # 定义存储每层信息的字典
    layers = {}

    if n_layer == 1:
        # 只有 0 层
        layers[0] = {
            "nz": 256,
            "shape": ELF_shape,
            "d": ELF_d,
            "h": ELF_h,
            "ori": ELF_ori,
            "C": ELF_initC  # 偶数层的体积分数
        }
    elif n_layer == 3:
        # 分配为 85, 86, 85
        layers[1] = {
            "nz": 85,
            "shape": OLF_shape,
            "d": OLF_d,
            "h": OLF_h,
            "ori": OLF_ori,
            "C": OLF_initC  # 奇数层体积分数
        }
        layers[0] = {
            "nz": 86,
            "shape": ELF_shape,
            "d": ELF_d,
            "h": ELF_h,
            "ori": ELF_ori,
            "C": ELF_initC  # 偶数层体积分数
        }
        layers[-1] = {
            "nz": 85,
            "shape": OLF_shape,
            "d": OLF_d,
            "h": OLF_h,
            "ori": OLF_ori,
            "C": OLF_initC  # 奇数层体积分数
        }
    elif n_layer == 5:
        # 分配为 51, 51, 52, 51, 51
        layers[2] = {
            "nz": 51,
            "shape": ELF_shape,
            "d": ELF_d,
            "h": ELF_h,
            "ori": ELF_ori,
            "C": ELF_initC + ELF_grad * 1  # 偶数层体积分数
        }
        layers[1] = {
            "nz": 51,
            "shape": OLF_shape,
            "d": OLF_d,
            "h": OLF_h,
            "ori": OLF_ori,
            "C": OLF_initC  # 奇数层体积分数
        }
        layers[0] = {
            "nz": 52,
            "shape": ELF_shape,
            "d": ELF_d,
            "h": ELF_h,
            "ori": ELF_ori,
            "C": ELF_initC  # 偶数层体积分数
        }
        layers[-1] = {
            "nz": 51,
            "shape": OLF_shape,
            "d": OLF_d,
            "h": OLF_h,
            "ori": OLF_ori,
            "C": OLF_initC  # 奇数层体积分数
        }
        layers[-2] = {
            "nz": 51,
            "shape": ELF_shape,
            "d": ELF_d,
            "h": ELF_h,
            "ori": ELF_ori,
            "C": ELF_initC + ELF_grad * 1  # 偶数层体积分数
        }
    elif n_layer == 7:
        # 分配为 37, 36, 37, 36, 37, 36, 37
        layers[3] = {
            "nz": 37,
            "shape": OLF_shape,
            "d": OLF_d,
            "h": OLF_h,
            "ori": OLF_ori,
            "C": OLF_initC + OLF_grad * 1  # 奇数层体积分数
        }
        layers[2] = {
            "nz": 36,
            "shape": ELF_shape,
            "d": ELF_d,
            "h": ELF_h,
            "ori": ELF_ori,
            "C": ELF_initC + ELF_grad * 1  # 偶数层体积分数
        }
        layers[1] = {
            "nz": 37,
            "shape": OLF_shape,
            "d": OLF_d,
            "h": OLF_h,
            "ori": OLF_ori,
            "C": OLF_initC  # 奇数层体积分数
        }
        layers[0] = {
            "nz": 36,
            "shape": ELF_shape,
            "d": ELF_d,
            "h": ELF_h,
            "ori": ELF_ori,
            "C": ELF_initC  # 偶数层的体积分数
        }
        layers[-1] = {
            "nz": 37,
            "shape": OLF_shape,
            "d": OLF_d,
            "h": OLF_h,
            "ori": OLF_ori,
            "C": OLF_initC   # 奇数层体积分数
        }
        layers[-2] = {
            "nz": 36,
            "shape": ELF_shape,
            "d": ELF_d,
            "h": ELF_h,
            "ori": ELF_ori,
            "C": ELF_initC + ELF_grad * 1  # 偶数层体积分数
        }
        layers[-3] = {
            "nz": 37,
            "shape": OLF_shape,
            "d": OLF_d,
            "h": OLF_h,
            "ori": OLF_ori,
            "C": OLF_initC + OLF_grad * 1  # 奇数层体积分数
        }
    else:
        raise ValueError("n_layer 必须为 1、3、5 或 7")

    return layers



if __name__ == "__main__":



    # 偶数层参数
    ELF_shape = 0  # 球形
    ELF_d = 10
    ELF_h = None
    ELF_ori = 0
    ELF_initC = 5
    ELF_grad = 2

    # 奇数层参数
    OLF_shape = 1  # 圆柱形
    OLF_d = 5
    OLF_h = 20
    OLF_ori = 90
    OLF_initC = 8
    OLF_grad = 3

    # 获取层信息
    n_layer = 7
    layers = assign_layers_infor(
        n_layer=n_layer,
        ELF_shape=ELF_shape, ELF_d=ELF_d, ELF_h=ELF_h, ELF_ori=ELF_ori, ELF_initC=ELF_initC, ELF_grad=ELF_grad,
        OLF_shape=OLF_shape, OLF_d=OLF_d, OLF_h=OLF_h, OLF_ori=OLF_ori, OLF_initC=OLF_initC, OLF_grad=OLF_grad
    )

    # 测试访问第 2 层的 nz 和 shape 参数
    print(f"第 3 层的 nz: {layers[3]['nz']}")
    print(f"第 3 层的 shape: {layers[3]['shape']}")

    # 测试访问第 -1 层的体积分数 C
    print(f"第 -3 层的体积分数: {layers[-3]['C']}%")
