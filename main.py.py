import streamlit as st
import pandas as pd
import numpy as np
import random
#прочитали таблицу со словами
#Она должна быть в формате xls excel 1997-2003
df_words = pd.read_csv('bd_words.csv')
#добавляем к словам "сложность". Напоминаю, первые по частотности 25% - легкие
# последние 25% - сложные
diffs = []
#qv = df_words['Частотность'].quantile([0.25,0.75]).tolist()
#for a in df_words['Частотность']:
#    if a <= qv[0]:
#        diffs.append(0)
#    elif a>= qv[1]:
#        diffs.append(2)
#    else:
#        diffs.append(1)
#df_words['diffs'] = diffs
#Это словарь с логинами паролями))
mydict = {'Клиника памяти':1, 'Организация Вторая':2, 's':3}




#Все, что начинается с st имеет отношение к стримлиту
st.title('Составитель списка определений для тренировки в Клинике памяти')
st.write('Авторизуйтесь, пожалуйста')

login = st.text_input('Логин')
password = st.text_input('Пароль')

if str(mydict[login]) == password:
    st.write('Составить список слов')
    version = st.selectbox('Настройки', ('Простые', 'Сложные'))
    if version == 'Простые':  #сложные пока не делаем
        #читаем базу данных пациентов
        df1 = pd.read_csv('bd_clinic.csv')
        #Берем только клинику из логина, берем так хитро,
        #кладя в новый датафрейм, чтобы нумерация строк была с 0 по порядку
        df_clinic = pd.DataFrame(df1[df1['Клиника']==login].values, columns=df1.columns)
        option = st.selectbox('Для кого?', ('Индивидуально или для группы', 'Анонимно'))
        #Для группы это как индивидуально, только вместо ФИО надо ввести название группы типа..
        #Анонимно типа когда не спрашиваем новые-старые, только число и сложность
        if option == 'Индивидуально или для группы':
            who = st.selectbox('Для кого?', ('Из базы', 'Новый испытуемый'))
            if who == 'Из базы':
                #собираем всех из базы в строчный вид
                persons = []
                for i in range(df_clinic.shape[0]):
                    persons.append(str(df_clinic['Фамилия'][i]) +' ' + str(df_clinic['Имя'][i]) +' '
                                  + str(df_clinic['Отчество'][i]) +' ' + str(df_clinic['Год рождения'][i])
                                  +' ' + 'г.р.')
                patient = st.selectbox('Выберите', persons)
                #Получили ID человека
                id_patient = persons.index(patient)
            if who == 'Новый испытуемый':
                st.write('Если хотите для группы, введите в поля "Группа" "Номер" "..."')
                surname = st.text_input('Фамилия')
                name = st.text_input('Имя')
                fname = st.text_input('Отчество')
                date_of_birth = st.date_input('Год рождения')
                df1.append(login, [df_clinic.shape[0]+1, surname, name, fname, date_of_birth, 'NaN', 'NaN'])
                id_patient = 'new'
                #Добавить строку в таблицу физически, пересохранить таблицу
        if option == 'Анонимно':
            id_patient = 'new'

        else:
            pass

        which = st.selectbox('Какие слова?', ('Новые', 'Немного новых, немного старых', 'Только старые', 'Последний лист'))
        how_many = st.selectbox('Сколько слов?', ('20', '15', '10'))
        how_difficult = st.selectbox('Какой сложности?', ('Простые', 'Средние', 'Сложные'))
        #Вот эту функцию надо дописать как раз
        createlist2(how_many)
        #createlist(id_patient, which, how_many, how_difficult)
        with open ('simple_demo.pdf', 'rb') as file:
            btn = st.download_button(label = 'Скачать лист',
                                     data = file,
                                     file_name = 'simple_demo.pdf',
                                     mime = 'pdf')
    if version == 'Сложные':
        st.write('### Full Dataset', df_words)
        selected_indices = st.multiselect('Select rows:', df_words.index)
        selected_rows = df_words.loc[selected_indices]
        st.write('### Selected Rows', selected_rows)


def createlist(id_patient, which, how_many, how_difficult):
    if id_patient=='new':
        #не обращаем внимание на новые старые
        pass
    if which == 'Последний лист':
        #просто выдаем слова с айдишниками, которые лежат в
        #df_clinic[df_clinic['ID']==id_patient]['Последний список']
        pass
    else:
        #Это распределение пропорции между новыми и старыми словами
        new = {'Новые':0.8, 'Немного новых, немного старых':0.5, 'Только старые':0}
        #Это распределение пропорции между простыми средними и сложными
        difficulty = {'Простые':[0.6, 0.2, 0.2], 'Средние':[0.2, 0.6, 0.2], 'Сложные':[0.2,0.2,0.6]}
        #У нас есть датафрейм вордс, в нем есть колонка со сложностью
        #И у нас есть список в df_clinic[df_clinic['ID']==id_patient]['Известные слова']
        #Может быть можно сделать как-то проще, но я придумал такую реализацию:
        #Нужно разбить датафрейм со словами на 6 датафреймов:
        #новые - простые, новые- средние, новые-сложные
        #старые-простые, старые-средние, старые-сложные
        #и потом из каждого датафрейма брать столько случайных слов, сколько я придумал
        #если 10 слов %%% #если 15  %%% если 20
        #новые-старые %%% #новые-старые новые-старые

        #list  = df_old_easy['ID'].tolist()
        #random.sample(list, n))
        #генерация пдф (это на мне)
