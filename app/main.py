from app.config.settings import env_settings


from app.demo.model_ask import async_stream_output


async def main():
    print("=== 全局配置信息 ===")
    print(f"App Name: {env_settings.app_name}")
    print(f"Debug Mode: {env_settings.debug}")
    print("\n=== VLLM 配置信息 ===")
    print(
        f"API Key: {env_settings.vllm.vllm_api_key[:10]}...{env_settings.vllm.vllm_api_key[-4:]}"
    )
    print(f"Base URL: {env_settings.vllm.api_base}")
    print(f"Model: {env_settings.vllm.vllm_model_name}")
    print(f"Chat URL: {env_settings.vllm.chat_completion_url}")
    print(f"Temperature: {env_settings.vllm.vllm_temperature}")
    print(f"Max Tokens: {env_settings.vllm.vllm_max_tokens}")

    await async_stream_output()


if __name__ == "__main__":
    pass
