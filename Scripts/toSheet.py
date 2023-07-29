import re
import pandas as pd

def parse_chat_record(file_path):
    pattern = r"(\d{4}-\d{2}-\d{2} \d{1,2}:\d{1,2}:\d{2}) (.+?)\((\d+)\)\n(.+?)\n\n"

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    matches = re.findall(pattern, content)

    data = {
        'Time': [match[0] for match in matches],
        'Sender': [match[1] for match in matches],
        'SenderID': [match[2] for match in matches],
        'Message': [match[3] for match in matches]
    }

    df = pd.DataFrame(data)

    # 把 'Time' 列转换为 datetime 类型
    df['Time'] = pd.to_datetime(df['Time'], format="%Y-%m-%d %H:%M:%S")

    # 然后我们按 'SenderID' 进行分组，并在每个组内按照时间顺序更新 'Sender' 
    df = df.sort_values('Time').groupby('SenderID').apply(lambda group: group.assign(Sender=group['Sender'].iloc[-1]))

    # 恢复原始的行顺序
    df = df.sort_index()

    return df

if __name__ == '__main__':
    file_path = r'聊天记录导出.txt'  # 将此处替换为您的聊天记录文件路径
    chat_df = parse_chat_record(file_path)
    print(chat_df)
    chat_df.to_csv(r"OrganizedData.csv",encoding='utf-8-sig')
