output "api_gateway_invoke_url" {
  value = aws_api_gateway_stage.stage_prod.invoke_url
}