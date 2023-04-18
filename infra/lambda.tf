data "archive_file" "layer_zip" {
  type        = "zip"
  source_file = "../app/lambda_function.py"
  output_path = "../python.zip"
}

resource "aws_lambda_layer_version" "basic_layer" {
  layer_name       = "python"
  filename         = data.archive_file.layer_zip.output_path
  source_code_hash = filebase64sha256(data.archive_file.layer_zip.output_path)

  compatible_runtimes = [
    "python3.9"
  ]
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "../app/lambda_function.py"
  output_path = "../lambda.zip"
}

resource "aws_lambda_function" "lambda" {
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = filebase64sha256(data.archive_file.lambda_zip.output_path)

  function_name = var.project_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.lambda_function.lambda_handler"
  runtime       = "python3.9"
  timeout       = 500
  layers        = ["${aws_lambda_layer_version.basic_layer.arn}"]

  vpc_config {
    subnet_ids         = ["subnet-06142ac6726d42667", "subnet-0136774f343ba95e4", "subnet-00394379445320e9f"]
    security_group_ids = ["sg-0524fc9f3dc12c825"]
  }

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