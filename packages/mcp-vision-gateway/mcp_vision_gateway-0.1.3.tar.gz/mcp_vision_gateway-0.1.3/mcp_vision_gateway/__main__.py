"""视觉AI网关MCP服务主入口"""

import sys
import os
import json
import base64
import traceback
import requests
import uuid
from typing import Optional, Dict, Any, List, Union

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("错误：需要安装 'mcp' 包才能运行此服务器。", file=sys.stderr)
    print("请运行: pip install mcp", file=sys.stderr)
    sys.exit(1)

# --- 配置管理 ---
def get_config():
    """从环境变量获取配置"""
    config = {
        # 默认中转站地址
        "api_base": os.environ.get("VISION_API_BASE", "https://api.ssopen.top"),
        # 默认API密钥
        "api_key": os.environ.get("VISION_API_KEY", ""),
        # 默认模型
        "default_model": os.environ.get("VISION_DEFAULT_MODEL", "gpt-4o"),
        # 调试模式
        "debug": os.environ.get("VISION_DEBUG", "false").lower() == "true"
    }
    return config

def debug_log(message: str):
    """输出调试日志"""
    config = get_config()
    if config["debug"]:
        print(f"[DEBUG] {message}", file=sys.stderr)

# --- 创建FastMCP服务器实例 ---
mcp = FastMCP("视觉AI网关")  # 服务器名称

# 图像存储 - 用于存储base64图像数据，避免直接传递大量文本
image_storage = {}

# --- API请求处理 ---
def make_vision_api_request(
    messages: List[Dict[str, Any]], 
    model: str, 
    api_base: str, 
    api_key: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stream: bool = False
) -> Dict[str, Any]:
    """向视觉API发送请求"""
    debug_log(f"使用模型 {model} 发送请求")
    
    # 构建请求体
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": stream
    }
    
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens

    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json", 
        "Authorization": f"Bearer {api_key}"
    }
    
    # 发送请求
    debug_log(f"向 {api_base}/v1/chat/completions 发送请求")
    try:
        response = requests.post(
            f"{api_base}/v1/chat/completions", 
            json=payload, 
            headers=headers
        )
        response.raise_for_status()
        result = response.json()
        debug_log("请求成功")
        return result
    except Exception as e:
        error_msg = f"API请求失败: {str(e)}"
        debug_log(error_msg)
        raise Exception(error_msg)

def encode_image_to_base64(image_data: bytes) -> str:
    """将图像数据编码为base64"""
    return base64.b64encode(image_data).decode('utf-8')

