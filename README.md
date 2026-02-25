# AI-Resume-Optimizer-Using-AWS-BedRock
Serverless GenAI solution that optimizes resumes based on job descriptions using Amazon Bedrock. 
This system reads a resume from S3, aligns it with a given Job Description (JD), improves ATS compatibility, and stores the optimized version back in S3.

## 🏗️ Architecture Overview

User
  │
  ▼
API Gateway (Optional)
  │
  ▼
AWS Lambda
  │
  ├── Read Resume from S3 (Input Bucket)
  ├── Build ATS Optimization Prompt
  ├── Invoke Amazon Bedrock (Claude 3 Haiku)
  ├── Receive Optimized Resume
  └── Store Result in S3 (Output Bucket)
  │
  ▼
User downloads optimized resume via Pre-Signed URL

## 🧩 AWS Services Used
Amazon S3 – Store input resumes & optimized outputs
AWS Lambda – Backend processing logic
Amazon Bedrock (Claude 3 Haiku) – LLM for resume optimization
IAM – Secure permissions
CloudWatch – Logging & monitoring

## 📂 S3 Bucket Structure
Input Bucket - gowthaman-bedrock-resume-input
Output Bucket - gowthaman-bedrock-resume-output

## 🧠 Model Used
### Claude 3 Haiku (Amazon Bedrock Edition)
Why Haiku?
✔ Low cost
✔ Fast response time
✔ Suitable for structured transformation tasks like resume optimization

## 🔄 Process Flow
### 1️⃣ Upload Resume

Upload .txt resume file to:
S3 → gowthaman-bedrock-resume-input

### 2️⃣ Invoke Lambda with JSON Event
```bash
{
  "resume_key": "resume.txt",
  "job_description": "Looking for AWS engineer with Lambda experience"
}
```

### 3️⃣ Lambda Execution Steps

✔ Fetch resume from S3
   Build optimized ATS prompt
   Invoke Bedrock model
   Receive structured improved resume

✔ Store output in S3
   Generate pre-signed download URL

### 4️⃣ Sample Response
```bash
{
  "message": "Resume optimized successfully",
  "download_url": "https://s3-presigned-url..."
}
```

## 🔐 IAM Permissions Required
### Lambda Role must include:
✔ Bedrock Permissions
✔ bedrock:InvokeModel
✔ S3 Permissions
✔ s3:GetObject
✔ s3:PutObject
✔ s3:ListBucket
✔ CloudWatch
✔ logs:CreateLogGroup
✔ logs:CreateLogStream
✔ logs:PutLogEvents

## 💰 Cost Optimization
✔ Fully serverless
✔ No EC2 instances
✔ Pay-per-request model
✔ No idle compute costs

### To minimize costs:
✔ Disable Lambda if not in use
✔ Clean unused S3 files
✔ Monitor Bedrock token usage

## 📬 Contact

For questions or collaboration requests:

* 📧 Email: [ecsgowtham@gmail.com ](mailto:ecsgowtham@gmail.com )
* 🌐 GitHub: [gowthaman25](https://github.com/gowthaman25/)
  
---
