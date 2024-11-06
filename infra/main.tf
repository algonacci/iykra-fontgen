terraform {
  backend "local" {
    path = "terraform.tfstate"
  }

  required_version = ">= 1.9.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.40.0"
    }
  }
}

provider "google" {
  project = var.PROJECT_ID
  region  = var.GCP_REGION
}
