import streamlit as st
import pandas as pd
import openai
import os
import platform

# 🔍 Detect the OS type
os_type = platform.system()

# ✅ Securely initialize OpenAI API Key using environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

#  Before running your app, set the API key in your terminal:
# export OPENAI_API_KEY='sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
if not openai.api_key:
    st.warning("OpenAI API key not found. Please enter it to continue.")
    api_key_input = st.text_input("Enter your OpenAI API Key:", type="password")
    
    if api_key_input:
        openai.api_key = api_key_input
        
        # If Windows, set the environment variable for this session
        if os_type == "Windows":
            os.system(f'setx OPENAI_API_KEY "{api_key_input}"')
            st.success("API Key successfully set for this session!")
        else:
            os.environ["OPENAI_API_KEY"] = api_key_input
            st.success("API Key successfully set for this session!")

    if not openai.api_key:
        st.error("OpenAI API key not found. Application cannot proceed.")
        st.stop()

# Title of the app
st.title("Chatbot")

# ✅ Load the dataset directly
dataset_path = "output_Monday_BI_data.csv"  # Provide full path if not in the same folder

try:
    df = pd.read_csv(dataset_path, encoding='ISO-8859-1')
    st.success("Dataset Loaded Successfully!")
    st.dataframe(df.head())  # Display the first 5 rows of the dataset
except FileNotFoundError:
    st.error(f"Dataset not found at path: {dataset_path}")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while reading the file: {e}")
    st.stop()

# User input
user_input = st.text_input("Ask a question about your dataset:")
if user_input:
    # Prepare the context for the LLM
    context = df.head().to_string(index=False)  # Only send the first 5 rows to avoid token overload
    
    # 🔄 **OpenAI Chat Completion with the NEW SDK method**
    try:
        response = openai.chat_completions.create(  # ✅ Correct method for openai>=1.0.0
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes datasets."},
                {"role": "user", "content": f"{user_input}\n\nHere is the dataset preview:\n{context}"}
            ],
            temperature=0.5,
        )
        
        # Extract and display the response
        bot_response = response['choices'][0]['message']['content']
        st.write("**Bot:**", bot_response)
    except Exception as e:
        st.error(f"An error occurred during OpenAI request: {e}")
