import json
import boto3
import os
import uuid
import time
from botocore.exceptions import ClientError

polly = boto3.client('polly')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    httpMethod = event['httpMethod']
    
    #define s3 bucket connect
    bucket_name = os.environ['BUCKET_NAME']
    #define dynamodb table connect
    table_name = os.environ['TABLE_NAME']
    
    if httpMethod == "POST":
        body = json.loads(event["body"])
        text = body["text"]
        user_name = body["name"]
        upload_time = body["time"]
        
        # Random name for file chunks
        folder_name = str(uuid.uuid4())
        
        #save in dict format to dynamodb
        saveInfo(user_name, folder_name, upload_time, table_name)
        
        response = generateAudioUsingText(text, bucket_name, folder_name)
        urls_list = []
        for i in response:
            url = generatePresignUrl(i, bucket_name)
            urls_list.append(url)
        return {
            'statusCode': 200,
            'body': json.dumps(urls_list)
        }
        
    if httpMethod == "GET":
        if event['queryStringParameters']:
            folder_name = event['queryStringParameters']['download']
            
            response = s3.list_objects_v2(
                Bucket=os.environ['BUCKET_NAME'], 
                Prefix=folder_name+"/"
            )
            
            file_names = [item['Key'] for item in response['Contents']]
            
            urls_list = []
            for file in file_names:
                url = generatePresignUrl(file, bucket_name)
                urls_list.append(url)
                
            return {
                'statusCode': 200,
                'body': json.dumps(urls_list)
            }
            
        else:
            body = json.loads(event["body"])  # Parse the body for GET method
            user_name = body["name"]
            
            db_table = dynamodb.Table(table_name)
            # Query the DynamoDB table
            response = db_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_name').eq(user_name)
            )
            
            # Extract the file_name from the response
            file_data = [{'file_name': item['file_name'], 'upload_time': item['upload_time']} for item in response['Items']]
            
            return {
                'statusCode': 200,
                'body': json.dumps(file_data)
            }

def generateAudioUsingText(text, bucket_name, folder_name):
    try:
        # Split the text into chunks of 3000 characters or less
        chunks = [text[i:i+3000] for i in range(0, len(text), 3000)]
        
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
            chunks_list.append(f"{folder_name}/({i}){file_name}")
            
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
        
def saveInfo(user_name, folder_name, upload_time, table_name):
    try:
        db_table = dynamodb.Table(table_name)
    
        response = db_table.put_item(
            Item={
                "user_name": user_name,
                "file_name": folder_name,
                "upload_time": upload_time
            }
        )
    except Exception as e:
        print(e)
        return None  # Return None and print the exception