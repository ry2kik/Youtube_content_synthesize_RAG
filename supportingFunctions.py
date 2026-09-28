import re
import time
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

load_dotenv(override = True)

# Initializing the ChatOpenAI model
openai = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0.2)

# Function to get youtube video ID
def extract_video_id(url):
    # Extract the youtube video ID from any valid youtube URL
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    st.error('Invalid youtube URL. PLease enter a valid URl')
    return None

# Function to get the full conversation into text
def get_transcript(video_id, language):
    transcript_api = YouTubeTranscriptApi()
    try:
        transcript_list = transcript_api.fetch(video_id, languages = [ language ])
        full_transcript =" ".join([caption.text for caption in transcript_list.snippets])
        time.sleep(10)
        return full_transcript

    except TranscriptsDisabled:
        return "No caption available for this video"

# Function to translate the caption into english language
def convert_to_english(transcript):
    try:
        prompt = ChatPromptTemplate.from_template(
            """
                You are an expert translator with deep cultural and linguistic knowledge.
                I'll provide you with the a transcript. Your task is to translate it into English with absolute accurancy, preserving:
                - Full meaning and context (no additions, no omittions).
                - Tone and style (formal/informal, emotional/neutral as in original).
                - Nuances, idioms, and cultural expressions (adapt appropriately while keeping intent).
                - Speakers voice (Same perspective, no rewriting into third-person).
                Do not summarize or simplify. The translation should read natuarlly in the targetlanguage and stay as close as possible to the original intent.
                
                transcript: {transcript}
            """
        )

        chain = prompt | openai
        response = chain.invoke({ 'transcript': transcript })
        return response.content

    except Exception as e:
        st.error(f"Error in fetching video { e }")

# Function to get important topics
def get_important_topics(transcript):
    try:
        prompt = ChatPromptTemplate.from_template(
            """
                You are an assistant that extracts the 5 most important topics discusses in a video transcript or summary.
                Rule:
                - Summarize into exactly 6 major points.
                - Each point should represent a key topic or concept, not small details.
                - Keep wording concise and focused on the technical content.
                - Do not phrase them as questions or opinions.
                - Output should be a numbered list.
                - Show only points that discussed in the transcript.

                Here is the transcript: {transcript}
            """
        )

        chain = prompt | openai
        response = chain.invoke({ 'transcript': transcript })
        return response.content

    except Exception as e:
        st.error(f"Error in fetching video { e }")

# Functions to get the notes from the video
def genarate_notes(transcript):
    try:
        prompt = ChatPromptTemplate.from_template(
            """
                You are an AI note-taker. Your task is to read the following transcript of the youtube video and produce well-structured, concise notes.
                
                Requirements:
                  - Present the output as bulleted points, grouped into clear section.
                  - Highlight key takeaways, important facts, and examples with yellow colour.
                  - Use short, clear sentences (No long paragraphs).
                  - If the transcript includes multiple themes, organize them under subheadings
                  - Do not add information that is not present in the transcript.

                Here is the transcript: {transcript}
            """
        )

        chain = prompt | openai
        response = chain.invoke({ 'transcript': transcript })
        return response.content

    except Exception as e:
        st.error(f"Error in fetching video { e }")