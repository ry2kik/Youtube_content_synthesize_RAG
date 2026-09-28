import streamlit as st
from supportingFunctions import (
    extract_video_id,
    get_transcript,
    convert_to_english,
    get_important_topics,
    genarate_notes
)

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

if submit_button:
    if youtube_url and video_language:
        video_url = extract_video_id(youtube_url)
        if video_url:
            with st.spinner('Step 1/3: fetching transcript....'):
                full_transcript = get_transcript(video_url, video_language)

                if video_language != 'en':
                    with st.spinner('Step 1.5/3: Translating transcript into English. That may take few moments......'):
                        full_transcript = convert_to_english(full_transcript)



            if task_options == 'Notes for you':
                with st.spinner('Step 2/3: Extracting important topics ....'):
                    topics = get_important_topics(full_transcript)
                    st.subheader('Important Topics')
                    st.write(topics)

                with st.spinner('Step 3/3: Genarating notes for you ....'):
                    notes = genarate_notes(full_transcript)
                    st.subheader('Notes for you')
                    st.write(notes)

                st.success('Summary and notes genarated.')


            # if task_options == 'Notes for you':
            #     with st.spinner('Step 3/3: Taking important notes about this topic ....'):