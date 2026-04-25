output "cloudfront_url" {
  value = module.cloudfront.domain_name
}

output "api_url" {
  value = module.api.api_endpoint
}