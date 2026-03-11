from app.config.settings import env_settings


def main():
    print("=== 全局配置信息 ===")
    print(f"App Name: {env_settings.app_name}")
    print(f"Debug Mode: {env_settings.debug}")
    print("\n=== VLLM 配置信息 ===")
    print(
        f"API Key: {env_settings.vllm_config.vllm_api_key[:10]}...{env_settings.vllm_config.vllm_api_key[-4:]}"
    )
    print(f"Base URL: {env_settings.vllm_config.api_base}")
    print(f"Model: {env_settings.vllm_config.vllm_model_name}")
    print(f"Chat URL: {env_settings.vllm_config.chat_completion_url}")
    print(f"Temperature: {env_settings.vllm_config.vllm_temperature}")
    print(f"Max Tokens: {env_settings.vllm_config.vllm_max_tokens}")


if __name__ == "__main__":
    main()
