import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from datetime import datetime
import os

plt.rcParams['font.sans-serif'] = ['Simhei']  #显示中文
plt.rcParams['axes.unicode_minus'] = False    #显示负号

# 创建OutputTimeseries文件夹，如果不存在
if not os.path.exists('OutputTimeseries'):
    os.makedirs('OutputTimeseries')

# 导入数据
df = pd.read_csv('OrganizedData.csv', encoding='utf-8-sig')

# 将 'Time' 列转换为 datetime 类型
df['Time'] = pd.to_datetime(df['Time'])

# 创建一个新的列 'Hour'，表示每条信息发送的小时
df['Hour'] = df['Time'].dt.hour

# 创建一个新的列 'Day_of_Week'，表示每条信息发送的是一周中的哪一天
df['Day_of_Week'] = df['Time'].dt.dayofweek

# 统计每个用户发送的消息总数
message_count = df['Sender'].value_counts()

# 统计每个用户在各个小时发送的消息数量
message_count_by_hour = df.groupby(['Sender', 'Hour']).size().reset_index(name='Counts')

# 如果sender数量大于20，则只展示前20个
if len(message_count) > 20:
    top_senders = message_count.index[:20]
    message_count = message_count.loc[top_senders]
    message_count_by_hour = message_count_by_hour[message_count_by_hour['Sender'].isin(top_senders)]

# 根据时间范围确定图的宽度
time_range = df['Time'].max() - df['Time'].min()
width = max(10, time_range.days / 30)  # 每30天增加1个单位的宽度

# 绘制每个用户发送的消息总数的柱状图
plt.figure(figsize=(width, 5))
sns.barplot(x=message_count.index, y=message_count.values)
plt.title('Message Counts by Sender')
plt.xlabel('Sender')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('OutputTimeseries/MessageCountsBySender.png')

# 绘制每个用户在各个小时发送的消息数量的热力图
message_count_by_hour_pivot = message_count_by_hour.pivot('Sender', 'Hour', 'Counts').fillna(0)
plt.figure(figsize=(width, 5))
sns.heatmap(message_count_by_hour_pivot, cmap='Blues')
plt.title('Message Counts by Sender and Hour')
plt.xlabel('Hour')
plt.ylabel('Sender')
plt.tight_layout()
plt.savefig('OutputTimeseries/MessageCountsBySenderAndHour.png')
