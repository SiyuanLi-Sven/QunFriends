import pandas as pd
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import sys
import traceback  # 用于打印异常详细信息

def load_stopwords(file_path):
    # 从文件中加载停用词库
    with open(file_path, 'r', encoding='utf-8') as file:
        stopwords = set([line.strip() for line in file])
    return stopwords

def load_userdict(file_path):
    # 从文件中加载jieba自定义词典，并加入jieba词库
    with open(file_path, 'r', encoding='utf-8') as file:
        for word in file:
            jieba.add_word(word.strip())

def generate_wordcloud(text, output_file, stopwords):
    # 生成词云图
    font_path = r'C:\Windows\Fonts\simhei.ttf'  # 字体文件的路径
    wordcloud = WordCloud(font_path=font_path, background_color='white', width=800, height=400, stopwords=stopwords,max_words=50,collocations=False).generate(text)
    plt.figure(figsize=(10, 5),dpi=300)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

def main():
    # 主程序
    file_path = r'OrganizedData.csv'
    df = pd.read_csv(file_path)  

    # 加载停用词库
    stopwords_file_path = r'JiebaStopwords.txt'
    stopwords = load_stopwords(stopwords_file_path)

    # 加载用户自定义词典
    userdict_file_path = r'JiebaAddwords.txt'
    load_userdict(userdict_file_path)

    # 生成所有消息的词云
    all_messages = ' '.join(df['Message'].dropna())
    all_messages_cut = ' '.join(word for word in jieba.cut(all_messages) if word not in stopwords)
    generate_wordcloud(all_messages_cut, 'all_messages_wordcloud.png', stopwords)

    # 为每个群友生成词云
    senders = df['Sender'].unique()
    total_senders = len(senders)
    for i, sender in enumerate(senders):
        jieba.add_word(sender)  # 将sender的名字加入到jieba词库
        try:
            sender_messages = ' '.join(df[df['Sender'] == sender]['Message'].dropna())
            sender_messages_cut = ' '.join(word for word in jieba.cut(sender_messages) if word not in stopwords)
            generate_wordcloud(sender_messages_cut, f'OutputWordcloud\{sender}_wordcloud.png', stopwords)
        except Exception as e:
            print(f"处理 {sender} 时出现异常:")
            traceback.print_exc()  # 打印异常详细信息

        # 更新进度条
        progress = (i+1) / total_senders  # 计算完成百分比
        sys.stdout.write("\r")
        sys.stdout.write("已完成：{:.2%}    正在进行：{:>15}".format(progress, sender))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
