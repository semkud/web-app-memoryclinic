import streamlit as st
import pandas as pd
import random

df_words = pd.read_csv('C:/Users/SKudr/PycharmProjects/Masterskaya/bd_words.csv')

st.title('Составитель списка определений для тренировки в Клинике памяти')

st.write('Составить список слов')
version = st.selectbox('Настройки', ('Простые', 'Сложные'))
if version == 'Простые':
    st.write('Вы получите список из случайных определений.')
    how_many = st.slider('Сколько определений вы хотите?', 5, 25)
    selected_ids = random.sample(set(range(1, len(df_words['ID'].tolist()), 1)), int(how_many))
    mystring = ''
    for i in selected_ids:
        mystring += str(df_words[df_words['ID'] == i]['Определение'].tolist()[0]) + '\n\n__________________________________\n'
    st.download_button(label='Скачать определения', data=mystring, file_name='defenitions.txt')
if version == 'Сложные':
    st.write('### Все слова', df_words)
    selected_words = st.multiselect('Выберите слова:', df_words['Слово'].tolist())
    selected_ids = []
    for word in selected_words:
        selected_ids+=(df_words[df_words['Слово']==word]['ID'].tolist())
    mystring = ''
    for i in selected_ids:
        mystring += str(df_words[df_words['ID'] == i]['Определение'].tolist()[0])+'\n\n__________________________________\n'
    st.download_button(label = 'Скачать определения', data = mystring, file_name='defenitions.txt')
