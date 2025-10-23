import boto3
import os
from django.utils import timezone
from dotenv import load_dotenv
load_dotenv()


session = boto3.session.Session()
r2 = session.client(
    service_name='s3',
    endpoint_url=os.getenv('CLOUDFLARE_R2_BUCKET_ENDPOINT'),
    aws_access_key_id=os.getenv('CLOUDFLARE_R2_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('CLOUDFLARE_R2_SECRET_KEY'),
)

def upload_to_r2(file_obj, filename=None, content_type=None):
    bucket = os.getenv('CLOUDFLARE_R2_BUCKET')
    if not filename:
        filename = f"{timezone.now().timestamp()}_{file_obj.name}"

    r2.put_object(
        Bucket=bucket,
        Key=filename,
        Body=file_obj.read(),
        ContentType=content_type or 'application/octet-stream'
    )

    public_url = f"https://pub-7a30aad3d5204f56979be7ab91970aaf.r2.dev/{filename}"
    return public_url


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    test_path = os.path.join(BASE_DIR, "tests/testfile.txt")

    if not os.path.exists(test_path):
        print(f"⚠️ No existe el archivo: {os.path.abspath(test_path)}")
    else:
        with open(test_path, "rb") as f:
            url = upload_to_r2(f, filename="testfile.txt", content_type="text/plain")
            print("✅ Subida exitosa:", url)