resource "google_project_service" "storage" {
  service            = "storage.googleapis.com"
  disable_on_destroy = false
}

resource "google_storage_bucket" "data_lake" {
  name          = "fontgen-datalake"
  location      = "US"
  force_destroy = true

  public_access_prevention = "enforced"
}

resource "google_storage_notification" "raw_data_lake" {
  bucket             = google_storage_bucket.data_lake.name
  payload_format     = "JSON_API_V1"
  topic              = google_pubsub_topic.raw_datalake.id
  event_types        = ["OBJECT_FINALIZE"]
  object_name_prefix = "raw/"
  depends_on         = [google_pubsub_topic_iam_binding.binding]
}

data "google_storage_project_service_account" "gcs_account" {
}

resource "google_pubsub_topic_iam_binding" "raw_data_lake" {
  topic   = google_pubsub_topic.raw_datalake.id
  role    = "roles/pubsub.publisher"
  members = ["serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"]
}
