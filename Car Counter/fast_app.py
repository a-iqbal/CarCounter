from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from CarCount import process_video

app = FastAPI()

# Define the directory to save uploaded videos
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Endpoint for uploading video and counting vehicles
@app.post("/count_vehicles/")
async def count_vehicles(file: UploadFile = File(...)):
    try:
        # Create a safe file path using the original file name
        video_filename = file.filename
        video_path = os.path.join(UPLOAD_DIR, video_filename)

        # Save the uploaded video file
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call the vehicle counting function and get the result
        count = process_video(video_path)

        # Remove the video after processing to save space
        os.remove(video_path)

        # Return the vehicle count
        return JSONResponse({"vehicle_count": count})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

# Run FastAPI with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002, reload=True)


