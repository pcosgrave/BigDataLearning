provider "aws" {
  region = "us-east-1"
}

module "s3_site" {
  source = "../../modules/s3_site"

  bucket_name = "my-terraform-site-philip-prod-2026-001"
  index_file  = "${path.module}/../../Site/index.html"
}

module "cloudfront" {
  source = "../../modules/cloudfront"

  website_endpoint = module.s3_site.website_endpoint
}

module "api" {
  source = "../../modules/api"

  lambda_zip_path = "${path.module}/../../lambda/function.zip"
  function_name    = "terraform-api-prod"
  lambda_role_name = "lambda-exec-role-prod"
}

resource "null_resource" "invalidate_cache" {
  triggers = {
    file_hash = filemd5("${path.module}/../../Site/index.html")
  }

  provisioner "local-exec" {
    command = "aws cloudfront create-invalidation --distribution-id ${module.cloudfront.distribution_id} --paths '/*'"
  }
}