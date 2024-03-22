import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from get_file_directory import get_file_directory

file_directory = get_file_directory()

def wordcloud():

    # Get Text
    df = pd.read_csv(f'{file_directory}/extracted_comments/common_words_Jan23_Apr24.csv') 

    df['Word'] = df['Word'].astype(str)
    df['count'] = df['count'].astype(int)

    word_frequencies = dict(zip(df['Word'], df['count']))
    text = ' '.join(word for word in word_frequencies.keys())
    
    stopwords_custom = ['gue', 'di', 'd', 'aku', 'saya', 'yang', 'dan', 'itu', 'banget', 'ini', 'ada', 'ya', 'ga', 'bisa', 'aja', 'nya', 'kalo', 'kalau', 'tapi', 'lo', 'kamu', 'buat', 'untuk', 'ke', 'apa', 'dia', 'hanya', 'melakukan', "tidak", 'dia', 'milikku', "apa", 'aku', 'seperti', 'tidak bisa', "dia", 'di bawah', 'lagi', "kamu akan", "bukan", 'kita', "aku", 'berakhir', 'dirinya sendiri', 'siapa', 'setelah', 'sekali', 'akan', 'kami', 'kamu', "tidak", 'adalah', 'sebagian besar', "tidak", 'sejak', 'http', 'karena', "belum", 'untuk', "belum", 'mati', 'siapa', 'suka', 'harus', "tidak boleh", 'selanjutnya', "ada", 'aktif', 'ke', 'yang mana', "bisa 't", 'milikmu', 'karena itu', "aku sudah", 'yang lain', "kita akan", 'a', 'k', 'itu', 'diri kita sendiri', "kamu akan", 'daripada', 'yang', 'dirimu sendiri', 'dari', "bukan", 'milikmu', 'tidak', 'bisa', 'dan', 'dirinya sendiri', "ayo", 'oleh', 'melakukan', "tidak", 'r', 'aku', 'melawan', 'di sini', 'yang', 'dalam', 'selama', 'sementara', "dia", "ini", 'diri mereka sendiri', 'milik kita', 'dia', 'jika', 'sebaliknya', 'diriku sendiri', "tidak akan", 'jadi', 'menjadi', 'dia', 'an', "dia akan ", 'dirimu sendiri', 'turun', "aku akan", 'oleh karena itu', 'di sana', 'seharusnya', 'tentang', "tidak seharusnya", 'atau', "kamu", 'adalah ', 'mereka', 'melakukan', "bagaimana", 'itu sendiri', 'sebagai', 'tetapi', 'keluar', 'mengapa', "mereka sudah", 'sangat', 'naik', 'memiliki ', 'tidak', "tidak boleh", 'apapun', 'com', 'keduanya', 'telah', "mereka akan", 'mereka', 'memiliki', 'di atas', "dia akan ", 'itu', 'juga', 'seharusnya', "dia akan", 'sebelum', 'beberapa', 'melakukan', "kapan", 'miliknya', 'memiliki', 'itu', "di mana ", 'sampai', "tidak", 'mereka', 'untuk', 'sedikit', "kita sudah", 'ini', 'itu', 'ini', 'memiliki', "kita akan ", 'sama', 'di mana', 'di bawah', 'di antara', 'miliknya', 'melalui', 'lalu', "tidak bisa", 'hanya', "itu", "kamu sudah", "kita", "mereka", 'menjadi', 'www', 'namun', "tidak akan", "mereka", 'juga', 'memiliki', 'http', 'https', 'wkwk', 'wk', 'wkwkwk', 'wkwkwkwk']
    stopwords = stopwords_custom + list(STOPWORDS)

    mask = np.array(Image.open(f"{file_directory}/assets/cretivox_logo.png"))
    wordcloud = WordCloud(background_color='white', mode='RGBA', max_words=10000, stopwords=stopwords, mask=mask, min_font_size=1, scale=1).generate(text)

    #Create colours
    image_colours = ImageColorGenerator(mask)
    plt.figure(figsize= [7, 7])
    plt.imshow((wordcloud.recolor(color_func=image_colours)), interpolation= 'bilinear')
    plt.axis('off')
    plt.show()


def testwordcloud():
    # Get Text
    text = open(f'{file_directory}/ignore/avengers_script.txt').read()
    
    stopwords = set(STOPWORDS)
    stopwords.add("int")
    stopwords.add("ext")

    mask = np.array(Image.open(f"{file_directory}/assets/cretivox_logo.png"))
    wordcloud = WordCloud(background_color='white', mode='RGBA', max_words=1000, mask=mask, min_font_size=0, stopwords=stopwords).generate(text)

    #Create colours
    image_colours = ImageColorGenerator(mask)
    plt.figure(figsize= [7, 7])
    plt.imshow(wordcloud.recolor(color_func=image_colours), interpolation= 'bilinear')
    plt.axis('off')
    plt.show()
# testwordcloud()
wordcloud()

