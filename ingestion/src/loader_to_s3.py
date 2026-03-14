
import os
import boto3
# NOTE: Ensure these imports match your actual directory structure
from ingestion.src.config import S3_BUCKET, S3_PREFIX, S3_PATH, HASH_FILE, s3_client

def upload_chroma_to_s3(bucket: str):
  # Using the client passed from config is fine
  for root, _, files in os.walk(S3_PATH):
    for file in files:
      if file == os.path.basename(HASH_FILE):
                continue
      local_file = os.path.join(root, file)
      # Create a clean S3 key
      s3_key = S3_PREFIX + os.path.relpath(local_file, S3_PATH)
      # Replace backslashes for Windows compatibility
      s3_key = s3_key.replace("\\", "/")

      s3_client.upload_file(local_file, bucket, s3_key)
      print(f"Uploading {local_file} → s3://{bucket}/{s3_key}")

def upload_hash_file_to_s3():
    """Uploads the local hash file to the chroma_db prefix in S3."""                
    # Use the filename from the config path (e.g., .processed_hashes.json)
    file_name = os.path.basename(HASH_FILE)
    
    # Construct the S3 key using the prefix from config (e.g., "chroma_db/")
    s3_key = f"{S3_PREFIX}{file_name}" 
    
    try:
        # HASH_FILE points to data/chroma_db/.processed_hashes.json
        print(f"Uploading local {HASH_FILE} to s3://{S3_BUCKET}/{s3_key}...")
        s3_client.upload_file(HASH_FILE, S3_BUCKET, s3_key)
        print("Hash file upload successful.")
    except Exception as e:
        print(f"Error uploading hash file: {e}")