provider "aws" {
  region = "us-west-1"
}

//creating s3 bucket for branch frontend content"
resource "aws_s3_bucket" "adriancaballero-branchcontent" {
  bucket = "adriancaballero-branchcontent"
}

resource "aws_s3_bucket_public_access_block" "adriancaballero-branchcontent" {
  bucket = aws_s3_bucket.adriancaballero-branchcontent.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

//create SNS topic that allows for emails 
resource "aws_sns_topic" "owner_updates" {
  name = "user-updates-websiteupdate"
}
resource "aws_sns_topic_subscription" "owner_updates_email_target" {
  topic_arn = aws_sns_topic.owner_updates.arn
  protocol  = "email"
  endpoint  = "abcaballero.py@gmail.com"
}

output "sns_topic_arn" {
  value = aws_sns_topic.owner_updates.arn
}


// Creating IAM roles and policy for all lambda functions
resource "aws_iam_role" "lambda_role" {
  name               = "Lambda_Function_Role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


resource "aws_iam_policy" "iam_policy_for_lambda" {
  name        = "aws_iam_policy_for_terraform_aws_lambda_role"
  path        = "/"
  description = "AWS IAM Policy for managing aws lambda role"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect   = "Allow"
        Action   = [
          "s3:*"
        ]
        Resource = [
          "${aws_s3_bucket.www.adriancaballeroresume.com.arn}/*",
          "${aws_s3_bucket.adriancaballero-branchcontent.arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = "sns:Publish"
        Resource = aws_sns_topic.owner_updates.arn
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
  role        = aws_iam_role.lambda_role.name
  policy_arn  = aws_iam_policy.iam_policy_for_lambda.arn
}


//zipping python initial lambda file 
data "archive_file" "lambda-sync-s3" {
  type = "zip"
  source_file = "${path.module}/backend/lambda-sync-s3website.py"
  output_path = "lambda-sync-s3website.zip"
  output_file_mode = 0666
}

//creating lambda function to move to s3 website, cloudwatch logs, sns
resource "aws_lambda_function" "website-s3-sync" {
  function_name = "lambda_function_syncs3"
  filename = "lambda-sync-s3website.zip"
  role = aws_iam_role.lambda_role.arn
  runtime = "python3.9"
  handler = "lambda-sync-s3website.lambda_handler"
  source_code_hash = data.archive_file.lambda-sync-s3.output_base64sha256
  depends_on = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
  timeout = 10
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.website-s3-sync.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.adriancaballero-branchcontent.arn
}

//add s3 trigger to lambda 
resource "aws_s3_bucket_notification" "trigger_lambdas3sync" {
  bucket = aws_s3_bucket.adriancaballero-branchcontent.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.website-s3-sync.arn
    events              = ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
  }
}