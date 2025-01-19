import pandas as pd
import chardet

class RowObject:
    def __init__(self, **kwargs):
        """
        动态初始化对象的属性
        :param kwargs: 每列名和对应的值
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

def read_csv_to_dataframe(file_path):
    """
    读取 CSV 文件并返回 DataFrame
    :param file_path: CSV 文件路径
    :return: pandas.DataFrame
    """
    try:
        # 读取 CSV 文件
        data = pd.read_csv(file_path, encoding='ascii')
        return data
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到。")
    except Exception as e:
        print(f"发生错误：{e}")
        return None

def dataframe_to_objects(dataframe):
    """
    将 DataFrame 转换为自定义对象
    :param dataframe: pandas.DataFrame
    :return: 以 ID 为键的 RowObject 对象字典
    """
    try:
        # 创建一个以 ID 为键，RowObject 为值的字典
        data_objects = {
            row.ID: RowObject(**row._asdict()) for row in dataframe.itertuples(index=False)
        }
        return data_objects
    except Exception as e:
        print(f"发生错误：{e}")
        return None

def detect_encoding(file_path):
    """
    检测 CSV 文件的编码类型
    :param file_path: CSV 文件路径
    :return: 检测到的编码类型
    """
    with open(file_path, 'rb') as file:
        # 读取文件的部分内容以检测编码
        raw_data = file.read(10000)  # 读取前 10,000 字节
        result = chardet.detect(raw_data)
        return result['encoding']

# 测试函数
def test_row_object():
    # 替换 'data.csv' 为您的实际 CSV 文件路径
    file_path = 'structure.csv'
    dataframe = read_csv_to_dataframe(file_path)  # 读取 CSV 为 DataFrame

    if dataframe is not None:
        objects = dataframe_to_objects(dataframe)  # 将 DataFrame 转换为对象字典

        # 循环打印每个 ID 的 ELM_eps 值
        print("每个 ID 的 ELM_eps 值：")
        for obj_id, obj in objects.items():
            print(f"ID={obj_id}, ELM_eps={obj.ELM_eps}")

        # 获取某个 ID 的某个属性值
        target_id = 2  # 要查找的 ID
        if target_id in objects:
            print(f"ID={target_id} 的 ELM_eps 值：{objects[target_id].ELM_eps}")
            print(f"ID={target_id} 的 ELF_eps 值：{objects[target_id].ELF_eps}")
        else:
            print(f"ID={target_id} 不存在")


if __name__ == '__main__':
    # 示例调用
    file_path = 'structure.csv'  # 替换为您的 CSV 文件路径
    encoding = detect_encoding(file_path)
    print(f"检测到的编码类型：{encoding}")
    # 运行测试函数
    test_row_object()
