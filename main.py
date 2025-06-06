
from fastapi import FastAPI

from test.test import multiplying_number
from test.test2.test2 import subtracting_number
from test.test2.test3.test3 import adding_number
from test.test21.test21 import dividing_number

app = FastAPI()



@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.get("/add/{a}/{b}")
def adding(a, b):
    return adding_number(a,b)


@app.get("/subtract/{a}/{b}")
def subtracting(a, b):
    if a < b:
        return subtracting_number(b,a)
    else:
        return subtracting_number(a,b)



@app.get("/multiply/{a}/{b}")
def multiplying(a, b):
    return multiplying_number(a,b)


@app.get("/divide/{a}/{b}")
def dividing(a, b):
    return dividing_number(a,b)