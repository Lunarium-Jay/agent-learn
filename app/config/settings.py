# config.py
"""
VLLM 配置管理模块
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class VLLMSettings(BaseSettings):
    """VLLM API 配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # 必填项
    vllm_api_key: str
    vllm_base_url: HttpUrl
    vllm_model_name: str

    # 可选项（带默认值）
    vllm_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    vllm_max_tokens: int = Field(default=2048, ge=1)
    vllm_top_p: float = Field(default=0.9, ge=0.0, le=1.0)

    @field_validator("vllm_base_url", mode="before")
    @classmethod
    def normalize_url(cls, v: str) -> str:
        """确保 URL 格式正确"""
        v = str(v)
        # 移除末尾的 /v1/ 或 /v1，统一处理
        v = v.rstrip("/")
        if v.endswith("/v1"):
            v = v[:-3]
        return v + "/"

    @property
    def api_base(self) -> str:
        """OpenAI 格式的基础 URL"""
        return str(self.vllm_base_url) + "v1/"

    @property
    def chat_completion_url(self) -> str:
        """完整的聊天补全接口 URL"""
        return f"{self.api_base}chat/completions"

    @property
    def is_local(self) -> bool:
        """检测是否为本地部署"""
        return any(
            x in str(self.vllm_base_url)
            for x in ["192.168.", "10.", "172.", "127.", "localhost"]
        )


class Settings(BaseSettings):
    """应用全局配置"""

    # 可以手动指定 .env 文件的位置, 而不使用load_env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "VLLM-App"
    debug: bool = True
    log_level: str = "info"

    # 嵌套 VLLM 配置，支持 settings.vllm_config.xxx 访问
    vllm_config: VLLMSettings = Field(default_factory=VLLMSettings)


@lru_cache()
def get_settings() -> Settings:
    """获取全局配置单例"""
    return Settings()


# 导出全局 settings 对象
env_settings = get_settings()


if __name__ == "__main__":
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
