from langgraph.graph import START, StateGraph, END
from langchain_openai import ChatOpenAI
from app.config.settings import env_settings


llm = ChatOpenAI(
    base_url=env_settings.vllm.api_base,
    api_key=env_settings.vllm.vllm_api_key,
    model=env_settings.vllm.vllm_model_name,
    temperature=env_settings.vllm.vllm_temperature,
)


def main():
    response = llm.invoke("hello")
    print(response)
    print("-" * 50)
    print(response.content)
    # print(f"total tokens = {response.response_metadata['token_usage']['total_tokens']}")
    print(
        f"total tokens = {response.response_metadata.get('token_usage')['total_tokens']}"
    )


if __name__ == "__main__":
    main()
