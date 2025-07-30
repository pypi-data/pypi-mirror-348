from mcp.server.fastmcp import FastMCP
from openai import OpenAI
import os
from typing import List

mcp = FastMCP('essay_qwen_mcp_server_lc')

openai_message = [
    {
        "role": "system",
        "content": [{"type": "text", "text": "你是一个擅长解读媒体文件的助手，会帮我解读里面的内容并且完整的列出来，最后对列出来的内容进行分析和总结，内容需要追求真实性。"}]
    },
    {
        "role": "user",
        "content": []
    }
]

qwen_api_key = os.getenv("QWEN_API_KEY", "")


def send_qwen_media_message(data, type, apikey):
    if data is not None and len(data) > 0:
        if type == 'image':
            for item in data:
                openai_message[1]["content"].append({"type": "image_url", "image_url": {"url": item}})
        elif type == 'video':
            openai_message[1]["content"].append({"type": "video_url", "video_url": {"url": data}})
        openai_message[1]["content"].append({"type": "text", "text": "给我一个内容分析方向"})
    else:
        return False
    client = OpenAI(
        api_key=apikey,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",
        # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/model-studio/getting-started/models
        messages=openai_message
    )
    return completion.choices[0].message.content


@mcp.tool(name='解读图片', description='通过可访问的URL链接解读图片图片')
async def image_interpretation(images: List[str]):
    if not qwen_api_key or len(qwen_api_key) < 10:
        raise ValueError("请配置QWEN_API_KEY")
    if len(images) == 0:
        raise ValueError("图片链接为空")
    result = send_qwen_media_message(images, "image", qwen_api_key)
    return result


@mcp.tool(name='解读视频', description='通过可访问的URL链接解读视频内容')
async def video_interpretation(src: str):
    if not qwen_api_key or len(qwen_api_key) < 10:
        raise ValueError("请配置QWEN_API_KEY")
    if len(src) == 0:
        raise ValueError("视频链接为空")
    result = send_qwen_media_message(src, "video", qwen_api_key)
    return result



def run():
    mcp.run()


if __name__ == '__main__':
    run()
