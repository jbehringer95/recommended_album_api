provider "aws" {
  region = "us-east-1"
  profile = "shuler-io"
}

resource "aws_s3_bucket" "predict-s3" {
  bucket = "shuler-consulting-music-predict"
  acl    = "public-read-write"
}