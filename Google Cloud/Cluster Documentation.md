# Cluster Documentation

## Steps for deploying cluster

---

- The fist step is to  Create a [Google Cloud](https://cloud.google.com) account.

- Later, you will need to create a Google Cloud Project, you must do this in the web page, you only need to do this once. You can give the name that you want.


- Install [Terraform](https://www.terraform.io/downloads.html)
- Install [Google SDK](https://cloud.google.com/sdk/docs/install)
- Install [Chocolately](https://chocolatey.org/install) //Windows users
- Install [Kubectl](https://kubernetes.io/es/docs/tasks/tools/install-kubectl/)
- Config [SDK](https://cloud.google.com/sdk/docs/initializing) 

 ---

### Enable the following [APIS from Google Cloud](https://console.cloud.google.com/apis/library).

- Compute Engine API
- Cloud Monitoring API
- Cloud Login API
- Cloud Identity-Aware Proxy API
- Kubernetes Engine API
- Cloud Storage
- Cloud Storage API
- Cloud Debugger API
- Service Manager API

---
Open the file ***terraform.tfvars***  and change the projectID to your own projectID, it could be any name, this will be your clusterID.

Next, you need to open the file **run-terraform-cluster.bat** and change the **yourClusterID** and the **yourProyectID**, with your own information in this command:

```
gcloud container clusters get-credentials yourClusterID-gke --region us-east1 --project yourProyectID
```

After that, you need to save the script and then run it.

Finally, you need to run the following command:
kubectl apply -k yaml-files


