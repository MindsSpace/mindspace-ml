provider "google" {
  project = "mindspace-capstone-project"
}

resource "google_cloud_run_v2_service" "default" {
  name     = "mindspace-learning"
  location = "asia-southeast2"
  client   = "terraform"

  template {
    containers {
      image = "asia-southeast2-docker.pkg.dev/mindspace-capstone-project/mindspace/mechine-learning:latest"
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "noauth" {
  location = google_cloud_run_v2_service.default.location
  name     = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
