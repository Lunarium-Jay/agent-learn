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


class AppSettings(BaseSettings):
    """应用全局配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "VLLM-App"
    debug: bool = False
    log_level: str = "info"

    # 嵌套 VLLM 配置（仅此一处，自动实例化）
    vllm: VLLMSettings = Field(default_factory=VLLMSettings)


# 单例获取函数
@lru_cache()
def get_vllm_settings() -> VLLMSettings:
    """获取 VLLM 配置"""
    return VLLMSettings()


@lru_cache()
def get_settings() -> AppSettings:
    """获取完整应用配置"""
    return AppSettings()


# 导出便捷变量
vllm_config = get_vllm_settings()
settings = get_settings()


if __name__ == "__main__":
    print("=== VLLM 配置信息 ===")
    print(f"API Key: {vllm_config.vllm_api_key[:10]}...{vllm_config.vllm_api_key[-4:]}")
    print(f"Base URL: {vllm_config.api_base}")
    print(f"Model: {vllm_config.vllm_model_name}")
    print(f"Chat URL: {vllm_config.chat_completion_url}")
    print(f"Temperature: {vllm_config.vllm_temperature}")
    print(f"Max Tokens: {vllm_config.vllm_max_tokens}")
