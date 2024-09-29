import pandas as pd


def write_to_csv(new_id, new_name, new_reg_time, new_conf,
                 csv_file='/home/ljw/pythonfile/zhian_school/face/existed_name.csv', ):
    """

    :param new_id: 学生id
    :param new_name: 学生姓名
    :param new_reg_time: 签到时间
    :param new_conf: 识别置性度
    :param csv_file: csv文件路径
    :return: None
    """
    # 尝试读取CSV文件，如果文件不存在或为空且没有表头，则创建一个空的DataFrame并添加表头
    if new_id == 'Unknown': return

    try:
        df = pd.read_csv(csv_file)
        # 检查是否缺少表头
        if set(df.columns) != {'id', 'name', 'reg_time', 'conf'}:
            # 如果表头不匹配，可能需要重新考虑如何处理这种情况，这里简单假设我们可以忽略它
            # 但通常更好的做法是抛出一个错误或通知用户
            print("Warning: CSV file headers do not match expected columns.")
    except FileNotFoundError:
        # 如果文件不存在，创建一个新的DataFrame并添加表头
        df = pd.DataFrame(columns=['id', 'name', 'reg_time', 'conf'])
    except Exception as e:
        # 捕获其他可能的异常，并打印错误信息
        print(f"An error occurred while reading the CSV file: {e}")
        return

        # 创建一个新的DataFrame来保存新的记录
    new_record = pd.DataFrame({
        'id': [new_id],
        'name': [new_name],
        'reg_time': [new_reg_time],
        'conf': [new_conf]
    })
    lst = [str(item) for item in df['id'].values.tolist()]
    # print(new_id in lst)
    # 检查id是否已存在
    if new_id in lst:
        # 如果存在，更新reg_time和conf
        df.loc[df['id'] == new_id, ['reg_time', 'conf']] = [new_reg_time, new_conf]
    else:
        # 如果不存在，将新记录添加到DataFrame的末尾
        df = pd.concat([df, new_record], ignore_index=True)

        # 将更新后的DataFrame写回CSV文件
    df.to_csv(csv_file, index=False)


# 使用示例

