from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2
)
response = model.invoke("tell me something about the sun in 2 sentences")
print(response.content)
