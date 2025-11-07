from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from schemas import AgentResponse

load_dotenv()





@tool
def get_text_length(text: str) -> int:
    """ returns the length of the text """
    return len(text)



tools = [get_text_length]



tools = [TavilySearch()]
llm = ChatOpenAI(model="gpt-4o-mini")

# Create agent with structured output using ToolStrategy
agent = create_agent(
    model=llm,
    tools=tools,
    response_format=ToolStrategy(AgentResponse),
    system_prompt="You are a helpful assistant. Search for information and provide detailed answers with sources."
)


def main():
    print("Hello from langchain-course!")

    # Invoke the agent with the new API
    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Search for 3 job postings for a AI engineer  in the bay area on linkedin and list their details in today's date"
            }
        ]
    })

    # Access the structured response
    structured_response = result["structured_response"]
    print("\nAnswer:", structured_response.answer)
    print("\nSources:")
    for source in structured_response.sources:
        print(f"  - {source.url}")


if __name__ == "__main__":
    main()
