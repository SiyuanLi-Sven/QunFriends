import re
import pandas as pd

def parse_chat_record(file_path):
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (.+?)\((\d+)\)\n(.+?)\n\n"

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
    return df

if __name__ == '__main__':
    file_path = r'群名.txt'  # 将此处替换为您的聊天记录文件路径
    chat_df = parse_chat_record(file_path)
    print(chat_df)
    chat_df.to_csv(r"OrganizedData.csv",encoding='utf-8-sig')
