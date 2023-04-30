resource "aws_s3_bucket" "church_manager_s3_bucket" {
  bucket = "church-manager-s3-bucket"
}

resource "aws_s3_bucket_lifecycle_configuration" "church_manager_s3_bucket_lifecycle" {
  bucket = aws_s3_bucket.church_manager_s3_bucket.id

  rule {
    id      = "DeleteExpiredFiles"
    status  = "Enabled"
    prefix  = "files/"
    expiration {
      days = 1
    }
  }
}