# Core Pkgs
import streamlit as st

st.set_page_config(
    page_title="⭐NLP⭐",
    page_icon="🗿",
    layout="centered",
    initial_sidebar_state="expanded",
)

# NLP Pkgs
from textblob import TextBlob
import spacy
import neattext as nt

from collections import Counter
import re


def summrize_text(text, num_sentences=3):
    # Remove special characters and change text to lower case
    clean_text = re.sub("[^a-zA-Z0-9.]", " ", text).lower()

    # Split the text into words
    words = clean_text.split()

    # Calculate the frequency of each word
    word_freq = Counter(words)

    # Sort the words based on their frequency in descending order
    sorted_words = sorted(word_freq, key=word_freq.get, reverse=True)

    # Extract the top 'num_sentences' most frequent words
    top_words = sorted_words[:num_sentences]

    # Create a summary by joining the top words
    summary = " ".join(top_words)

    return summary


@st.cache_data
def text_analyzer(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Tokens
    all_data = [(f'"Token":{token.text}, "Lemma":{token.lemma_}') for token in doc]

    return all_data


from deep_translator import GoogleTranslator


# Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib

# may or may not improve performance
# matplotlib.use("Agg")
from wordcloud import WordCloud


def main():
    """NLP web app with Streamlit"""

    st.title("Dummy NLP")

    # title_template = """
    # <div style="background-color:blue; padding:8px;">
    # <h1 style="color:cyan">NLP Web App</h1>
    # </div>
    # """
    # st.markdown(title_template, unsafe_allow_html=True)

    # title_template = """
    # <div class="bg-white">
    # <h1 class="text-white">NLP Web App</h1>
    # </div>
    # """
    # st.components.v1.html(title_template)

    # subheader_template = """
    # <div style="background-color:cyan; padding:8px;">
    # <h3 style="color:blue">Powered by Streamlit</h1>
    # </div>
    # """
    # st.markdown(subheader_template, unsafe_allow_html=True)

    st.sidebar.image("nlp.png", use_column_width=True)

    activity = ["Text Analysis", "Translation", "Sentiment Analysis", "About"]
    choice = st.sidebar.selectbox("Menu", activity)

    if choice == "Text Analysis":
        st.subheader("Text Analysis")
        st.write("")

        raw_text = st.text_area(
            "Write something", "Enter a text in English...", height=300
        )

        if st.button("Analyze"):
            if not raw_text:
                st.warning("Please enter a text")
            else:
                blob = TextBlob(raw_text)
                st.info("Basic Functions")

                col1, col2 = st.columns(2)

                with col1:
                    with st.expander("Basic Info"):
                        st.write("Text Stats")
                        word_desc = nt.TextFrame(raw_text).word_stats()
                        result_desc = {
                            "Length of Text": word_desc["Length of Text"],
                            "Num of Vowels": word_desc["Num of Vowels"],
                            "Num of Consonants": word_desc["Num of Consonants"],
                            "Num of Stopwords": word_desc["Num of Stopwords"],
                        }
                        st.write(result_desc)
                    with st.expander("Stopwords"):
                        st.success("Stop Words List")
                        stop_w = nt.TextExtractor(raw_text).extract_stopwords()
                        st.error(stop_w)

                with col2:
                    with st.expander("Processed Text"):
                        st.success("Stopwords Excluded Text")
                        processed_text = str(
                            nt.TextExtractor(raw_text).remove_stopwords()
                        )
                        st.write(processed_text)
                    with st.expander("Word Cloud"):
                        st.success("Word Cloud")
                        # wc = WordCloud().generate(processed_text)
                        wc = WordCloud().generate(raw_text)
                        fig = plt.figure(1, figsize=(20, 10))
                        plt.imshow(wc, interpolation="bilinear")
                        plt.axis("off")
                        st.pyplot(fig)

                # st.write("")
                # st.write("")
                # st.info("Advanced Features")

                # col3, col4 = st.columns(2)

                # with col3:
                #     with st.expander("Token & Lemmas"):
                #         st.write("T&K")
                #         processed_text_mid = str(
                #             nt.TextFrame(raw_text).remove_stopwords()
                #         )
                #         processed_text_mid = str(
                #             nt.TextFrame(processed_text_mid).remove_puncts()
                #         )
                #         processed_text_fin = str(
                #             nt.TextFrame(processed_text_mid).remove_special_characters()
                #         )
                #         tandl = text_analyzer(processed_text_fin)
                #         st.json(tandl)
                # with col4:
                #     with st.expander("Summarize"):
                #         st.success("Summarize")
                #         summary = summrize_text(raw_text)
                #         st.success(summary)

    if choice == "Translation":
        st.subheader("Translation")
        st.write("")
        st.write("")
        raw_text = st.text_area(
            "Original Text", "Write something to be translated...", height=200
        )
        if len(raw_text.strip()) < 3:
            st.warning("Please provide a text with at least 3 characters...")
        else:
            target_lang = st.selectbox(
                "Target Language",
                [
                    "日本語",
                    "espanōl",
                    "简体中文",
                ],
            )
            if target_lang == "espanōl":
                target_lang = "es"
            elif target_lang == "简体中文":
                target_lang = "zh-CN"
            else:
                target_lang = "ja"

            if st.button("Translate"):
                translator = GoogleTranslator(source="auto", target=target_lang)
                translated_text = translator.translate(raw_text)
                st.write(translated_text)

    if choice == "Sentiment Analysis":
        st.subheader("Sentiment Analysis")
        st.write("")
        st.write("")
        raw_text = st.text_area(
            "Text to analyze", "Write something to be analyzed...", height=200
        )
        if st.button("Analyze"):
            if not raw_text:
                st.warning("Please enter a text")
            else:
                blob = TextBlob(raw_text)
                st.info("Sentiment Analysis")
                st.write(blob.sentiment)
                st.write()

    if choice == "About":
        st.subheader("About")
        st.write("")

        st.markdown(
            """
        ### Another Dummy NLP Web App
        #### made with ❤️ by [Daring Cλlf](https://www.linkedin.com/in/daringcalf)

        😜 😉 😏
        """
        )


if __name__ == "__main__":
    main()
