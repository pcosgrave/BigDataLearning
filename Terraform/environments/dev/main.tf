provider "aws" {
  region = "us-east-1"
}

module "s3_site" {
  source = "../../modules/s3_site"

  bucket_name = var.bucket_name
  index_file  = "${path.module}/../../Site/index.html"
}

module "cloudfront" {
  source = "../../modules/cloudfront"

  website_endpoint = module.s3_site.website_endpoint
}

module "api" {
  source = "../../modules/api"

  lambda_zip_path                 = "${path.module}/../../lambda/function.zip"
  processor_zip_path              = "${path.module}/../../processor/function.zip"
  parquet_processor_zip_path      = "${path.module}/../../processor_parquet/function.zip"
  function_name                   = var.function_name
  processor_function_name         = var.processor_function_name
  parquet_processor_function_name = var.parquet_processor_function_name
  lambda_role_name                = var.lambda_role_name
  events_queue_name               = var.events_queue_name
  data_lake_bucket_name           = var.data_lake_bucket_name
  dynamodb_table_name             = var.dynamodb_table_name  
}

resource "null_resource" "invalidate_cache" {
  triggers = {
    file_hash = filemd5("${path.module}/../../Site/index.html")
  }

  provisioner "local-exec" {
    command = "aws cloudfront create-invalidation --distribution-id ${module.cloudfront.distribution_id} --paths '/*'"
  }
}

