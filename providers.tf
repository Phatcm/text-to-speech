terraform {
  backend "s3" {
    bucket = "s3-text-to-speech-tfstate"
    key    = "terraform.tfstate"
    region = "ap-northeast-1"
  }
}