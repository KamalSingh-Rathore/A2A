
from fastapi import FastAPI

app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/documentation")
def write_documentation():
    return {"message": "This is the documentation endpoint. You can add more details here."}