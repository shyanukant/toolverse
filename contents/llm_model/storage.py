from google.cloud import storage
from django.conf import settings
import random
import string

bucket_name = settings.GCP_BUCKET_NAME
destination_blob_name = settings.GCP_BUCKET_DESTINATION

def image_name(prefix="toolverse", length=8):
    random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    name = f"{prefix}_{random_name}.png"
    return name


def image_storage_url(img_url):
    # Initialize client (assumes GOOGLE_APPLICATION_CREDENTIALS is set)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    destination = f"{destination_blob_name}/{image_name()}"
    blob = bucket.blob(destination)

    # Upload the bytes directly
    blob.upload_from_string(img_url, content_type="image/png")
    blob.upload_from_string(img_url)

    return f"https://storage.googleapis.com/{bucket_name}/{destination}"