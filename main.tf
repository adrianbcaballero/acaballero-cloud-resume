provider "aws" {
  region = "us-west-1"
}

//creating s3 bucket for branch frontend content"
resource "aws_s3_bucket" "adriancaballero-branchcontent" {
  bucket = "adriancaballero-branchcontent"
  region = "us-west-1"
}

resource "aws_s3_bucket_public_access_block" "adriancaballero-branchcontent" {
  bucket = aws_s3_bucket.adriancaballero-branchcontent.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}