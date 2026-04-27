output "cloudfront_url" {
  value = module.cloudfront.domain_name
}

output "api_url" {
  value = module.api.api_endpoint
}

output "events_queue_url" {
  value = module.api.events_queue_url
}

output "data_lake_bucket_name" {
  value = module.api.data_lake_bucket_name
}