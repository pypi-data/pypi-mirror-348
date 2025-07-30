from pydantic_settings  import BaseSettings

class SecurityConfig(BaseSettings):
    allowed_domains: list = ["api.example.com", "www.baidu.com"]
    max_redirects: int = 3
    follow_redirects:  bool = True
    rate_limit: int = 100  # 每秒最大请求数
    api_keys: dict = {
        "internal": "sk-xxxxxx",
        "external": "ey-xxxxxx"
    }

security_config = SecurityConfig()