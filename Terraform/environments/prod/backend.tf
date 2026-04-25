terraform {
  backend "s3" {
    bucket = "philip-terraform-state-576134964270"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}