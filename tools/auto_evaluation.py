# Read .txt file as csv file and test the model

import pandas as pd
from collections import defaultdict
import google.generativeai as genai
import streamlit as st
import os

path = "test_data"
file = "questions.csv"
df = pd.read_csv(os.path.join(path, file), quotechar='"', delimiter=',',  engine='c', on_bad_lines='warn', skipinitialspace=True)

# Define the model
genai.configure(api_key=st.secrets.gemini.api_key)
course_book = genai.upload_file('course_book.pdf')
model = genai.GenerativeModel(
            model_name = 'gemini-1.5-flash'
            ,generation_config=genai.types.GenerationConfig(
            temperature=0.0,
            ) )


done = False # To check if the course book has been sent

try:
    for index, question_number in enumerate(df.question_number.unique()):
        sub_questions = df[df.question_number == question_number]
        chat = model.start_chat() # Start the chat for each question - i.e. clear history between questions
        done = False
        for index, question in enumerate(sub_questions.question):
            # if index < 3:   # For when the model has quit prematurely
            #     continue
            q = df.loc[(df.question_number == question_number)&(df.question == question), 'question'].values[0]
            image = df.loc[(df.question_number == question_number)&(df.question == question), 'extra_material'].values[0]
            image = genai.upload_file(os.path.join(path, image)) if image != "Null" else None
            # image = None

            if not done:
                if image:
                    response = chat.send_message([course_book, image, "Use the course book provided to answer the following question. Answer in latex format. Refer to the specific sections in the course book used for your answer.", q]).text
                else:
                    response = chat.send_message([course_book, "Use the course book provided to answer the following question. Answer in latex format. Refer to the specific sections in the course book used for your answer.", q]).text
                done = True
            else:
                if image:
                    response = chat.send_message([image, "Use the course book previously provided to answer the following question. Answer in latex format. Refer to the specific sections in the course book used for your answer.", q]).text
                else:
                    response = chat.send_message(["Use the course book previously provided to answer the following question. Answer in latex format. Refer to the specific sections in the course book used for your answer.", q]).text
            df.loc[(df.question_number == question_number)&(df.question == question), 'response'] = response
            print(f"Question: {question_number} - {index}: {response}")
except Exception as e:
    print(e)

# Print results to csv
df.to_csv(os.path.join(path,"questionsWOContest.csv"), index=False)
df.to_excel(os.path.join(path,"questionsWOContest.xlsx"), index=False)