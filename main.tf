terraform {
  required_version = ">=1.0.0"
}

locals {
  name = var.project_name
}

provider "aws" {
  region = var.region
  profile = var.profile
}

module "s3_bucket" {
  source = "./modules/s3"
  s3_organize_bucket = var.s3_organize_bucket
}


module "iam_role" {
  source = "./modules/iam_role"
  iam_role_name = var.iam_role_name
  policies_list = var.policies_list
}

module "lambda" {
  source = "./modules/lambda"
  lambda_function_name = var.lambda_uploader_function_name
  lambda_handler = var.lambda_handler
  lambda_runtime = var.lambda_runtime
  lambda_role_arn = module.iam_role.iam_role_arn
  output_path = var.lambda_uploader_output_path
  source_dir = var.lambda_uploader_source_dir
  filename = var.lambda_uploader_filename
  s3_bucket_name = var.s3_bucket_name
}

module "api_gateway" {
  source = "./modules/api_gateway"
  api_name = var.api_name
  lambda_function_name = module.lambda.lambda_function_name
  lambda_function_arn = module.lambda.lambda_function_arn
  lambda_invoke_arn = module.lambda.lambda_invoke_arn
}

