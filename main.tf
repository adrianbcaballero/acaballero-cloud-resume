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
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::adriancaballero-branchcontent/*",
        "arn:aws:s3:::adriancaballero-branchcontent",
        "arn:aws:s3:::www.adriancaballeroresume.com/*",
        "arn:aws:s3:::www.adriancaballeroresume.com"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "${aws_sns_topic.owner_updates.arn}"
    },
    {
        "Effect": "Allow",
        "Action": "cloudfront:*",
        "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
  role        = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "attach_sns_publish_policy_to_iam_role" {
  role        = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.iam_policy_for_lambda.arn
}

resource "aws_iam_role_policy_attachment" "attach_policy_to_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.iam_policy_for_lambda.arn
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
  depends_on = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role, aws_iam_role_policy_attachment.attach_sns_publish_policy_to_iam_role]
  timeout = 10

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.owner_updates.arn
    }
  }
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

//creating Dynamo DB table 
resource "aws_dynamodb_table" "website-dynamodb-table" {
  name           = "Website-access"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "website_id"

  attribute {
    name = "website_id"
    type = "S"
  }

  attribute {
    name = "access_count"
    type = "N"
  }

  global_secondary_index {
    name               = "AccessCountIndex"
    hash_key           = "access_count"
    projection_type    = "ALL"
  }
}

//initialize at zero
resource "aws_dynamodb_table_item" "initial_website_item" {
  table_name = aws_dynamodb_table.website-dynamodb-table.name

  hash_key = "website_id"
  item = <<ITEM
{
  "website_id": {"S": "adriancaballeroresume.com"},
  "access_count": {"N": "0"}
}
ITEM
}

//lambda function triggered by api gateway
data "archive_file" "lambda-update-dynamodb" {
  type = "zip"
  source_file = "${path.module}/backend/lambda-update-dynamodb.py"
  output_path = "lambda-update-dynamodb.zip"
  output_file_mode = 0666
}

resource "aws_iam_policy" "lambda_full_access_policy" {
  name        = "lambda_full_access_policy"
  description = "Policy for full access to DynamoDB and CloudWatch Logs"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "dynamodb:*"  
        ],
        Resource = "*"
      },
      {
        Effect   = "Allow",
        Action   = [
          "logs:*"  
        ],
        Resource = "*"
      },
      {
        Effect   = "Allow",
        Action   = "apigateway:*",
        Resource = "*"
      },
      {
        Effect   = "Allow",
        Action   = "cloudfront:*",
        Resource = "*"
      },
      {
        Effect   = "Allow",
        Action   = "lambda:*",
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_full_access_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_full_access_policy.arn
}

resource "aws_lambda_function" "update-dynamodb" {
  function_name = "update-dynamodb"
  filename = "lambda-update-dynamodb.zip"
  role = aws_iam_role.lambda_role.arn
  runtime = "python3.9"
  handler = "lambda-update-dynamodb.lambda_handler"
  source_code_hash = data.archive_file.lambda-update-dynamodb.output_base64sha256
  depends_on = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role, aws_iam_role_policy_attachment.lambda_full_access_policy_attachment]
  timeout = 10
}

// API Gateway Resource
resource "aws_api_gateway_rest_api" "website_proxy" {
  name          = "website_proxy"
}

resource "aws_api_gateway_resource" "website_proxy" {
  parent_id   = aws_api_gateway_rest_api.website_proxy.root_resource_id
  path_part   = "websiteproxy"
  rest_api_id = aws_api_gateway_rest_api.website_proxy.id
}

resource "aws_api_gateway_method" "website_proxy" {
  authorization = "NONE"
  http_method   = "POST"
  resource_id   = aws_api_gateway_resource.website_proxy.id
  rest_api_id   = aws_api_gateway_rest_api.website_proxy.id
}

resource "aws_api_gateway_integration" "website_proxy" {
  rest_api_id = aws_api_gateway_rest_api.website_proxy.id
  resource_id = aws_api_gateway_resource.website_proxy.id
  http_method = aws_api_gateway_method.website_proxy.http_method
  integration_http_method = "POST"
  type  = "AWS_PROXY"
  uri = aws_lambda_function.update-dynamodb.invoke_arn
}

data "aws_iam_policy_document" "website_proxy" {
  statement {
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions   = ["execute-api:Invoke"]
    resources = ["*"]

  }
}
resource "aws_api_gateway_rest_api_policy" "website_proxy" {
  rest_api_id = aws_api_gateway_rest_api.website_proxy.id
  policy      = data.aws_iam_policy_document.website_proxy.json
}

resource "aws_api_gateway_deployment" "website_proxy" {
  depends_on = [ aws_api_gateway_integration.website_proxy ]
  rest_api_id = aws_api_gateway_rest_api.website_proxy.id
  stage_name = "stage"
}