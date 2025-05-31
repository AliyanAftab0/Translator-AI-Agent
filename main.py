from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os
import streamlit as st
import asyncio

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file."
    )

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

translator = Agent(
    name="Translator Agent",
    instructions="You are a translator agent. Translate text from English to any language.",
)


async def main(user_input, target_language):
    # Update the agent's instructions with the target language
    translator.instructions = f"You are a translator agent. Translate the following text from English to {target_language}. Preserve the original meaning and tone."
    return await Runner.run(translator, input=user_input, run_config=config)


st.set_page_config(
    page_title="English to Any language Translator", page_icon="🌐", layout="wide"
)

st.title("Translator AI Agent 🌐")
st.write("This application translates English to any language using a Gemini model.")

# Complete list of languages
all_languages = [
    "Afrikaans",
    "Albanian",
    "Amharic",
    "Arabic",
    "Armenian",
    "Azerbaijani",
    "Basque",
    "Belarusian",
    "Bengali",
    "Bosnian",
    "Bulgarian",
    "Burmese",
    "Catalan",
    "Cebuano",
    "Chichewa",
    "Chinese (Simplified)",
    "Chinese (Traditional)",
    "Corsican",
    "Croatian",
    "Czech",
    "Danish",
    "Dutch",
    "Esperanto",
    "Estonian",
    "Filipino",
    "Finnish",
    "French",
    "Frisian",
    "Galician",
    "Georgian",
    "German",
    "Greek",
    "Gujarati",
    "Haitian Creole",
    "Hausa",
    "Hawaiian",
    "Hebrew",
    "Hindi",
    "Hmong",
    "Hungarian",
    "Icelandic",
    "Igbo",
    "Indonesian",
    "Irish",
    "Italian",
    "Japanese",
    "Javanese",
    "Kannada",
    "Kazakh",
    "Khmer",
    "Kinyarwanda",
    "Korean",
    "Kurdish",
    "Kyrgyz",
    "Lao",
    "Latin",
    "Latvian",
    "Lithuanian",
    "Luxembourgish",
    "Macedonian",
    "Malagasy",
    "Malay",
    "Malayalam",
    "Maltese",
    "Maori",
    "Marathi",
    "Mongolian",
    "Nepali",
    "Norwegian",
    "Odia",
    "Pashto",
    "Persian",
    "Polish",
    "Portuguese",
    "Punjabi",
    "Romanian",
    "Russian",
    "Samoan",
    "Scots Gaelic",
    "Serbian",
    "Sesotho",
    "Shona",
    "Sindhi",
    "Sinhala",
    "Slovak",
    "Slovenian",
    "Somali",
    "Spanish",
    "Sundanese",
    "Swahili",
    "Swedish",
    "Tajik",
    "Tamil",
    "Tatar",
    "Telugu",
    "Thai",
    "Turkish",
    "Turkmen",
    "Ukrainian",
    "Urdu",
    "Uyghur",
    "Uzbek",
    "Vietnamese",
    "Welsh",
    "Xhosa",
    "Yiddish",
    "Yoruba",
    "Zulu",
]

# Language selection
target_language = st.selectbox(
    "Select target language:",
    options=all_languages,
    index=all_languages.index("Urdu"),  # Default to Urdu
)

st.write("Enter the text you want to translate below:")
user_input = st.text_area(
    "Input Text", height=200, placeholder="Type or paste your text here..."
)
st.write("Made with ❤️ by Aliyan")

if st.button("Translate"):
    if user_input.strip() == "":
        st.error("Input text cannot be empty. Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                response = asyncio.run(main(user_input, target_language))
                st.subheader(f"Translated Text Into ({target_language}):")
                st.write(response.final_output)
            except Exception as e:
                st.error(f"An error occurred during translation: {str(e)}")