from fastapi import FastAPI
import uvicorn

app = FastAPI()


# include the port number in the URL. Can it be accessed within startup_event()?
# http://localhost:8000


@app.on_event("startup")
def startup_event():
    print("Visit http://localhost:8000 or http://127.0.0.1:8000 to access the app.")

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
