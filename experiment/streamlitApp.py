# streamlit is used for creating web apps quickly

import sys
import os
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from langchain_community.callbacks.manager import get_openai_callback
from mcqgenerator.utils import read_file, get_table_data
from mcqgenerator.MCQGenerator import generate_evaluate_chain
from mcqgenerator.logger import logging
with open(r'C:\Users\aakri\mcqgen_proj1\experiment\response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)


st.title("AI MCQ Generator")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or Text file")
    
    mcq_count = st.number_input("No. of MCQs", min_value = 3, max_value=50)
    subject = st.text_input("Insert subject", max_chars = 20)
    tone=st.text_input("Complexity of questions", max_chars = 20, placeholder = "simple, moderate, complex")
    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("LOADING..."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": RESPONSE_JSON
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens Used: {cb.total_tokens}")

                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: ${cb.total_cost}")
                if isinstance(response, dict):
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame
                            df.index=df.index+1
                            st.table(df)
                            st.text_area(label="Review", value = response["review"])
                        else:
                            st.error("error in table data")
                else:
                    st.write(response)





























            try:
                text = read_file(uploaded_file)
                st.write("Text extracted successfully!")
                
                with get_openai_callback() as cb:
                    result = generate_evaluate_chain.invoke(
                        text = text,
                        number = mcq_count,
                        subject = subject,
                        tone = tone,
                        response_json = RESPONSE_JSON
                    )
                
                st.success("MCQs generated successfully!")
                st.write("Quiz:", result['quiz'])
                st.write("Review:", result['review'])
                
                quiz_table_data = get_table_data(result['quiz'])
                if quiz_table_data:
                    df = pd.DataFrame(quiz_table_data)
                    st.dataframe(df)
                else:
                    st.error("Error in generating quiz table data.")
                    
            except Exception as e:
                logging.error(f"Error: {e}")
                st.error(f"An error occurred: {e}")