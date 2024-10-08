# Read .txt file as csv file and test the model

import pandas as pd
from collections import defaultdict
import google.generativeai as genai
import streamlit as st
import os

path = "test_data/exam_2024_01_28"
file = "test_data/exam_2024_01_28/exam_2024_01_28.csv"
df = pd.read_csv(file, quotechar='"', delimiter=',',  engine='c', on_bad_lines='warn', skipinitialspace=True)

genai.configure(api_key=st.secrets.gemini.api_key)
course_book = genai.upload_file('course_book.pdf')
model = genai.GenerativeModel(
            model_name = 'gemini-1.5-flash', )
done = False
try:
    for index, question_number in enumerate(df.question_number.unique()):
        if question_number < 3:
            continue
        sub_questions = df[df.question_number == question_number]
        chat = model.start_chat()
        done = False
        for index, question in enumerate(sub_questions.question):
            # if index < 3:
            #     continue
            q = df.loc[(df.question_number == question_number)&(df.question == question), 'question'].values[0]
            image = df.loc[(df.question_number == question_number)&(df.question == question), 'extra_material'].values[0]
            image = genai.upload_file(os.path.join(path, image)) if image != "Null" else None
            

            if not done:
                if image:
                    response = chat.send_message([course_book, image, "Use the course book provided to answer the following exam question", q]).text
                else:
                    response = chat.send_message([course_book, "Use the course book provided to answer the following exam question", q]).text
                done = True
            else:
                if image:
                    response = chat.send_message([image, "Use the course book previously provided to answer the following exam question", q]).text
                else:
                    response = chat.send_message(["Use the course book previously provided to answer the following exam question", q]).text
            df.loc[(df.question_number == question_number)&(df.question == question), 'response'] = response
            print(f"Question: {question_number} - {index}: {response}")
except Exception as e:
    print(e)

df.to_csv("test_results_exam_2024_01_28.csv")