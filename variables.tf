#provider configure
variable "project_name" {
  type = string
  default = "my-project"
}

variable "region" {
  type = string
}

variable "profile" {
  type = string
}

#s3 configure
variable "s3_organize_bucket" {
  type = string
}

#iam configure
variable "iam_role_name" {
  type = string
}

variable "policies_list" {
  type = list(string)
}

#lambda 
variable "lambda_uploader_function_name" {
  type = string
}

variable "lambda_handler" {
  type = string
}

variable "lambda_runtime" {
  type = string
}

variable "lambda_uploader_output_path" {
  type = string
}

variable "lambda_uploader_source_dir" {
  type = string
}

variable "lambda_uploader_filename" {
  type = string
}

variable "s3_bucket_name" {
  type = string
}
#api gateway configure
variable "api_name" {
  type = string
  default = "api_gateway"
}

