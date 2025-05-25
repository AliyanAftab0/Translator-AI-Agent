from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client,
)

congfig = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)

translator = Agent(
    name = "Translator Agent",
    instructions = "You are a translator agent. Translate text from Urdu to English.",
)

response = Runner.run_sync(
    translator,
    input = """ہم تہہ دل سے جناب سر علی جواد، سر امین عالم، اور سر ضیاء خان کا شکریہ ادا کرتے ہیں کہ انہوں نے ہمیں ایجنٹک اے آئی جیسے جدید اور مفید موضوع کی تعلیم دی۔ آپ کی محنت، رہنمائی اور خلوصِ نیت ہمارے لیے باعثِ فخر اور علم کا خزانہ ہے۔ اللہ آپ سب کو سلامت رکھے اور مزید کامیابیاں عطا فرمائے۔""",
    run_config = congfig
)
print(f'Input: {response.input}')
print("---")
print(f'Output: {response.final_output}')