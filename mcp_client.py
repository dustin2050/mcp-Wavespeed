import asyncio
import os
import argparse
import logging
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.types import Tool, TextContent, ImageContent
from mcp import StdioServerParameters

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("wavespeed-client")

async def run_client(server_type, tool_name, params):
    # 设置 API 密钥
    api_key = os.getenv("WAVESPEED_API_KEY")
    if not api_key:
        raise ValueError("请设置 WAVESPEED_API_KEY 环境变量")
    logger.info(f"启动 {server_type} 客户端，准备调用工具: {tool_name}")
    
    # 固定使用wavespeed模块
    module_path = "wavespeed"
    
    logger.info(f"使用模块路径: {module_path}")
    
    server_params = StdioServerParameters(
        command="mcp-wavespeed",
        args=["--api-key", api_key]
    )
    #server_params = StdioServerParameters(
    #    command="python",
    #    args=["-m", "wavespeed", "--api-key", api_key]
    #)
    logger.info("正在连接到服务器...")
    
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            logger.info("已连接到服务器")
            
            # 创建 MCP 客户端会话并使用 async with 确保初始化完成
            logger.info("正在初始化客户端连接...")
            async with ClientSession(read_stream, write_stream) as client:
                logger.info("客户端连接初始化完成")
                await client.initialize()
                # 获取可用工具列表
                logger.info("正在获取可用工具列表...")
                tools_result = await client.list_tools()
                tools = tools_result.tools  # 获取工具列表
                logger.info(f"获取到 {len(tools)} 个可用工具")
                print("可用工具:")
                for tool in tools:
                    print(f"- {tool.name}: {tool.description}")
                
                # 调用指定的工具
                if tool_name not in [tool.name for tool in tools]:
                    raise ValueError(f"工具 '{tool_name}' 不可用")
                
                logger.info(f"正在调用工具 {tool_name}，参数: {params}")
                result = await client.call_tool(tool_name, params)
                logger.info("工具调用完成，正在处理结果")
                
                # 处理结果
                if isinstance(result, tuple):
                    # 如果结果是元组，解包它
                    for item in result:
                        if hasattr(item, 'type'):
                            if item.type == "image":
                                print(f"生成的图像 URL: {item.url}")
                            elif item.type == "text":
                                print(item.text)
                else:
                    # 如果结果是单个对象
                    for content in result:
                        if hasattr(content, 'type'):
                            if content.type == "image":
                                print(f"生成的图像 URL: {content.url}")
                            elif content.type == "text":
                                print(content.text)
    except Exception as e:
        logger.error(f"客户端执行出错: {str(e)}", exc_info=True)
        raise

def main():
    parser = argparse.ArgumentParser(description="MCP 客户端示例")
    parser.add_argument("--server", choices=["wavespeed"], default="wavespeed", help="要使用的服务器类型")
    parser.add_argument("--tool", choices=["generate_image", "generate_video"], default="generate_image", help="要调用的工具名称")
    args = parser.parse_args()
    
    logger.info(f"启动客户端，服务器类型: {args.server}，工具: {args.tool}")
    
    # 根据工具类型设置默认参数
    if args.tool == "generate_image":
        params = {
            "prompt": "一只可爱的猫咪在阳光下玩耍",
            "image": "https://k.sinaimg.cn/n/sinakd20121/285/w496h589/20200617/ad33-iuzasxt3509985.jpg/w700d1q75cms.jpg",
            "loras": [{"path": "linoyts/yarn_art_Flux_LoRA", "scale": 1.0}],
            "size": "1024*1024"
        }
    elif args.tool == "generate_video":
        params = {
            "image_url": "https://k.sinaimg.cn/n/sinakd20121/285/w496h589/20200617/ad33-iuzasxt3509985.jpg/w700d1q75cms.jpg",
            "prompt": "猫咪在玩耍",
            "loras": [{"path": "Remade-AI/Deflate", "scale": 1.0}]
        }
    else:
        params = {}
    
    logger.info(f"使用参数: {params}")
    
    try:
        asyncio.run(run_client(args.server, args.tool, params))
        logger.info("客户端执行完成")
    except Exception as e:
        logger.error(f"客户端执行失败: {str(e)}")
        raise

if __name__ == "__main__":
    main()