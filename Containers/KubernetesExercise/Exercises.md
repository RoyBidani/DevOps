### Add a history feature to your weather app, save all search queries data (in a separate json file by date and city) to local FS. Add a web page showing the history as downloadable files.


### Step 1: Recording Search Queries to a JSON File

To save search query data (date and city) to a JSON file, you can follow these steps:

1. Import the necessary modules for working with JSON and managing file operations in your `app.py`:

   ```python
   import json
   import os
   from flask import make_response
   ```

2. Create a function to save search queries to a JSON file. You can do this in your `app.py` file, just below your current code:

   ```python
   def save_search_history(date, city):
       history_data = []
       filename = 'search_history.json'

       # Check if the history file exists
       if os.path.exists(filename):
           with open(filename, 'r') as file:
               history_data = json.load(file)

       # Append the new search query to the history
       history_data.append({'date': date, 'city': city})

       # Save the updated history to the file
       with open(filename, 'w') as file:
           json.dump(history_data, file)
           file.write('\n')

   ```

3. Next, modify your `weather_display` route to call this function and pass the current date and city:

   ```python
   @app.route("/weather", methods=['POST'])
   def weather_display():
       location = request.form['location']
       weather_info = Api.get_weather(location)

       if weather_info[0]['cod'] == '404':
           error_message = 'City not found. Please enter a valid city.'
           return render_template('index.html', error_message=error_message)

       # Save the search query to the history
       date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       save_search_history(date, location)

       return render_template('weather.html', location=location, weather_info=weather_info)
   ```

Now, whenever a user searches for weather, the search query (date and city) will be saved to a JSON file named `search_history.json`.

### Step 2: Creating a Web Page to Display and Download Search History

To create a web page that displays and allows users to download search history, follow these steps:

