# Cluster Documentation

## Steps for deploying cluster

---

- The fist step is to  Create a [Google Cloud](https://cloud.google.com) account.

- Later, you will need to create a Google Cloud Project, you must do this in the web page, you only need to do this once. You can give the name that you want. The platform will give you the ID of your project, copy it, it will be needed in the following steps.


- Install [Terraform](https://www.terraform.io/downloads.html)
- Install [Google SDK](https://cloud.google.com/sdk/docs/install)
- Install [Chocolately](https://chocolatey.org/install) //Windows users
- Install [Kubectl](https://kubernetes.io/es/docs/tasks/tools/install-kubectl/)
- Config [SDK](https://cloud.google.com/sdk/docs/initializing) 

 ---

### Enable the following [APIS from Google Cloud](https://console.cloud.google.com/apis/library).

- Compute Engine API
- Cloud Login API
- Cloud Identity-Aware Proxy API
- Kubernetes Engine API
- Cloud Storage
- Cloud Storage API
- Cloud Debugger API

---
Open the file ***terraform.tfvars***  and change the **YOUR-PROJECT-ID** to your own projectID.

Next, you need to open the file **run-terraform-cluster.bat** and change the **YOUR-PROJECT-ID** with your own information in this command:

```
gcloud container clusters get-credentials yourProjectID-gke --region us-east1 --project yourProyectID
```
After that, you need to save the script and then run it.

To perform the next steps, you will need four files that are not available on GitHub and that you will have to request from the developers. This is because the files have sensitive cluster settings. 

Once the developers have provided you with the files, you will need to do the following: 

The ***.k8.env***, ***ca-cert.txt*** and ***cert-privkey.txt*** files should be placed in the following directory:

```
...\BlueXolo\OPS\K8\GKE\yaml-files
```

Finally, you need to run the following command inside the yam-files diretory:
```
kubectl apply -k yaml-files
```

To know the IP address of the application run the following command:
```
kubectl get services -n bluexolo
```
The IP to be selected is the one in the "EXTERNAL-IP" column. To access the site just type the IP address in your browser followed by the HTTPS port, ie:
```
35.76.5.23:443
```

To destroy the cluster simply run the ***kill-cluster.bat*** script.