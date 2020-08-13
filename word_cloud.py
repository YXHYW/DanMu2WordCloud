import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread

import warnings
warnings.filterwarnings("ignore")

def get_word():
    # 读取文本文件，并使用lcut()方法进行分词
    with open("dan_mu.txt",encoding="utf-8") as f:
        txt = f.read()
    txt = txt.split()
    data_cut = [jieba.lcut(x) for x in txt]

    # 读取停用词
    with open("stopword.txt",'r') as f:
        stop = f.read()
    stop = stop.split()
    stop = [" ","道","说道","说"] + stop

    # 去掉停用词之后的最终词
    s_data_cut = pd.Series(data_cut)
    all_words_after = s_data_cut.apply(lambda x:[i for i in x if i not in stop])
    return all_words_after

def get_word_count(all_words_after):
    # 词频统计
    all_words = []
    for i in all_words_after:
        all_words.extend(i)
    word_count = pd.Series(all_words).value_counts()
    return word_count

if __name__ == "__main__":
    all_words_after = get_word()
    word_count = get_word_count(all_words_after)
    # 词云图的绘制
    # 1、读取背景图片
    back_picture = imread("JPG1.jpg")

    # 2、设置词云参数
    wc = WordCloud(font_path="simhei.ttf",
                background_color="white",
                max_words=500,
                mask=back_picture,
                max_font_size=200,
                random_state=42
                )
    wc2 = wc.fit_words(word_count)

    # 3、绘制词云图
    plt.figure(figsize=(16,9),dpi=300)
    plt.imshow(wc2)
    plt.axis("off")
    wc.to_file("ciyunimg.png")