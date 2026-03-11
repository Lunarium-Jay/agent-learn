from app.config.settings import vllm_config


def main():
    print("=== VLLM 配置信息 ===")
    print(f"API Key: {vllm_config.vllm_api_key[:10]}...{vllm_config.vllm_api_key[-4:]}")
    print(f"Base URL: {vllm_config.api_base}")
    print(f"Model: {vllm_config.vllm_model_name}")
    print(f"Chat URL: {vllm_config.chat_completion_url}")
    print(f"Temperature: {vllm_config.vllm_temperature}")
    print(f"Max Tokens: {vllm_config.vllm_max_tokens}")


if __name__ == "__main__":
    main()
