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
    urls_list = []
    for i in response:
        url = generatePresignUrl(i, bucket_name)
        urls_list.append(url)
    return {
        'statusCode': 200,
        'body': json.dumps(urls_list)
    }

def generateAudioUsingText(text, bucket_name):
    try:
        # Split the text into chunks of 3000 characters or less
        chunks = [text[i:i+3000] for i in range(0, len(text), 3000)]
        
        # Random name for file chunks
        folder_name = str(uuid.uuid4())
        file_name = folder_name+".mp3"
        chunks_list = []
        
        for i, chunk in enumerate(chunks):
            # Generate the audio file for this chunk
            response = polly.synthesize_speech( Text=chunk,
                                            Engine="standard",
                                            TextType = "text",
                                            OutputFormat="mp3",
                                            SampleRate='22050',
                                            VoiceId="Joanna")
            
            # Get the audio data from the response
            audio_data = response['AudioStream'].read()
            
            # Append the chunk name to the list
            chunks_list.append(f"{file_name}({i})")
            
            # Upload the audio data to S3
            s3.put_object(Bucket=bucket_name, Key=f"{folder_name}/({i}){file_name}", Body=audio_data)
        
        return chunks_list # Return the list of chunks
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