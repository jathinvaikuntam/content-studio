import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

from prompts import (
    LINKEDIN_PROMPT,
    EMAIL_PROMPT,
    BLOG_PROMPT,
    INSTAGRAM_PROMPT
)

st.set_page_config(
    page_title="Content Studio",
    page_icon="📝" ,
    layout="wide",
)

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")



with st.sidebar:
    st.title(" Content Studio")

    st.markdown("---")

    st.subheader("About")

    st.markdown("""
    This ai content studio helps you generate:

    ✅ LinkedIn Posts

    ✅ Cold Emails

    ✅ Blog Outlines

    ✅ Instagram Captions
    """)

    st.markdown("---")

    st.info(
        "Built with Streamlit + Gemini"
    )

   




if not API_KEY:
    st.error(
        "❌ GEMINI_API_KEY not found in .env file"
    )
    st.stop()



try:
    client = genai.Client(api_key=API_KEY)

except Exception as e:
    st.error(f"Gemini Error: {e}")
    st.stop()



st.title(" Content Studio")

st.caption(
    "Generate professional content using Gemini AI"
)



tab1, tab2, tab3, tab4 = st.tabs([
    "LinkedIn Post",
    "Cold Email",
    "Blog Outline",
    "Instagram Caption"
])


def generate_content(
    prompt_template,
    user_input,
    tone,
    word_count
):
    MAX_TOKENS = 3000

    token_count = client.models.count_tokens(
        model="gemini-2.5-flash",
        contents=user_input
    )
    actual_tokens = token_count.total_tokens

    if actual_tokens > MAX_TOKENS:
        st.error(
        f"Document exceeds token limit.\n"
        f"Actual Tokens: {actual_tokens}\n"
        f"Maximum Allowed: {MAX_TOKENS}"
    )
        st.stop()


    final_prompt = f"""
    {prompt_template}

    Tone:
    {tone}

    Word Count:
    {word_count}

    User Request:
    {user_input}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt
    )

    return response.text



with tab1:

    st.subheader("LinkedIn Post Generator")

    left, right = st.columns(2)

    with left:

        topic = st.text_area(
            "What is your LinkedIn post about?",
            height=200
        )

        tone = st.radio(
            "Select Tone",
            [
                "Professional",
                "Casual",
                "Witty",
                "Hinglish"
            ],
            key="linkedin_tone"
        )

        words = st.slider(
            "Word Count",
            50,
            500,
            200,
            key="linkedin_words"
        )

        generate = st.button(
            "Generate LinkedIn Post"
        )

    with right:

        if generate:

            if not topic.strip():
                st.warning(
                    "Please enter a topic."
                )

            else:

                with st.spinner(
                    "Generating..."
                ):

                    try:

                        result = generate_content(
                            LINKEDIN_PROMPT,
                            topic,
                            tone,
                            words
                        )

                        st.code(
                            result,
                            language="text"
                        )

                        st.download_button(
                            "Download",
                            result,
                            "linkedin_post.txt"
                        )

                    except Exception as e:

                        st.error(
                            f"Error: {e}"
                        )



with tab2:

    st.subheader("Cold Email Generator")

    left, right = st.columns(2)

    with left:

        topic = st.text_area(
            "Email purpose",
            height=200,
            key="email_input"
        )

        tone = st.radio(
            "Tone",
            [
                "Professional",
                "Casual",
                "Witty",
                "Hinglish"
            ],
            key="email_tone"
        )

        words = st.slider(
            "Word Count",
            50,
            500,
            150,
            key="email_words"
        )

        generate = st.button(
            "Generate Email"
        )

    with right:

        if generate:

            if not topic.strip():

                st.warning(
                    "Please enter email details."
                )

            else:

                try:

                    result = generate_content(
                        EMAIL_PROMPT,
                        topic,
                        tone,
                        words
                    )

                    st.code(result)

                    st.download_button(
                        "Download",
                        result,
                        "email.txt"
                    )

                except Exception as e:

                    st.error(str(e))



with tab3:

    st.subheader("Blog Outline Generator")

    left, right = st.columns(2)

    with left:

        topic = st.text_area(
            "Blog topic",
            height=200,
            key="blog_input"
        )
           
        tone = st.radio(
            "Tone",
            [
                "Professional",
                "Casual",
                "Witty",
                "Hinglish"
            ],
            key="blog_tone"
        )

        words = st.slider(
            "Word Count",
            50,
            500,
            300,
            key="blog_words"
        )

        generate = st.button(
            "Generate Blog Outline"
        )

    with right:

        if generate:

            if not topic.strip():

                st.warning(
                    "Enter a blog topic."
                )

            else:

                try:

                    result = generate_content(
                        BLOG_PROMPT,
                        topic,
                        tone,
                        words
                    )

                    st.code(result)

                    st.download_button(
                        "Download",
                        result,
                        "blog_outline.txt"
                    )

                except Exception as e:

                    st.error(str(e))



with tab4:

    st.subheader(
        "Instagram Caption Generator"
    )

    left, right = st.columns(2)

    with left:

        topic = st.text_area(
            "Instagram post topic",
            height=200,
            key="insta_input"
        )

        tone = st.radio(
            "Tone",
            [
                "Professional",
                "Casual",
                "Witty",
                "Hinglish"
            ],
            key="insta_tone"
        )

        words = st.slider(
            "Word Count",
            50,
            500,
            100,
            key="insta_words"
        )

        generate = st.button(
            "Generate Caption"
        )

    with right:

        if generate:

            if not topic.strip():

                st.warning(
                    "Enter a topic."
                )

            else:

                try:

                    result = generate_content(
                        INSTAGRAM_PROMPT,
                        topic,
                        tone,
                        words
                    )

                    st.code(result)

                    st.download_button(
                        "Download",
                        result,
                        "instagram_caption.txt"
                    )

                except Exception as e:

                    st.error(str(e))