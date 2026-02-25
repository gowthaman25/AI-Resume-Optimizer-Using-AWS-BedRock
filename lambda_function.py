import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

#INPUT_BUCKET = "gowthaman-bedrock-resume-input"
OUTPUT_BUCKET = "gowthaman-bedrock-resume-output"

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def extract_text_from_s3(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    content = obj["Body"].read().decode("utf-8")
    return content


def build_prompt(resume_text, jd_text):
    prompt = f"""
You are an expert ATS resume optimizer.

JOB DESCRIPTION:
{jd_text}

CURRENT RESUME:
{resume_text}

TASK:
1. Identify skill gaps.
2. Reorder resume based on Job Description priority.
3. Improve bullet points with quantified impact.
4. Keep information truthful.
5. Output clean professional resume.
6. Ensure ATS optimized keywords included.

Return only the optimized resume.
"""
    return prompt


def invoke_bedrock(prompt):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1200,
        "temperature": 0.4,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body)
    )

    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]


def save_output_to_s3(text_output):
    file_name = f"optimized_resume_{uuid.uuid4()}.txt"
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=file_name,
        Body=text_output.encode("utf-8")
    )

    signed_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": OUTPUT_BUCKET, "Key": file_name},
        ExpiresIn=3600
    )

    return signed_url


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        #resume_key = body["resume_key"]
        jd_text = body["job_description"]

        # Step 1: Get Resume
        #resume_text = extract_text_from_s3(INPUT_BUCKET, resume_key)
        resume_text = body["resume_text"]

        # Step 2: Build Prompt
        prompt = build_prompt(resume_text, jd_text)

        # Step 3: Call Bedrock
        optimized_resume = invoke_bedrock(prompt)

        # Step 4: Store Output
        download_url = save_output_to_s3(optimized_resume)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Resume optimized successfully",
                "download_url": download_url
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
