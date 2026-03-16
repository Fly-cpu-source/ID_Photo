# VISAGE — 智能证件照 & AI 换发型

基于 HivisionIDPhotos 核心能力的 AI 形象处理产品，支持专业证件照生成与 AI 换发型两大功能。证件照生成由 **AWS EC2 云端**推理处理，AI 换发型由 GPT-Image 驱动。

---

## 功能

- **证件照生成**：AI 精准人像抠图，支持 14 种规格，自定义背景色，4 款抠图模型可选
- **AI 换发型**：6 款发型风格（单马尾、波浪头、爆炸头、大背头、短发、中分），由 GPT-Image 驱动，Before/After 对比展示
- 后端部署于 **AWS EC2**，云端推理，前端直接调用公网 HTTPS 接口

---

## 项目结构

```
ID_Photo/
├── code/
│   ├── Backend/        # FastAPI 后端（证件照 API）
│   └── Frontend/       # 前端页面（单文件 HTML）
└── backup/             # 参考文档
```

---

## 快速开始

### 1. Clone 仓库

```bash
git clone https://github.com/Fly-cpu-source/ID_Photo.git
cd ID_Photo
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r code/Backend/requirements.txt
```

依赖包含：fastapi、uvicorn、opencv-python、onnxruntime、mtcnn-runtime、gradio 等。

### 4. 下载模型权重

模型文件较大，不在仓库中，需要手动下载后放到对应目录。

**目录：`code/Backend/hivision/creator/weights/`**

| 文件名 | 说明 |
|--------|------|
| `hivision_modnet.onnx` | 轻量抠图模型 |
| `modnet_photographic_portrait_matting.onnx` | 高质量抠图模型（推荐） |
| `birefnet-v1-lite.onnx` | BiRefNet 抠图模型 |
| `rmbg-1.4.onnx` | RMBG 抠图模型 |

**目录：`code/Backend/hivision/creator/retinaface/weights/`**

| 文件名 | 说明 |
|--------|------|
| `retinaface-resnet50.onnx` | 人脸检测模型 |

> 模型来源：[HivisionIDPhotos 官方仓库](https://github.com/Zeyi-Lin/HivisionIDPhotos)，在其 Release 页面下载。

### 5. 启动后端（AWS EC2）

后端已部署于 AWS EC2，由 nginx 反向代理对外提供 HTTPS 服务。本地开发如需自行启动：

```bash
cd code/Backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

云端 API 文档：`https://3.137.203.149/docs`

### 6. 打开前端

直接用浏览器打开 `code/Frontend/index.html` 即可，前端默认连接 AWS EC2 云端 API。

> **注意**：AI 换发型功能需在 **Poe 平台**内嵌页面中使用（依赖 Poe Embed API + GPT-Image-1.5）。

---

## API 说明

### POST `/api/generate`

生成证件照。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `image` | file | - | 上传的人像照片 |
| `bg_color` | string | `#FFFFFF` | 背景颜色（Hex） |
| `height` | int | `413` | 证件照高度（像素） |
| `width` | int | `295` | 证件照宽度（像素） |
| `matting_model` | string | `modnet_photographic_portrait_matting` | 使用的抠图模型（见下表） |

**可用抠图模型：**

| 值 | 说明 |
|----|------|
| `modnet_photographic_portrait_matting` | MODNet 摄影版（默认推荐） |
| `hivision_modnet` | HivisionModNet，证件照优化 |
| `birefnet-v1-lite` | BiRefNet Lite，边缘精细 |
| `rmbg-1.4` | RMBG 1.4，背景去除专项 |

返回 JSON：`{ "image": "<base64>" }`

---

## 常见问题

**Q: 提示「未检测到人脸」**
A: 请上传包含清晰正面人脸的照片，避免侧脸、遮挡或模糊。

**Q: 模型加载报错**
A: 检查模型文件是否放在正确目录，文件名是否完全一致。

**Q: pip 安装失败**
A: 确保 Python 版本 >= 3.9，建议使用虚拟环境。

**Q: AI 换发型功能无法使用**
A: 此功能依赖 Poe Embed API，需在 Poe 平台嵌入页面中使用，直接打开 HTML 文件无法调用。

**Q: 前端连不上后端**
A: 前端默认连接 AWS EC2 云端 `https://3.137.203.149`，确认 EC2 实例正在运行且安全组已开放 443 端口。首次访问浏览器可能提示证书警告，手动信任自签名证书后即可正常使用。
