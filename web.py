from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from PIL import Image
from io import BytesIO

import json
import shutil
import base64
import requests
import numpy as np

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

url = "http://0.0.0.0:5000/idc_vn/recognition"


def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))


def sort_result(result):
    sorted_result = {}
    id = result["id"] + " -- confidence: " + str(result["id_conf"])
    sorted_result["ID"] = id

    name = result["name"] + " -- confidence: " + str(result["name_conf"])
    sorted_result["Name"] = name

    birthday = result["birthday"] + " -- confidence: " + str(result["birthday_conf"])
    sorted_result["Birthday"] = birthday

    address = result["address"] + " -- confidence: " + str(result["address_conf"])
    sorted_result["Address"] = address

    hometown = result["hometown"] + " -- confidence: " + str(result["hometown_conf"])
    sorted_result["Hometown"] = hometown

    document = result["document"]

    if document == "CCCD":

        national = (
            result["national"] + " -- confidence: " + str(result["national_conf"])
        )
        sorted_result["National"] = national

        ethnicity = (
            result["ethnicity"] + " -- confidence: " + str(result["ethnicity_conf"])
        )
        sorted_result["Ethnicity"] = ethnicity

        sorted_result["Document"] = result["document"]
    elif document == "CMND":
        sorted_result["Document"] = result["document"]
    return sorted_result


# get index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# get result page
@app.post("/result", response_class=HTMLResponse)
async def upload_image(request: Request, image: UploadFile = File(...)):
    with open("./static/images/destination.jpg", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    with open("./static/images/destination.jpg", "rb") as img_file:
        data = base64.b64encode(img_file.read()).decode("utf-8")

    send_data = {"image": data}
    response = requests.post(url, json=send_data)
    result = response.json()
    if "detail" not in result.keys():
        result = sort_result(result)

    return templates.TemplateResponse(
        "result.html", {"request": request, "result": result}
    )


# get test_image_1 page
@app.get("/test_image_1", response_class=HTMLResponse)
async def test_image_1(request: Request):
    shutil.copy(
        "./static/images/test_image/ocr-1.jpg", "./static/images/destination.jpg"
    )

    with open("./static/images/test_image/ocr-1.jpg", "rb") as img_file:
        data = base64.b64encode(img_file.read()).decode("utf-8")

    send_data = {"image": data}
    response = requests.post(url, json=send_data)
    result = response.json()
    if "detail" not in result.keys():
        result = sort_result(result)

    return templates.TemplateResponse(
        "result.html", {"request": request, "result": result}
    )


# get test_image_2 page
@app.get("/test_image_2", response_class=HTMLResponse)
async def test_image_2(request: Request):
    shutil.copy(
        "./static/images/test_image/ocr-2.jpg", "./static/images/destination.jpg"
    )

    with open("./static/images/test_image/ocr-2.jpg", "rb") as img_file:
        data = base64.b64encode(img_file.read()).decode("utf-8")

    send_data = {"image": data}
    response = requests.post(url, json=send_data)
    result = response.json()
    if "detail" not in result.keys():
        result = sort_result(result)

    return templates.TemplateResponse(
        "result.html", {"request": request, "result": result}
    )


# get test_image_3 page
@app.get("/test_image_3", response_class=HTMLResponse)
async def test_image_3(request: Request):
    shutil.copy(
        "./static/images/test_image/ocr-3.jpg", "./static/images/destination.jpg"
    )

    with open("./static/images/test_image/ocr-3.jpg", "rb") as img_file:
        data = base64.b64encode(img_file.read()).decode("utf-8")

    send_data = {"image": data}
    response = requests.post(url, json=send_data)
    result = response.json()
    if "detail" not in result.keys():
        result = sort_result(result)

    return templates.TemplateResponse(
        "result.html", {"request": request, "result": result}
    )
