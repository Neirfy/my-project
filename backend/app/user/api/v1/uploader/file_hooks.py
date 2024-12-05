import os
from fastapi import APIRouter, File, HTTPException, UploadFile
from common.security.jwt import DependsJwtAuth
from core.path_conf import STORE_DIR

router = APIRouter(prefix="/upload", tags=["Загрузка файлов с 1С"])


@router.post("/archive", dependencies=[DependsJwtAuth])
async def upload_archive(file: UploadFile):
    filename = file.filename
    ext = os.path.splitext(filename)[-1].lower()
    if ext != ".zip":
        raise HTTPException(
            status_code=422, detail="Неверное расширение файла. Ожидался XML."
        )

    with open(f"{STORE_DIR}/{filename}", "wb") as f:
        f.write(await file.read())

    return {"filename": filename, "status": "Файл загружен успешно."}


@router.post("/xml", dependencies=[DependsJwtAuth])
async def upload_xml(file: UploadFile):
    filename = file.filename
    ext = os.path.splitext(filename)[-1].lower()
    if ext != ".xml":
        raise HTTPException(
            status_code=422, detail="Неверное расширение файла. Ожидался XML."
        )

    with open(f"{STORE_DIR}/{filename}", "wb") as f:
        f.write(await file.read())

    return {"filename": filename, "status": "Файл загружен успешно."}


@router.post("/images", dependencies=[DependsJwtAuth])
async def upload_images(file: UploadFile):
    filename = file.filename
    ext = os.path.splitext(filename)[-1].lower()
    if ext != ".zip":
        raise HTTPException(
            status_code=422, detail="Неверное расширение файла. Ожидался ZIP."
        )

    with open(f"{STORE_DIR}/{filename}", "wb") as f:
        f.write(await file.read())

    return {"filename": filename, "status": "Файл загружен успешно."}
