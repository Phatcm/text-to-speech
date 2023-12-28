import json
import boto3
import os
import uuid
import time
from botocore.exceptions import ClientError

polly = boto3.client('polly')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    body = json.loads(event["body"])
    text = body["text"]
    #define bucket connect
    bucket_name = os.environ['BUCKET_NAME']
    
    response = generateAudioUsingText(text, bucket_name)
    file_name = response['SynthesisTask']['TaskId']+".mp3"
    
    file_available = False
    
    while not file_available:
        try:
            s3.head_object(Bucket = bucket_name, Key = file_name)
            url = generatePresignUrl(file_name, bucket_name)
            file_available = True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                time.sleep(1)
            else:
                print("An error occurred:", e)  # Log the error
                # Handle the error without re-raising it
    print(url)
    return {
        'statusCode': 200,
        'body': json.dumps(url)
    }

def generateAudioUsingText(text, bucket_name):
    try:
        response = polly.start_speech_synthesis_task( Text=text,
                                            Engine="standard",
                                            TextType = "text",
                                            OutputFormat="mp3",
                                            OutputS3BucketName = bucket_name,
                                            SampleRate='22050',
                                            VoiceId="Matthew")
        return response # Return the file_name if it is successfully generated
    except Exception as e:
        print(e)
        return None # Return None and print the exception
    
def generatePresignUrl(file_name, bucket_name):
    try:
        url = s3.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name,'Key': file_name},
                                                ExpiresIn=3600)
        return url  # Return the URL if it is successfully generated
    except Exception as e:
        print(e)
        return None  # Return None and print the exception