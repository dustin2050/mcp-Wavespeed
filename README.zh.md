# WavespeedMCP

WavespeedMCP 是 WaveSpeed AI 服务的模型控制协议（MCP）服务器实现。它通过 MCP 协议为访问 WaveSpeed 的图像和视频生成功能提供了标准化接口。

## 功能特点

- **高级图像生成**：从文本提示创建高质量图像，支持图像到图像生成、局部重绘和 LoRA 模型
- **动态视频生成**：使用可自定义的动作参数将静态图像转换为视频
- **优化性能**：通过智能重试逻辑和详细的进度跟踪增强 API 轮询
- **灵活的资源处理**：支持 URL、Base64 和本地文件输出模式
- **全面的错误处理**：专门的异常层次结构，用于精确识别和恢复错误
- **强大的日志系统**：用于监控和调试的详细日志系统
- **多种配置选项**：支持环境变量、命令行参数和配置文件

## 安装

### 前提条件

- Python 3.11+
- WaveSpeed API 密钥（从 [WaveSpeed AI](https://wavespeed.ai) 获取）

### 安装步骤

直接从 PyPI 安装：

```bash
pip install wavespeed-mcp
```

### MCP 配置

要将 WavespeedMCP 与您的 IDE 或应用程序一起使用，请添加以下配置：

```json
{
  "mcpServers": {
    "Wavespeed": {
      "command": "wavespeed-mcp",
      "env": {
        "WAVESPEED_API_KEY": "wavespeedkey"
      }
    }
  }
}
```

## 使用方法

### 运行服务器

启动 WavespeedMCP 服务器：

```bash
wavespeed-mcp --api-key your_api_key_here
```

### Claude Desktop 集成

WavespeedMCP 可以与 Claude Desktop 集成。要生成必要的配置文件：

```bash
python -m wavespeed_mcp --api-key your_api_key_here --config-path /path/to/claude/config
```

此命令生成一个 `claude_desktop_config.json` 文件，该文件配置 Claude Desktop 使用 WavespeedMCP 工具。生成配置后：

1. 使用 `wavespeed-mcp` 命令启动 WavespeedMCP 服务器
2. 启动 Claude Desktop，它将使用配置好的 WavespeedMCP 工具

## 配置选项

WavespeedMCP 可以通过以下方式进行配置：

1. **环境变量**：

   - `WAVESPEED_API_KEY`：您的 WaveSpeed API 密钥（必需）
   - `WAVESPEED_API_HOST`：API 主机 URL（默认：https://api.wavespeed.ai）
   - `WAVESPEED_MCP_BASE_PATH`：输出文件的基本路径（默认：~/Desktop）
   - `WAVESPEED_API_RESOURCE_MODE`：资源输出模式（选项：url、base64、local；默认：url）
   - `WAVESPEED_LOG_LEVEL`：日志级别（选项：DEBUG、INFO、WARNING、ERROR；默认：INFO）
   - `WAVESPEED_API_TEXT_TO_IMAGE_ENDPOINT`：文本生成图像的自定义端点（默认：/wavespeed-ai/flux-dev）
   - `WAVESPEED_API_IMAGE_TO_IMAGE_ENDPOINT`：图像编辑的自定义端点（默认：/wavespeed-ai/flux-kontext-pro）
   - `WAVESPEED_API_VIDEO_ENDPOINT`：视频生成的自定义端点（默认：/wavespeed-ai/wan-2.1/i2v-480p-lora）

2. **命令行参数**：

   - `--api-key`：您的 WaveSpeed API 密钥
   - `--api-host`：API 主机 URL
   - `--config`：配置文件的路径

3. **配置文件**（JSON 格式）：
   参见 `wavespeed_mcp_config_demo.json` 示例。

## 架构

WavespeedMCP 遵循清晰、模块化的架构：

- `server.py`：核心 MCP 服务器实现，包含工具定义
- `client.py`：优化的 API 客户端，具有智能轮询功能
- `utils.py`：用于资源处理的综合实用函数
- `exceptions.py`：用于错误处理的专门异常层次结构
- `const.py`：常量和默认配置值

## 开发

### 要求

- Python 3.11+
- 开发依赖：`pip install -e ".[dev]"`

### 测试

运行测试套件：

```bash
pytest
```

或者使用覆盖率报告：

```bash
pytest --cov=wavespeed_mcp
```

## 许可证

本项目根据 MIT 许可证授权 - 有关详细信息，请参阅 LICENSE 文件。

## 支持

如需支持或功能请求，请联系 WaveSpeed AI 团队：support@wavespeed.ai。
