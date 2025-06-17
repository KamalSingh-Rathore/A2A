from typing import Optional

from fastapi import FastAPI, UploadFile, File
from zip_extractor import zip_extractor
from loadinggit import download_github_repo_as_zip

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
    if file and not repo_url:
        zip_extractor(repo_url=file.file)
    elif repo_url and not file:
        download_github_repo_as_zip(repo_url=repo_url)
    else:
        return {"error": "Please provide either a file or a repository URL, but not both."}

    return {"filename": file.filename}