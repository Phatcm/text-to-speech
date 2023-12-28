variable "lambda_function_name" {
  type = string
  default = "lambda_function"
}

variable "lambda_role_arn" {
  type = string
}

variable "lambda_handler" {
  type = string
}

variable "lambda_runtime" {
  type = string
}

variable "output_path" {
  type = string
}

variable "source_dir" {
  type = string
}

variable "filename" {
  type = string
}

variable "s3_bucket_name" {
  type = string
}