# --- MCP工具定义 ---
@mcp.tool()
def upload_image_from_url(url: str) -> str:
    """从URL下载图像并转换为base64以便后续使用
    
    参数:
        url: 图像的URL
    
    返回:
        图像引用ID，可在vision_query的image_ref参数中使用
    """
    debug_log(f"从URL下载图像: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # 获取图像数据并转换为base64
        image_data = response.content
        base64_image = encode_image_to_base64(image_data)
        
        # 生成唯一ID并存储图像
        image_id = f"img_{uuid.uuid4().hex[:8]}"
        image_storage[image_id] = base64_image
        
        debug_log(f"图像下载并转换为base64成功，存储ID: {image_id}")
        return image_id
    except Exception as e:
        error_msg = f"下载图像失败: {str(e)}"
        debug_log(error_msg)
        return f"错误: {error_msg}"

@mcp.tool()
def upload_local_image(file_path: str) -> str:
    """从本地文件系统读取图像并转换为base64编码
    
    参数:
        file_path: 图像文件的本地路径
    
    返回:
        图像引用ID，可在vision_query的image_ref参数中使用
    """
    debug_log(f"读取本地图像: {file_path}")
    
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"错误: 文件不存在: {file_path}"
            
        # 读取图像文件
        with open(file_path, 'rb') as image_file:
            image_data = image_file.read()
            base64_image = encode_image_to_base64(image_data)
        
        # 生成唯一ID并存储图像
        image_id = f"img_{uuid.uuid4().hex[:8]}"
        image_storage[image_id] = base64_image
        
        debug_log(f"本地图像转换为base64成功，存储ID: {image_id}")
        return image_id
    except Exception as e:
        error_msg = f"读取本地图像失败: {str(e)}"
        debug_log(error_msg)
        return f"错误: {error_msg}"

@mcp.tool()
def vision_query(
    prompt: str,
    image_url: Optional[str] = None,
    image_base64: Optional[str] = None,
    image_ref: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """向AI模型发送查询，支持纯文本对话和图像分析
    
    参数:
        prompt: 文本提示
        image_url: 图像URL (可选)
        image_base64: base64编码的图像 (可选)
        image_ref: 图像引用ID (通过upload_image_xxx函数获取，优先级高于其他图像参数)
        model: 使用的模型名称 (默认使用环境变量)
        temperature: 采样温度，范围0-2
        max_tokens: 生成的最大token数
        api_base: API基础URL (默认使用环境变量)
        api_key: API密钥 (默认使用环境变量)
    """
    config = get_config()
    
    # 使用参数或环境变量的配置
    actual_api_base = api_base or config["api_base"]
    actual_api_key = api_key or config["api_key"]
    actual_model = model or config["default_model"]
    
    if not actual_api_key:
        return "错误: 未提供API密钥。请设置VISION_API_KEY环境变量或提供api_key参数。"
    
    # 检查图像参数，最多只能提供一种
    provided_image_params = sum(1 for p in [image_url, image_base64, image_ref] if p)
    if provided_image_params > 1:
        return "错误: image_url、image_base64和image_ref参数不能同时提供，请只选择一种方式。"
    
    # 优先使用图像引用
    if image_ref:
        if image_ref in image_storage:
            debug_log(f"使用引用的图像: {image_ref}")
            image_base64 = image_storage[image_ref]
        else:
            return f"错误: 图像引用'{image_ref}'不存在，请先上传图像。"
    
    # 构建消息
    if image_url or image_base64:
        # 如果提供了图像，使用多模态格式
        content = [{"type": "text", "text": prompt}]
        
        if image_url:
            debug_log(f"使用图像URL: {image_url}")
            content.append({
                "type": "image_url",
                "image_url": {"url": image_url}
            })
        elif image_base64:
            debug_log("使用base64编码图像")
            # 确保base64正确格式化
            if not image_base64.startswith("data:"):
                image_base64 = f"data:image/jpeg;base64,{image_base64}"
            
            content.append({
                "type": "image_url",
                "image_url": {"url": image_base64}
            })
    else:
        # 纯文本对话
        debug_log("使用纯文本对话模式")
        content = prompt
    
    messages = [{"role": "user", "content": content}]
    
    # 发送请求
    try:
        response = make_vision_api_request(
            messages=messages,
            model=actual_model,
            api_base=actual_api_base,
            api_key=actual_api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # 解析响应
        if "choices" in response and len(response["choices"]) > 0:
            answer = response["choices"][0]["message"]["content"]
            return answer
        else:
            return f"错误: 无效的API响应: {json.dumps(response)}"
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return f"错误: {str(e)}"

@mcp.tool()
def list_available_models(
    api_base: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """列出可用的AI模型
    
    参数:
        api_base: API基础URL (默认使用环境变量)
        api_key: API密钥 (默认使用环境变量)
    """
    config = get_config()
    
    # 使用参数或环境变量的配置
    actual_api_base = api_base or config["api_base"]
    actual_api_key = api_key or config["api_key"]
    
    if not actual_api_key:
        return "错误: 未提供API密钥。请设置VISION_API_KEY环境变量或提供api_key参数。"
    
    # 构建请求头
    headers = {
        "Authorization": f"Bearer {actual_api_key}"
    }
    
    # 发送请求
    try:
        response = requests.get(f"{actual_api_base}/v1/models", headers=headers)
        response.raise_for_status()
        
        models_data = response.json()
        if "data" in models_data:
            # 提取模型信息
            models = []
            for model in models_data["data"]:
                models.append({
                    "id": model["id"],
                    "created": model.get("created"),
                    "owned_by": model.get("owned_by", "unknown")
                })
            
            return json.dumps(models, ensure_ascii=False, indent=2)
        else:
            return f"无法获取模型列表: {json.dumps(models_data)}"
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return f"错误: {str(e)}"

# --- 服务器启动入口 ---
def main():
    """MCP服务器入口函数，供命令行或uvx调用"""
    try:
        config = get_config()
        print(f"视觉AI网关MCP服务正在启动...", file=sys.stderr)
        print(f"API地址: {config['api_base']}", file=sys.stderr)
        print(f"默认模型: {config['default_model']}", file=sys.stderr)
        print(f"调试模式: {config['debug']}", file=sys.stderr)
        
        if not config["api_key"]:
            print("警告: 未设置API密钥环境变量(VISION_API_KEY)", file=sys.stderr)
        
        print("MCP服务器实例已创建，准备运行...", file=sys.stderr)
        mcp.run()  # 启动服务器
        print("视觉AI网关MCP服务已停止。", file=sys.stderr)
    except Exception as e:
        print(f"启动或运行时发生严重错误: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

# 允许直接通过 python -m mcp_vision_gateway 运行
if __name__ == "__main__":
    main() 