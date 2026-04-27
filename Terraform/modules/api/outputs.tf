output "api_endpoint" {
  value = aws_apigatewayv2_api.http_api.api_endpoint
}
output "events_queue_url" {
  value = aws_sqs_queue.events.url
}