from dotenv import load_dotenv
from fastapi import File
from imagekitio import ImageKit
import os
import shutil
import tempfile

load_dotenv()

private_key=None
public_key=None
url_endpoint=None

try:
    private_key = os.getenv("IMAGEKIT_PRIVATE_KEY")
    public_key = os.getenv("IMAGEKIT_PUBLIC_KEY")
    url_endpoint = os.getenv("IMAGEKIT_URL")
except Exception as e:
    print("Error loading environment variables:", e)

imagekit = ImageKit(
    private_key=private_key
)

class ImageKitHandler():
    '''Class to handle image uploads to ImageKit'''

    def upload_image(self, file : File) -> dict:
        '''Uploads an image to ImageKit and returns the upload result.
        Args:
            file (UploadFile): The file to be uploaded.
        Returns:
            dict: A dictionary containing the upload result.
        '''
        
        temp_file_path = None

        try: 
            with tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=os.path.splitext(file.filename)[1]
            ) as temp_file:
                temp_file_path = temp_file.name
                shutil.copyfileobj(file.file, temp_file)
            
            upload_result = imagekit.files.upload(
                file=open(temp_file_path, "rb"),
                file_name=file.filename,
                tags=["product", "featured"]
            )
            
            if upload_result:
                return {
                    "response": {
                        "name": file.filename,
                        'fileType': upload_result.file_type,
                        "url": upload_result.url
                    }
                }
                
        except Exception as e:
            print(f"Error uploading image: {e}")
            raise
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            file.file.close()