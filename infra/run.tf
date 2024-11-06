resource "google_project_service" "run" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_cloud_run_v2_service" "deploy-iykra-fontgen" {
  name                = "deploy-iykra-fontgen"
  location            = ""
  deletion_protection = false
  ingress             = "ingree_all_traffic"

  template {
    containers {
      image = var.image_uri
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }
}
