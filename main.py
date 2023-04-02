import streamlit as st
import io
import openai
import json
import pandas as pd

openai.api_key = ''

df = pd.DataFrame(columns=["Question", "Response", "Prescence", "Frequency"])

df.loc[0] = ["Little interest or pleasure in doing things", "","",""]
df.loc[1] = ["Feeling down, depressed, or hopeless", "" , "", ""]
df.loc[2] = ["Trouble falling or staying asleep, or sleeping too much", "","",""]
df.loc[3] = ["Feeling tired or having little energy", "","",""]
df.loc[4] = ["Poor appetite or overeating", "","",""]
df.loc[5] = ["Feeling bad about yourself or that you are a failure or have let yourself or your family down", "","",""]
df.loc[6] = ["Trouble concentrating on things, such as reading the newspaper or watching television", "","",""]
df.loc[7] = ["Moving or speaking so slowly that other people could have noticed. Or the opposite being so fidgety or restless that you have been moving around a lot more than usual", "","",""]
df.loc[8] = ["Thoughts that you would be better off dead, or of hurting yourself in some way", "","",""]

styles = [{'selector':'*',
           'props':[
            ('background-color', '#c1d6ce'),
            ('font-family','sans serif'), 
            ('color','#383536')
           ]}]

st.markdown(
    """
<style>
    div[data-testid="column"] {
    box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
    border-radius: 15px;
    padding: 5% 5% 5% 10%;
    background-color: #24a364;
} 
    div[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"]{
    box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
    border-radius: 15px;
    padding: 5% 5% 5% 10%;
    background-color: #24a364;
} 

    div
</style>
""",
    unsafe_allow_html=True,
)

def process_audio(audio_file):
    # Add your backend logic to process the audio file
    response = openai.Audio.transcribe("whisper-1", audio_file)
    return response

# Title of the app
st.title("OASIS Assistant")

# Add an audio file uploader
uploaded_file = st.sidebar.file_uploader("Upload your audio question:", type=['mp3'])

#create container c
c1 = st.container()
c2 = st.container()

def recordingParse(recording, question):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": f"This is recording of a conversation {recording}. Return the sentence after the question that relativly closesly resembles {question}. If {question} is not found return '2'"}]
    )
    content = completion["choices"][0]["message"]["content"]
    return content

def prescence(response):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": f"This is a paragraph: {response}. Your response will only be 0, 1, or 9. output 0 if the paragaph contains no. output 1 is the paragraph contains yes. if the pararaph is 2 ouput 9"}]
    )
    presc = completion["choices"][0]["message"]["content"]
    return presc
    
def frequency(response):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": f"extrapolate the days from this sentence: {response}"}]
    )
    presc = completion["choices"][0]["message"]["content"]
    return presc

# If the user has uploaded an audio file, process it and display the response
if uploaded_file:
    # Pass the `uploaded_file` object directly to the `process_audio` function
    response = process_audio(uploaded_file)
    
    # Extract the text field directly from the response object
    recording = response["text"]
    with c1:
        with st.expander("See Speech to Text"):
            st.write(response)

    for i in range(9):
        question = df.loc[i, "Question"]
        answer = recordingParse(recording, question)
        df.loc[i, "Response"] = answer

        value = prescence(df.loc[i, "Response"])
        df.loc[i, "Prescence"] = value

        freq = frequency(df.loc[i, "Frequency"])
        df.loc[i, "Frequency"] = freq
    
    df2=df.style.set_table_styles(styles)
    with c2:
        with st.expander("See AI Analysis"):
            st.table(df2)
