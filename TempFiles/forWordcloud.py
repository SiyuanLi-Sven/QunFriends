import pandas as pd
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        stopwords = set([line.strip() for line in file])
    return stopwords

def generate_wordcloud(text, output_file, stopwords):
    font_path = r'C:\Windows\Fonts\simhei.ttf'  # 字体文件的路径
    wordcloud = WordCloud(font_path=font_path, background_color='white', width=800, height=400, stopwords=stopwords).generate(text)
    plt.figure(figsize=(10, 5),dpi=300)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

def main():
    # 读取CSV文件
    file_path = r'OrganizedData.csv.csv'
    df = pd.read_csv(file_path)

    # 加载停用词库
    stopwords_file_path = r'JiebaStopwords.txt'
    stopwords = load_stopwords(stopwords_file_path)

    # 整体信息的词云
    all_messages = ' '.join(df['Message'].dropna())
    # 使用jieba进行分词并过滤停用词
    all_messages_cut = ' '.join(word for word in jieba.cut(all_messages) if word not in stopwords)
    generate_wordcloud(all_messages_cut, 'all_messages_wordcloud.png', stopwords)

    # 按Sender生成词云
    senders = df['Sender'].unique()
    for sender in senders:
        try:
            sender_messages = ' '.join(df[df['Sender'] == sender]['Message'].dropna())
            # 使用jieba进行分词并过滤停用词
            sender_messages_cut = ' '.join(word for word in jieba.cut(sender_messages) if word not in stopwords)
            generate_wordcloud(sender_messages_cut, f'词云图\{sender}_wordcloud.png', stopwords)
        except:
            print(sender)

if __name__ == '__main__':
    main()
