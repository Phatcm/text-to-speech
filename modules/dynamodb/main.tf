resource "aws_dynamodb_table" "tts-table" {
    name           = var.table_name
    billing_mode   = "PROVISIONED"
    read_capacity  = 5
    write_capacity = 5
    hash_key       = "user_name"
    range_key      = "file_name"

    attribute {
        name = "user_name"
        type = "S"
    }

    attribute {
        name = "file_name"
        type = "S"
    }
}