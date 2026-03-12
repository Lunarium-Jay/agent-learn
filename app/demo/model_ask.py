from langgraph.graph import START, StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from app.config.settings import env_settings


llm = ChatOpenAI(
    base_url=env_settings.vllm.api_base,
    api_key=env_settings.vllm.vllm_api_key,
    model=env_settings.vllm.vllm_model_name,
    temperature=env_settings.vllm.vllm_temperature,
)


def stream_output():
    # 构建 LangChain 兼容的消息列表
    messages = [
        SystemMessage(content="   "),
        HumanMessage(content="  "),
    ]

    # 使用 stream 方法进行流式调用
    for chunk in llm.stream(messages):
        # chunk 是一个 AIMessageChunk 对象，打印其内容
        print(chunk.content, end="", flush=True)

    print("\n")


if __name__ == "__main__":
    stream_output()
