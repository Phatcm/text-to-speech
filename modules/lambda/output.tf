output "lambda_function_arn" {
  value = aws_lambda_function.lambda_function[0].arn
}

output "lambda_function_name" {
  value = aws_lambda_function.lambda_function[0].function_name
}

output "lambda_invoke_arn" {
  value = aws_lambda_function.lambda_function[0].invoke_arn
}