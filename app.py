import streamlit as st


with st.sidebar:
    st.title('VidSync AI')
    st.markdown('---')
    st.markdown('Transform any Youtube videos into key topics, a podcast, or a chatbot')
    st.markdown('### Input Details')
    
    # Input Variables
    youtube_url = st.text_input('Youtube URL', placeholder = 'https://www.youtube.com/watch?v=......')
    video_language = st.text_input('Video Language', placeholder = 'ex: en, hi, es, fr', value = 'en')

    task_options = st.radio(
        'Choose what you want to genarate',
        ['Chat with Video', 'Notes for you']
    )

    submit_button = st.button('Start Processing')
    st.markdown('---')

st.markdown('## Youtube Content Synthesizer')
st.markdown('Paste a video link and select a task from the sidebar')