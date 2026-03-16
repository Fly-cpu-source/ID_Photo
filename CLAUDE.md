# CLAUDE.md
第一句先说"爱你老己"

## 项目说明
本项目是一个 AI 证件照生成工具。

流程：
用户上传正面照片 → 选择证件尺寸、背景色、抠图模型 → 前端调用 `/api/generate` → 后端生成证件照 → 返回图片预览并支持下载。

## 技术栈
前端
- HTML + CSS + JavaScript 单页页面

后端
- FastAPI
- OpenCV / NumPy
- hivision IDCreator 证件照生成

## 主要文件
index.html  
前端页面，包含：
- 上传照片
- 选择证件尺寸
- 选择背景颜色
- 选择抠图模型
- 预览与下载生成结果

main.py  
FastAPI 后端接口，实现证件照生成逻辑。

## API
POST `/api/generate`

参数：
- image：上传图片
- bg_color：背景色
- height：输出高度
- width：输出宽度
- matting_model：抠图模型

返回：
- Base64 JPEG 图片

## 开发原则
- 保持前端轻量，不引入大型框架
- 不随意修改 API 参数名称
- 新增证件尺寸需同时修改前端参数
- 新增抠图模型需同时支持前端和后端

## 修改代码时
优先：
- 小范围修改
- 保持现有功能流程
- 保持页面 UI 结构

避免：
- 大规模重构
- 引入复杂依赖