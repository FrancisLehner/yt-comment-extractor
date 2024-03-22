import pandas as pd
import os
from string import punctuation
import emoji
import re
from utils.wordcloud_generator import wordcloud
from dotenv import load_dotenv

load_dotenv()
directory = os.getenv('directory')

directory_ext = f'{directory}/extracted_comments'

dataframes = {}
def read_all_csv_files(file_directory):
    count = 0
    for root, dirs, files in os.walk(file_directory):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                print("Reading:", file_path)
                df_name = f'df_{count}'
                dataframes[df_name] = pd.read_csv(file_path)
                count += 1
    return dataframes

def concat():
    chunk_list = []

    all_dataframes = read_all_csv_files(directory_ext)
    
    
    concat_df = pd.concat(all_dataframes.values())

    concat_df = concat_df.reset_index()
    concat_df.to_csv("comments_concat_df.csv")
    print(concat_df)


def contains_only_emoji(text):
    return all(emoji.is_emoji(char) for char in text)

def remove_trailing_repeating_letters(word):
    return re.sub(r'(\w)\1*$', r'\1', word)

def common_words():

    concat()
    concat_df_filepath = f'{directory_ext}/comments_concat_df.csv'
    df_concat = pd.read_csv(concat_df_filepath)

    new_data = []
    common_word = df_concat['textOriginal']
    for comment in common_word:
        # Check if comment contains emojis
        if contains_only_emoji(comment):
            new_data.append({'Word': comment})
        else:
            # Remove leading and trailing emojis
            stripped_comment = comment.strip(''.join(c for c in comment if emoji.is_emoji(c)))
            for word in stripped_comment.lower().split():
                word = word.strip().lstrip(punctuation).rstrip(punctuation)
                word = word.replace('yg', 'yang')
                word = word.replace('gua', 'gue')
                word = word.replace('lu', 'lo')
                word = word.replace('gw', 'gue')
                word = word.replace('bgt', 'banget')
                word = remove_trailing_repeating_letters(word)
                if word:
                    new_data.append({'Word': word})

    common_word_df = pd.DataFrame(new_data)
    common_word_df['count'] = 1
    common_word_df = common_word_df.groupby('Word').count()['count']
    common_word_df = common_word_df.sort_values(ascending=False)
    print(common_word_df)
    common_word_df.to_csv('common_words_Jan23_Apr24.csv')

def main():
    common_words()

if __name__ == '__main__':
    main()










