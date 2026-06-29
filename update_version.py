import json
import os
import urllib.request

# API 地址
API_URL = "https://v1.valorant-api.com/v1/version/ap"
TARGET_FILE = "data.json"


def fetch_and_update():
    # 从系统环境变量中读取 GitHub Secrets 传入的 Key
    api_key = os.getenv("HENRIK_API_KEY")

    if not api_key:
        print("错误：未检测到环境变量 HENRIK_API_KEY！")
        return

    try:
        # 在 Headers 中加入 Authorization 和 User-Agent
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Authorization": api_key,  # 传入你的 API Key
        }

        req = urllib.request.Request(API_URL, headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                raw_data = json.loads(response.read().decode())

                # 提取内层 data 字典
                inner_data = raw_data.get("data", {})

                # 仅保留你需要的两个字段
                filtered_data = {
                    "version": inner_data.get("version"),
                    "clientVersion": inner_data.get("clientVersion"),
                }

                with open(TARGET_FILE, "w", encoding="utf-8") as f:
                    json.dump(filtered_data, f, ensure_ascii=False, indent=4)
                print("已成功携带 Key 请求并更新精简数据！")
            else:
                print(f"请求失败，状态码: {response.status}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    fetch_and_update()
