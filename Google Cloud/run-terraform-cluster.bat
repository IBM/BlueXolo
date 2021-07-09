::For Terraform Dependencies
terraform init
terraform apply -auto-approve

::This could change depending on your clusters name and zone.

gcloud container clusters get-credentials bluexolo-cluster-315504-gke --region us-east1 --project bluexolo-cluster-315504