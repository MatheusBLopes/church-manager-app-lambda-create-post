data "archive_file" "zip" {
  type        = "zip"
  source_file = "../app/lambda_function.py"
  output_path = "../lambda.zip"
}

resource "aws_lambda_function" "lambda" {
  filename         = data.archive_file.zip.output_path
  source_code_hash = filebase64sha256(data.archive_file.zip.output_path)

  function_name = var.project_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.lambda_function.lambda_handler"
  runtime       = "python3.9"
  timeout       = 10
  # publish       = true

  tags = {
    "permit-github-action" = true
  }
}

resource "aws_lambda_alias" "alias_dev" {
  name             = "dev"
  description      = "dev"
  function_name    = aws_lambda_function.lambda.arn
  function_version = "$LATEST"
}

resource "aws_lambda_alias" "alias_prod" {
  name             = "prod"
  description      = "prod"
  function_name    = aws_lambda_function.lambda.arn
  function_version = "$LATEST"
}


resource "aws_cloudwatch_log_group" "convert_log_group" {
  name = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
}