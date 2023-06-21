
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Flipkart import return_details,return_all

app = FastAPI()

origins = ["*"]  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/")
async def read_item(request_data: dict):
    url = request_data.get('url')
    code = request_data.get('code')
    number = request_data.get('number')
    # print(url)
    # print(code,number)
    # return return_all(url)
    if(code==True):
        return return_details(url,True)
    else:
        return return_details(url,False,number)

