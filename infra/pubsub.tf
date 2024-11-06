resource "google_project_service" "pubsub" {
  service            = "pubsub.googleapis.com"
  disable_on_destroy = false
}

resource "google_pubsub_topic" "raw_datalake" {
  name = "raw-datalake-topic"
}

resource "google_pubsub_subscription" "trigger_transform" {
  name  = "trigger-transform-subscription"
  topic = google_pubsub_topic.trigger_transform.id

  push_config {
    push_endpoint = "${google_cloud_run_v2_service.deploy-iykra-fontgen.uri}/transform_google_fonts"

    attributes = {
      x-goog-version = "v1"
    }
  }
}
