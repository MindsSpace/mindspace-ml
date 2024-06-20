provider "google" {
  project = "mindspace-capstone-project"
}

resource "google_cloud_run_v2_service" "default" {
  name     = "mindspace-learning"
  location = "asia-southeast2"
  client   = "terraform"

  # set the port to 8080


  template {
    containers {
      image = "asia-southeast2-docker.pkg.dev/mindspace-capstone-project/mindspace/mechine-learning:latest"
      ports {
        container_port = 8080
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "noauth" {
  location = google_cloud_run_v2_service.default.location
  name     = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
