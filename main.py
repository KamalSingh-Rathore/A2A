from typing import Optional

from fastapi import FastAPI, UploadFile, File
from zip_extractor import zip_extractor
app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/documentation")
def write_documentation():
    return {"message": "This is the documentation endpoint. You can add more details here."}


@app.post("/upload")
def upload_file(file: Optional[UploadFile] = None , repo_url: str = None):
    # Here you can handle the file upload logic
    zip_extractor(repo_url=file.file)
    return {"filename": file.filename}