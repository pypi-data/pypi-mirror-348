import boto3
import os
import logging
 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
def persist_model(message_type, experiment_name, file_path):
    bucket_name = 'neuroedge-device'
    device_type = 'Default'
    s3 = boto3.client('s3')
 
    if message_type == 1:
        if os.path.exists(file_path):
            try:
                device_type = 'DEF'
                s3_key = f'{device_type}_{experiment_name}_{os.path.basename(file_path)}'
                s3.upload_file(file_path, bucket_name, s3_key)
                logging.info(f"File '{file_path}' successfully uploaded to 's3://{bucket_name}/{s3_key}'")
            except Exception as e:
                logging.error(f"Error uploading file to S3: {e}")
        else:
            logging.warning(f"File '{file_path}' does not exist.")
            
    else if message_type == 2:
        if os.path.exists(file_path):
            try:
                device_type = 'QNN'
                s3_key = f'{device_type}_{experiment_name}_{os.path.basename(file_path)}'
                s3.upload_file(file_path, bucket_name, s3_key)
                logging.info(f"File '{file_path}' successfully uploaded to 's3://{bucket_name}/{s3_key}'")
            except Exception as e:
                logging.error(f"Error uploading file to S3: {e}")
        else:
            logging.warning(f"File '{file_path}' does not exist.")
