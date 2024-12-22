import os
from dotenv import load_dotenv
from langchain_together import ChatTogether

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatTogether(
    together_api_key=os.getenv("TOGETHER_API_KEY"),
    model=os.getenv("TOGETHER_MODEL"),
    temperature=0.5
)
