from fastapi import FastAPI, Response

app = FastAPI()  # uvicorn create_api_tiktok:app --reload

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/download")
def csv():
    file_path = "user.txt"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            csv_content = f.read()
    except FileNotFoundError:
        return Response(content="File not found", media_type="text/plain", status_code=404)
    
    return Response(content=csv_content, media_type="text/plain")