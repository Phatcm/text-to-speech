#provider configure
variable "project_name" {
  type = string
  default = "my-project"
}

variable "region" {
  type = string
  default = "ap-northeast-1"
}

#s3 configure
variable "s3_organize_bucket" {
  type = string
  default = "s3-tts"
}

#iam configure
variable "iam_role_name" {
  type = string
  default = "role-tts"
}

variable "policies_list" {
  type = list(string)
  default = [
    "arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/CloudWatchFullAccess",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  ]
}

#lambda 
variable "lambda_uploader_function_name" {
  type = string
  default = "tts-lambda"
}

variable "lambda_handler" {
  type = string
  default = "lambda_function.lambda_handler"
}

variable "lambda_runtime" {
  type = string
  default = "python3.9"
}

variable "lambda_uploader_output_path" {
  type = string
  default = "lambda_function.zip"
}

variable "lambda_uploader_source_dir" {
  type = string
  default = "./resources/"
}

variable "lambda_uploader_filename" {
  type = string
  default = "lambda_function.zip"
}

variable "s3_bucket_name" {
  type = string
  default = "tts-s3"
}
#api gateway configure
variable "api_name" {
  type = string
  default = "tts-api"
}

