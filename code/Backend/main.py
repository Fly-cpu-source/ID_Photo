import os
import io
import base64
import numpy as np
import cv2
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from hivision import IDCreator
from hivision.creator.choose_handler import choose_handler
from hivision.utils import add_background
from hivision.error import FaceError

app = FastAPI(title="证件照生成 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

creator = IDCreator()


def hex_to_bgr(hex_color: str):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (b, g, r)


def numpy_to_base64(img: np.ndarray, fmt: str = "JPEG") -> str:
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    img_uint8 = np.clip(img, 0, 255).astype(np.uint8)
    success, buffer = cv2.imencode(f".{fmt.lower()}", img_uint8)
    if not success:
        raise ValueError("图片编码失败")
    return base64.b64encode(buffer).decode("utf-8")


@app.post("/api/generate")
async def generate(
    image: UploadFile = File(...),
    bg_color: str = Form("#FFFFFF"),
    height: int = Form(413),
    width: int = Form(295),
    matting_model: str = Form("modnet_photographic_portrait_matting"),
):
    # 读取上传图片
    contents = await image.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="图片读取失败，请上传有效的图片文件")

    # 绑定抠图模型
    choose_handler(creator, matting_model, "mtcnn")

    # 执行证件照生成
    try:
        result = creator(img, size=(height, width))
    except FaceError:
        raise HTTPException(status_code=422, detail="未检测到人脸，请上传包含清晰人脸的照片")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败：{str(e)}")

    # 添加背景颜色
    bgr = hex_to_bgr(bg_color)
    output = add_background(result.standard, bgr=bgr, mode="pure_color")

    return {
        "image": numpy_to_base64(output),
    }