1. Create a new HTML template file called `history.html` in your 'templates' folder (create the folder if it doesn't exist). This file will display the search history:

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Search History</title>
   </head>
   <body>
       <h1>Search History</h1>

       <ul>
           {% for entry in search_history %}
               <li>{{ entry.date }} - {{ entry.city }} <a href="{{ url_for('download_history', city=entry.city) }}">Download</a></li>
           {% endfor %}
       </ul>
   </body>
   </html>
   ```

2. Update your `app.py` file to include a new route for displaying the search history page:

   ```python
   @app.route("/history")
   def search_history():
       with open('search_history.json', 'r') as file:
           search_history = json.load(file)
       return render_template('history.html', search_history=search_history)
   ```

3. Add a route to allow users to download search history by city:

   ```python
   
	@app.route("/download/<city>")
	def download_history(city):
    	with open('search_history.json', 'r') as file:
        	search_history = json.load(file)

    	# Create a list of search entries for the specified city
    	city_searches = [entry for entry in search_history if entry['city'] == city]

    	# Create a downloadable JSON file
    	response = make_response(json.dumps(city_searches, indent=4))
    	response.headers['Content-Disposition'] = f'attachment; filename={city}_search_history.json'
    	response.headers['Content-Type'] = 'application/json'
    	return response


   ```

4. Finally, create a link in your `index.html` template to navigate to the search history page:

   ```html
   <a href="{{ url_for('search_history') }}">View Search History</a>
   ```

Now, when users click on "View Search History," they will see a list of search queries by date and city on the 'history.html' page. They can also download the search history for each city as a JSON file by clicking the "Download" link.


### Configure your app background color as $(BG_COLOR) ENV variable.

### 1. Modify `app.py`:

At the top of your `app.py` file, import the `os` module to work with environment variables:

```python
import os
```

Define a default background color (you can choose any color code or use a variable):

```python
# Default background color (if ENV variable is not set)
BG_COLOR = '#f2f2f2'
```

Access the environment variable to set the background color in your Flask app:

```python
# Get the background color from the ENV variable, use the default if not set
app.config['BG_COLOR'] = os.environ.get('BG_COLOR', BG_COLOR)
```

### 2. Use the Environment Variable in Your CSS Files (e.g., 'index.css' and 'style.css'):

Modify your Flask route for the home and weather pages ('/','/weather' ) to pass the `BG_COLOR` variable to the templates:

```python
@app.route('/')
def home():
    return render_template('index.html', BG_COLOR=app.config['BG_COLOR'])
```

```python
@app.route("/weather", methods=['POST'])
def weather_display():
    return render_template('weather.html', location=location, weather_info=weather_info, BG_COLOR=app.config['BG_COLOR'])
```
2. In your templates, you can then use the `BG_COLOR` variable to set the background color:

```html
<body style="background-color: {{ BG_COLOR }};">
```

This code uses the `app.config['BG_COLOR']` variable to set the background color dynamically based on the environment variable.

### 3. Set the Environment Variable:

Before running your Flask application, you need to set the `BG_COLOR` environment variable. You can do this in your terminal or in your development environment. For example, to set the background color to blue:


   ```bash
   export BG_COLOR='#0000FF'
   ```


### 4. Run Your Flask App:

Start or restart your Flask application to apply the new background color configuration:

```bash
python app.py
```

Now, your Flask app will use the background color specified in the `BG_COLOR` environment variable, allowing you to change the background color easily by modifying the environment variable without having to edit the CSS files directly.



### Set up a k8s cluster on EKS with 1 manager and 2 worker nodes.

To create an Amazon Elastic Kubernetes Service (EKS) cluster on AWS with one master node (control plane) and two worker nodes, you can follow these step-by-step instructions:

**Prerequisites:**
1. **AWS Account:** Ensure you have an AWS account and are logged in to the AWS Management Console.

2. **AWS CLI and eksctl:** Install and configure the AWS CLI and eksctl on your local machine. 

3. **IAM Role:** Create an IAM role for your EKS cluster with the necessary permissions. The role should have permissions for EKS, EC2, and other resources that your cluster and worker nodes will need. Attach this role to your EC2 instances (worker nodes).

**Step 1: Create an EKS Cluster:**
```bash
eksctl create cluster \
  --name my-eks-cluster \
  --region your-preferred-region \
  --nodegroup-name my-node-group \
  --node-type t2.micro \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```
- Replace `my-eks-cluster` with your desired cluster name.
- Change `your-preferred-region` to your preferred AWS region.

**Step 2: Configure `kubectl` to Interact with the Cluster:**
```bash
aws eks --region your-preferred-region update-kubeconfig --name my-eks-cluster
```

**Step 3: Verify the Cluster:**
```bash
kubectl get nodes
```
You should see the two worker nodes listed and in the "Ready" state.

That's it! You've successfully created an EKS cluster with one master node and two worker nodes. You can now deploy and manage your containerized applications on this cluster.



### Using helm charts:
Helm charts are designed to encapsulate Kubernetes manifests, including Deployment, Service, ConfigMap, and other resource definitions, within a structured directory. Helm uses templates to dynamically generate these manifests when you install the chart. Therefore, you typically do not need to create individual `deployment.yaml` or `service.yaml` files. Instead, you provide the templates and values in the Helm chart structure.
key components in this Helm chart structure:

1. **values.yaml**: This file contains configuration values for your Helm chart. These values can be overridden when you install the chart. It sets values such as the number of replicas, Docker image information, service settings, and a ConfigMap name.

2. **Deployment.yaml**: This file defines a Kubernetes Deployment resource. It uses the values from `values.yaml` to customize the Deployment. It sets the number of replicas, container image, image pull policy, ports, and an environment variable (`BG_COLOR`) sourced from a ConfigMap.

3. **service.yaml**: This file defines a Kubernetes Service resource. Like the Deployment, it uses values from `values.yaml` to customize the Service. It specifies the service type, selector to target the Deployment pods, and port configurations.

4. **configmap.yaml**: This file defines a Kubernetes ConfigMap resource. It contains a single key-value pair with a background color setting. The value is set to "green" .

5. **weather-app-chart**: This is the root directory of your Helm chart. Inside this directory, you typically have the following subdirectories and files:
   - **charts**: This directory is used for sub-charts if your Helm chart depends on other charts.
   - **templates**: This directory contains the Kubernetes resource templates that will be rendered and deployed when you install the Helm chart. In your case, it includes `deployment.yaml` and `service.yaml`.
   - **_helpers.tpl**: This is a common Helm convention for defining template helper functions that can be used in your resource templates.

Here's how this structure works together:
- When you install the Helm chart using `helm install`, Helm takes the values from `values.yaml` and uses them to render the templates in the `templates` directory.
- The rendered templates are then applied to your Kubernetes cluster, creating the Deployment, Service, and ConfigMap resources with the specified configurations.
- The ConfigMap provides configuration data to the pods in the Deployment, such as the background color.


# Terraform AWS EKS Configuration

This Terraform configuration manages the deployment of an Amazon Elastic Kubernetes Service (EKS) cluster in AWS. The following sections describe the key components and configurations within the Terraform files.

## terraform.tf

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.7.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.5.1"
    }

    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0.4"
    }

    cloudinit = {
      source  = "hashicorp/cloudinit"
      version = "~> 2.3.2"
    }
  }

  required_version = "~> 1.0"
}
```

This section defines the required providers and Terraform version.

## Variables.tf

```hcl
variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-3"
}
```

Defines an AWS region variable with a default value.

## main.tf
```hcl

provider "aws" {
  region = var.region
}

# Filter out local zones, which are not currently supported 
# with managed node groups
data "aws_availability_zones" "available" {
  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}

locals {
  cluster_name = "education-eks-${random_string.suffix.result}"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "education-vpc"

  cidr = "10.0.0.0/16"
  azs  = slice(data.aws_availability_zones.available.names, 0, 3)

  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = 1
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = 1
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.15.3"

  cluster_name    = local.cluster_name
  cluster_version = "1.27"

  vpc_id                         = module.vpc.vpc_id
  subnet_ids                     = module.vpc.private_subnets
  cluster_endpoint_public_access = true

  eks_managed_node_group_defaults = {
    ami_type = "AL2_x86_64"

  }

  eks_managed_node_groups = {
    one = {
      name = "node-group-1"

      instance_types = ["t3.small"]

      min_size     = 1
      max_size     = 3
      desired_size = 2
    }

    two = {
      name = "node-group-2"

      instance_types = ["t3.small"]

      min_size     = 1
      max_size     = 3
      desired_size = 2
    }
  }
}


# https://aws.amazon.com/blogs/containers/amazon-ebs-csi-driver-is-now-generally-available-in-amazon-eks-add-ons/ 
data "aws_iam_policy" "ebs_csi_policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
}

module "irsa-ebs-csi" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  version = "4.7.0"

  create_role                   = true
  role_name                     = "AmazonEKSTFEBSCSIRole-${module.eks.cluster_name}"
  provider_url                  = module.eks.oidc_provider
  role_policy_arns              = [data.aws_iam_policy.ebs_csi_policy.arn]
  oidc_fully_qualified_subjects = ["system:serviceaccount:kube-system:ebs-csi-controller-sa"]
}

resource "aws_eks_addon" "ebs-csi" {
  cluster_name             = module.eks.cluster_name
  addon_name               = "aws-ebs-csi-driver"
  addon_version            = "v1.20.0-eksbuild.1"
  service_account_role_arn = module.irsa-ebs-csi.iam_role_arn
  tags = {
    "eks_addon" = "ebs-csi"
    "terraform" = "true"
  }
}
```

## outputs.tf

```hcl
output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = module.eks.cluster_security_group_id
}

output "region" {
  description = "AWS region"
  value       = var.region
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = module.eks.cluster_name
}
```

Defines output variables for key information about the EKS cluster.

This Terraform configuration sets up an EKS cluster in the specified AWS region, deploys necessary modules, IAM roles, and the EBS CSI driver, and provides essential cluster information through output variables.

# Kubernetes Deployment and Service Configuration

This is Kubernetes deployment and service configuration for two applications: "Weather" and "Soliter." Below, you will find a breakdown of the YAML files and their configurations.

## weather-deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: weather-deployment
spec:
  replicas: {{ .Values.replicacount }}
  selector:
    matchLabels:
      app: weather
  template:
    metadata:
      labels:
        app: weather
    spec:
      containers:
        - name: weather
          image: {{ .Values.image }}
          ports:
            - containerPort: 8000
          env:
            - name: BACKGROUND_COLOR
              valueFrom:
                configMapKeyRef:
                  name: blue-configmap
                  key: BACKGROUND_COLOR
          volumeMounts:
            - name: data
              mountPath: /json
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: block-claim
```

## soliter-deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: soliter-deployment
spec:
  replicas: {{ .Values.replicacount }}
  selector:
    matchLabels:
      app: soliter-app
  template:
    metadata:
      labels:
        app: soliter-app
    spec:
      containers:
        - name: soliter
          image: chimenesjr/solitaire:nginx
          ports:
            - containerPort: 80
```

## configmap.yaml

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: blue-configmap
data:
  BACKGROUND_COLOR: blue
```

## ebs-storage-class.yaml

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
```

## ebs-pvc.yaml

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: block-claim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: ebs-sc
  resources:
    requests:
      storage: 12Gi
```

## ingress.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: weather-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  ingressClassName: nginx
  rules:
    - host: www.weather.io
      http:
        paths:
          - path: /
            pathType: ImplementationSpecific
            backend:
              service:
                name: weather-service
                port:
                  number: 32300

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: soliter-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  ingressClassName: nginx
  rules:
    - host: www.soliter.io
      http:
        paths:   
          - path: /
            pathType: Prefix
            backend:
              service:
                name: soliter-service
                port:
                  number: 32400
```

## nginx-controller.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  labels:
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
  name: ingress-nginx
---
apiVersion: v1
automountServiceAccountToken: true
kind: ServiceAccount
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx
  namespace: ingress-nginx
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    app.kubernetes.io/component: admission-webhook
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-admission
  namespace: ingress-nginx
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx
  namespace: ingress-nginx
rules:
- apiGroups:
  - ""
  resources:
  - namespaces
  verbs:
  - get
- apiGroups:
  - ""
  resources:
  - configmaps
  - pods
  - secrets
  - endpoints
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - ""
  resources:
  - services
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - networking.k8s.io
  resources:
  - ingresses
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - networking.k8s.io
  resources:
  - ingresses/status
  verbs:
  - update
- apiGroups:
  - networking.k8s.io
  resources:
  - ingressclasses
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - coordination.k8s.io
  resourceNames:
  - ingress-nginx-leader
  resources:
  - leases
  verbs:
  - get
  - update
- apiGroups:
  - coordination.k8s.io
  resources:
  - leases
  verbs:
  - create
- apiGroups:
  - ""
  resources:
  - events
  verbs:
  - create
  - patch
- apiGroups:
  - discovery.k8s.io
  resources:
  - endpointslices
  verbs:
  - list
  - watch
  - get
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  labels:
    app.kubernetes.io/component: admission-webhook
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-admission
  namespace: ingress-nginx
rules:
- apiGroups:
  - ""
  resources:
  - secrets
  verbs:
  - get
  - create
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  - endpoints
  - nodes
  - pods
  - secrets
  - namespaces
  verbs:
  - list
  - watch
- apiGroups:
  - coordination.k8s.io
  resources:
  - leases
  verbs:
  - list
  - watch
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
- apiGroups:
  - ""
  resources:
  - services
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - networking.k8s.io
  resources:
  - ingresses
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - ""
  resources:
  - events
  verbs:
  - create
  - patch
- apiGroups:
  - networking.k8s.io
  resources:
  - ingresses/status
  verbs:
  - update
- apiGroups:
  - networking.k8s.io
  resources:
  - ingressclasses
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - discovery.k8s.io
  resources:
  - endpointslices
  verbs:
  - list
  - watch
  - get
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    app.kubernetes.io/component: admission-webhook
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-admission
rules:
- apiGroups:
  - admissionregistration.k8s.io
  resources:
  - validatingwebhookconfigurations
  verbs:
  - get
  - update
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx
  namespace: ingress-nginx
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: ingress-nginx
subjects:
- kind: ServiceAccount
  name: ingress-nginx
  namespace: ingress-nginx
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    app.kubernetes.io/component: admission-webhook
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-admission
  namespace: ingress-nginx
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: ingress-nginx-admission
subjects:
- kind: ServiceAccount
  name: ingress-nginx-admission
  namespace: ingress-nginx
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: ingress-nginx
subjects:
- kind: ServiceAccount
  name: ingress-nginx
  namespace: ingress-nginx
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    app.kubernetes.io/component: admission-webhook
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-admission
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: ingress-nginx-admission
subjects:
- kind: ServiceAccount
  name: ingress-nginx-admission
  namespace: ingress-nginx
---
apiVersion: v1
data:
  allow-snippet-annotations: "false"
kind: ConfigMap
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-controller
  namespace: ingress-nginx
---
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-controller
  namespace: ingress-nginx
spec:
  externalTrafficPolicy: Local
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - appProtocol: http
    name: http
    port: 80
    protocol: TCP
    targetPort: http
  - appProtocol: https
    name: https
    port: 443
    protocol: TCP
    targetPort: https
  selector:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
  type: LoadBalancer
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-controller-admission
  namespace: ingress-nginx
spec:
  ports:
  - appProtocol: https
    name: https-webhook
    port: 443
    targetPort: webhook
  selector:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-controller
  namespace: ingress-nginx
spec:
  minReadySeconds: 0
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app.kubernetes.io/component: controller
      app.kubernetes.io/instance: ingress-nginx
      app.kubernetes.io/name: ingress-nginx
  strategy:
    rollingUpdate:
      maxUnavailable: 1
    type: RollingUpdate
  template:
    metadata:
      labels:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/part-of: ingress-nginx
        app.kubernetes.io/version: 1.9.0
    spec:
      containers:
      - args:
        - /nginx-ingress-controller
        - --publish-service=$(POD_NAMESPACE)/ingress-nginx-controller
        - --election-id=ingress-nginx-leader
        - --controller-class=k8s.io/ingress-nginx
        - --ingress-class=nginx
        - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
        - --validating-webhook=:8443
        - --validating-webhook-certificate=/usr/local/certificates/cert
        - --validating-webhook-key=/usr/local/certificates/key
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: LD_PRELOAD
          value: /usr/local/lib/libmimalloc.so
        image: registry.k8s.io/ingress-nginx/controller:v1.9.0@sha256:c15d1a617858d90fb8f8a2dd60b0676f2bb85c54e3ed11511794b86ec30c8c60
        imagePullPolicy: IfNotPresent
        lifecycle:
          preStop:
            exec:
              command:
              - /wait-shutdown
        livenessProbe:
          failureThreshold: 5
          httpGet:
            path: /healthz
            port: 10254
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        name: controller
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        - containerPort: 443
          name: https
          protocol: TCP
        - containerPort: 8443
          name: webhook
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /healthz
            port: 10254
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources:
          requests:
            cpu: 100m
            memory: 90Mi
        securityContext:
          allowPrivilegeEscalation: true
          capabilities:
            add:
            - NET_BIND_SERVICE
            drop:
            - ALL
          runAsUser: 101
        volumeMounts:
        - mountPath: /usr/local/certificates/
          name: webhook-cert
          readOnly: true
      dnsPolicy: ClusterFirst
      nodeSelector:
        kubernetes.io/os: linux
      serviceAccountName: ingress-nginx
      terminationGracePeriodSeconds: 300
      volumes:
      - name: webhook-cert
        secret:
          secretName: ingress-nginx-admission
---
apiVersion: batch/v1
kind: Job
metadata:
  labels:
    app.kubernetes.io/component: admission-webhook
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-admission-create
  namespace: ingress-nginx
spec:
  template:
    metadata:
      labels:
        app.kubernetes.io/component: admission-webhook
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/part-of: ingress-nginx
        app.kubernetes.io/version: 1.9.0
      name: ingress-nginx-admission-create
    spec:
      containers:
      - args:
        - create
        - --host=ingress-nginx-controller-admission,ingress-nginx-controller-admission.$(POD_NAMESPACE).svc
        - --namespace=$(POD_NAMESPACE)
        - --secret-name=ingress-nginx-admission
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        image: registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20230407@sha256:543c40fd093964bc9ab509d3e791f9989963021f1e9e4c9c7b6700b02bfb227b
        imagePullPolicy: IfNotPresent
        name: create
        securityContext:
          allowPrivilegeEscalation: false
      nodeSelector:
        kubernetes.io/os: linux
      restartPolicy: OnFailure
      securityContext:
        fsGroup: 2000
        runAsNonRoot: true
        runAsUser: 2000
      serviceAccountName: ingress-nginx-admission
---
apiVersion: batch/v1
kind: Job
metadata:
  labels:
    app.kubernetes.io/component: admission-webhook
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-admission-patch
  namespace: ingress-nginx
spec:
  template:
    metadata:
      labels:
        app.kubernetes.io/component: admission-webhook
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/part-of: ingress-nginx
        app.kubernetes.io/version: 1.9.0
      name: ingress-nginx-admission-patch
    spec:
      containers:
      - args:
        - patch
        - --webhook-name=ingress-nginx-admission
        - --namespace=$(POD_NAMESPACE)
        - --patch-mutating=false
        - --secret-name=ingress-nginx-admission
        - --patch-failure-policy=Fail
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        image: registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20230407@sha256:543c40fd093964bc9ab509d3e791f9989963021f1e9e4c9c7b6700b02bfb227b
        imagePullPolicy: IfNotPresent
        name: patch
        securityContext:
          allowPrivilegeEscalation: false
      nodeSelector:
        kubernetes.io/os: linux
      restartPolicy: OnFailure
      securityContext:
        fsGroup: 2000
        runAsNonRoot: true
        runAsUser: 2000
      serviceAccountName: ingress-nginx-admission
---
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: nginx
spec:
  controller: k8s.io/ingress-nginx
---
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  labels:
    app.kubernetes.io/component: admission-webhook
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.9.0
  name: ingress-nginx-admission
webhooks:
- admissionReviewVersions:
  - v1
  clientConfig:
    service:
      name: ingress-nginx-controller-admission
      namespace: ingress-nginx
      path: /networking/v1/ingresses
  failurePolicy: Fail
  matchPolicy: Equivalent
  name: validate.nginx.ingress.kubernetes.io
  rules:
  - apiGroups:
    - networking.k8s.io
    apiVersions:
    - v1
    operations:
    - CREATE
    - UPDATE
    resources:
    - ingresses
  sideEffects: None

```

## values.yaml

```yaml
replicacount: 4
image: yarinlaniado/capyweather:ebs-json
```

## Chart.yaml

```yaml
apiVersion: v2
name: roy-test
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "1.16.0"
```

This set of YAML files provides the configurations required for deploying the "Weather" and "Soliter" applications in a Kubernetes cluster. You can customize the number of replicas, container images, and other settings by modifying the values in the `values.yaml` file.



Performing a rolling update and rollback in Kubernetes typically involves updating the configuration and observing the application's behavior. Below are the steps to perform a rolling update and rollback while ensuring the availability of the application:

### Rolling Update:

1. **Update ConfigMap:**
   Change the `BACKGROUND_COLOR` value in the `blue-configmap` to "green-configmap" or vice versa, depending on which color you want to use.

2. **Apply ConfigMap Change:**
   Apply the updated ConfigMap to Kubernetes:

   ```bash
   helm upgrade appv1 .
   ```

3. **Monitor Rolling Update:**
   Watch the progress of the rolling update by checking the status of the Deployment:

   ```bash
   kubectl get deployment weather-deployment --watch
   ```

   You should see the old pods gradually terminated and new pods created with the updated ConfigMap.

4. **Test Application Availability:**
   Continuously access the application (e.g., using a web browser or `curl`) while the rolling update is in progress. Ensure that the application remains accessible and that the background color changes as expected.

5. **Rolling Update Verification:**
   After the rolling update is complete, verify that the application is still working correctly with the new ConfigMap.

### Rollback:

1. **Rollback Deployment:**
   If you want to perform a rollback, you can use the following command:

   ```bash
	helm rollback <RELEASE> [REVISION] [flags]
   ```
   
   for example:
   	```bash
	 helm rollback appv1 1
	```

   This will roll back the Deployment to the previous revision.

2. **Monitor Rollback:**
   Watch the progress of the rollback by checking the status of the Deployment:

   ```bash
   kubectl get deployment weather-deployment --watch
   ```

   You should see the Deployment being rolled back to the previous version.

3. **Test Application Availability:**
   Continuously access the application while the rollback is in progress. Ensure that the application remains accessible and that it reverts to its previous state (background color) as per the previous ConfigMap.

4. **Rollback Verification:**
   After the rollback is complete, verify that the application is working as expected with the previous ConfigMap.

If you don't notice any differences in the application behavior during both the rolling update and rollback, it indicates that the update and rollback processes are working correctly, and the application remains available without disruptions. If you do encounter issues, review the Kubernetes logs, events, and configurations to identify and resolve any problems.
