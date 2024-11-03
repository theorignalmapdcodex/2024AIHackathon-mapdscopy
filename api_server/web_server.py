from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

from add_new_video import main as add_new_video
from app import main as get_response
from app_v2 import main as get_response_v2


app = FastAPI(docs_url="/")

# setup the directory to store uploaded videos
UPLOAD_DIR = "uploaded_videos"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # write the file to local directory
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"File saved at: {file_path}")

    # upload the video to Google Cloud Storage
    raw_result = add_new_video(file_path)

    # convert the video uri to the url so that can be accessed from outside
    parts = raw_result.data_uri.split("/")
    bucket_name = parts[2]
    video_name = parts[-1]
    video_url = f"https://storage.googleapis.com/{bucket_name}/{video_name}"

    return {"message": "File uploaded successfully", "file_name": video_url}


@app.get("/query")
async def perform_query(query_param: str):
    raw_result = get_response(query_param)

    result = {
        "response": raw_result[0],
        "video_info": raw_result[1],
    }

    return JSONResponse(content=result)

@app.get("/query_v2")
async def perform_query_v2(query_param: str):
    raw_result = get_response_v2(query_param)

    result = {
        "response": raw_result[0],
        "video_info": raw_result[1],
    }

    return JSONResponse(content=result)


# start the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=10990)
