import uvicorn

from fastapi import FastAPI, Depends, File, UploadFile, Path, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.cors import CORSMiddleware

from supertokens_python import init, get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

import boto3
from io import BytesIO

import logging
import os
import config

init(
    supertokens_config=config.supertokens_config,
    app_info=config.app_info,
    framework=config.framework,
    recipe_list=config.recipe_list,
    mode="asgi", # use wsgi if you are running using gunicorn
)

app = FastAPI(title="panda.ai")
app.add_middleware(get_middleware())

S3_BUCKET = "panda.ai"
s3 = boto3.client('s3', aws_access_key_id = 'AKIA4M7OWVUMBL3LUZ5D', aws_secret_access_key = '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')

@app.get("/sessioninfo")    
async def secure_api(s: SessionContainer = Depends(verify_session())):
    return {
        "sessionHandle": s.get_handle(),
        "userId": s.get_user_id(),
        "accessTokenPayload": s.get_access_token_payload(),
    }

@app.post("/uploadimage/")
async def upload_file(userid: str, file: UploadFile = File(...)):
    try:
        # Read the file content
        content = await file.read()

        folder = f'{userid}/avatar/avatar'
        file_name, file_extension = os.path.splitext(file.filename)

        # Upload the file to S3
        s3.upload_fileobj(
            Fileobj=BytesIO(content),  # Convert the content to a file-like object
            Bucket=S3_BUCKET,
            Key=folder + file_extension,
        )

        # Return the public URL of the uploaded file
        response = {
            "message": "Image uploaded successfully",
            "url": f"https://{S3_BUCKET}.s3.amazonaws.com/{folder}{file_extension}",
        }
        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        response = {"error": str(e)}
        return JSONResponse(content=response, status_code=400)
    
@app.get("/getimage/")
async def download_file(userid):
    try:
        prefix = f'{userid}/avatar/avatar'

        # Search for files with the specified prefix in the S3 bucket
        s3_response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)

        if "Contents" not in s3_response or not s3_response["Contents"]:
            raise HTTPException(status_code=404, detail="File not found")

        # Extract file names from the S3 response
        file_name = [obj["Key"] for obj in s3_response["Contents"]]

        # Convert file_name to string
        key = "".join(file_name)

        # Get the file from S3
        s3_file = s3.get_object(Bucket=S3_BUCKET, Key=key)

        # Create a StreamingResponse to send the file content to the client
        response = StreamingResponse(
            s3_file["Body"], headers={"Content-Type": s3_file["ContentType"]}
        )

        return response

    except Exception as e:
        return {"error": str(e)}

@app.get("/test")
async def root():
    return {"message": "Hello World"}

app = CORSMiddleware(
    app=app,
    allow_origins=[config.app_info.website_domain],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

if __name__  == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
