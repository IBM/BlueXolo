::For Terraform Dependencies
terraform init
terraform apply -auto-approve

::This could change depending on your clusters name and zone.

gcloud container clusters get-credentials YOUR-CLUSTER-ID-gke --region us-east1 --project YOUR-CLUSTER-ID