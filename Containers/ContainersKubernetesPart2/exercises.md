
## Table of Contents

1. [Create an Nginx Pod with Environment Variables](#create-an-nginx-pod-with-environment-variables)
2. [Create a Busybox Deployment on a Specific Node](#create-a-busybox-deployment-on-a-specific-node)
3. [Initiate a Rolling Update on a Deployment](#initiate-a-rolling-update-on-a-deployment)
4. [Rollback a Deployment Update](#rollback-a-deployment-update)
5. [Create a Filebeat DaemonSet](#create-a-filebeat-daemonset)
6. [Use an NFS Server as a PV](#use-an-nfs-server-as-a-pv)
7. [Advanced Exercise: Use a Colleague's NFS Server as a PV](#advanced-exercise-use-a-colleagues-nfs-server-as-a-pv)

---

## Create an Nginx Pod with Environment Variables

### Step 1: Create a ConfigMap with Environment Variables

Start by creating a ConfigMap that contains the environment variables for your Nginx pod. Use the following YAML as an example:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  NGINX_PORT: "8080"
  NGINX_SERVER_NAME: "my-nginx-server"
```

You can create this ConfigMap by running:

```bash
kubectl apply -f nginx-configmap.yaml
```

### Step 2: Create a Secret with Sensitive Environment Variables

Next, create a Secret to store sensitive environment variables like API keys or passwords. Use the following YAML as an example:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: nginx-secret
type: Opaque
data:
  DB_PASSWORD: <base64-encoded-password>
```

Replace `<base64-encoded-password>` with the actual base64-encoded password. Create the Secret by running:

```bash
kubectl apply -f nginx-secret.yaml
```

### Step 3: Create the Nginx Pod Using Environment Variables from ConfigMap and Secret

Now, create the Nginx pod and inject the environment variables from the ConfigMap and Secret. Use the following YAML as an example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx-container
      image: nginx:latest
      env:
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: nginx-config
              key: NGINX_PORT
        - name: SERVER_NAME
          valueFrom:
            configMapKeyRef:
              name: nginx-config
              key: NGINX_SERVER_NAME
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: nginx-secret
              key: DB_PASSWORD
```

Apply the pod configuration:

```bash
kubectl apply -f nginx-pod.yaml
```

### Step 4: Verify the Nginx Pod

Check if the Nginx pod is running and has the environment variables set correctly:

```bash
kubectl get pods nginx-pod
```

You should see the pod in the "Running" state. To inspect the environment variables inside the pod, execute a shell in the container:

```bash
kubectl exec -it nginx-pod -- /bin/sh
```

Inside the pod, you can print the environment variables:

```bash
echo $PORT
echo $SERVER_NAME
echo $DB_PASSWORD
```

You should see the values you defined in the ConfigMap and Secret.

That's it! You've successfully created an Nginx pod with environment variables sourced from both a ConfigMap and a Secret in Kubernetes.

---

## Create a Busybox Deployment on a Specific Node

### Step 1: Create a Busybox Deployment on a Specific Worker Node

1. List all nodes in your cluster to find their names:

   ```bash
   kubectl get nodes
   ```

   Note down the name of the specific node you want to target.

2. Create a Busybox deployment YAML file (`busybox-deployment.yaml`) with node affinity to schedule pods on the chosen node. Replace `<node-name>` with the actual node name:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: busybox-deployment
   spec:
     replicas: 1
     template:
       metadata:
         labels:
           app: busybox
       spec:
         affinity:
           nodeAffinity:
             requiredDuringSchedulingIgnoredDuringExecution:
               nodeSelectorTerms:
               - matchExpressions:
                 - key: kubernetes.io/hostname
                   operator: In
                   values:
                   - <node-name>
         containers:
         - name: busybox
           image: busybox
           command:
           - sleep
           - "3600"
   ```

   Apply the deployment:

   ```bash
   kubectl apply -f busybox-deployment.yaml
   ```

   This will create a Busybox pod on the specified node.

### Step 2: Delete the Busybox Deployment

1. Delete the Busybox deployment:

   ```bash
   kubectl delete deployment busybox-deployment
   ```

   This will remove the deployment, and the pod will be deleted as a result.

### Step 3: Disable Scheduling on the Specific Node

1. To disable scheduling on the specific node, add a taint to the node that repels pods. Replace `<node-name>` with the actual node name:

   ```bash
   kubectl taint nodes <node-name> node-role.kubernetes.io/not-schedulable=:NoSchedule
   ```

   This taint will prevent new pods from being scheduled on the specified node.

### Step 4: Deploy the Busybox Pod Again

1. To deploy the Busybox pod again, create a new deployment YAML file (`busybox-deployment-2.yaml`) without node affinity since scheduling will be controlled by the taint:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: busybox-deployment-2
   spec:
     replicas: 1
     template:
       metadata:
         labels:
           app: busybox
       spec:
         containers:
         - name: busybox
           image: busybox
           command:
           - sleep
           - "3600"
   ```

   Apply the deployment:

   ```bash
   kubectl apply -f busybox-deployment-2.yaml
   ```

### Step 5: Check Pod States and Logs

1. Check the state of the pods to ensure that the new Busybox pod is running:

   ```bash
   kubectl get pods
   ```

   You should see the `busybox-deployment-2` pod in the "Running" state.

2. To check the logs of the pod, use `kubectl logs`:

   ```bash
   kubectl logs <pod-name>
   ```

   Replace `<pod-name>` with the name of the `busybox-deployment-2` pod. This will display the log output from the pod.

You have now completed the exercise, which involved creating a Busybox

 deployment on a specific node, deleting the deployment, disabling scheduling on the node, deploying again, and checking pod states and logs.

---

## Initiate a Rolling Update on a Deployment

### Step 1: Create a Deployment with 4 Pods

Before initiating a rolling update, you need to have a deployment with 4 pods running. You can create a sample deployment using the following YAML file (`sample-deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-deployment
spec:
  replicas: 4
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: sample-container
        image: nginx:latest
```

Apply this deployment using the command:

```bash
kubectl apply -f sample-deployment.yaml
```

### Step 2: Initiate a Rolling Update with maxSurge and maxUnavailable

To initiate a rolling update with specific settings, use the `kubectl set image` command. In this case, we will update the image to trigger the rolling update and specify `maxSurge` and `maxUnavailable` parameters:

```bash
kubectl set image deployment/sample-deployment sample-container=nginx:1.17 --record=true --max-surge=25% --max-unavailable=1
```

- `--record=true` is used to record this change in the revision history.
- `--max-surge=25%` allows 25% more pods to be created above the desired count during the update.
- `--max-unavailable=1` specifies that at most 1 pod can be unavailable during the update.

### Step 3: Describe the Deployment

Now, describe the deployment to see detailed information about the update process:

```bash
kubectl describe deployment sample-deployment
```

When you run the `kubectl describe deployment` command, you will see detailed information about the deployment, including the number of desired replicas, current replicas, and various conditions. Here's what you might see:

- **Replicas**: Information about the desired number of replicas and the actual number of replicas, including the updated pods.

- **Conditions**: The status of the deployment, such as "Progressing" or "Available."

- **Events**: Events related to the rolling update, including when pods are being created, deleted, or updated.

- **Rollout History**: If you used the `--record=true` flag when updating the deployment, a history of revisions with their associated images and other details.

- **Strategy**: Details about the rolling update strategy, including the `maxSurge` and `maxUnavailable` values.

By examining the output of `kubectl describe deployment`, you can monitor the progress of the rolling update, check for any issues, and see how many new pods are being created while ensuring the old ones are gracefully replaced, according to the specified `maxSurge` and `maxUnavailable` values.

---

## Rollback a Deployment Update

### Step 1: Determine the Revision to Roll Back To

Before rolling back the update, identify the revision number to which you want to revert. List the revision history of the deployment:

```bash
kubectl rollout history deployment/sample-deployment
```

This command displays a list of revisions, including their revision numbers and details about the changes made in each revision. Note the revision number you want to roll back to.

### Step 2: Initiate the Rollback

To initiate the rollback, use the `kubectl rollout undo` command and specify the desired revision number. Replace `<revision-number>` with the revision number you noted in the previous step:

```bash
kubectl rollout undo deployment/sample-deployment --to-revision=<revision-number>
```

For example:

```bash
kubectl rollout undo deployment/sample-deployment --to-revision=2
```

This command triggers the rollback to the specified revision, and Kubernetes begins reverting to the previous configuration.

### Step 3: Monitor the Rollback

Monitor the status of the rollback by describing the deployment:

```bash
kubectl describe deployment/sample-deployment
```

The output provides information about the rollback progress, including events related to the rollback process. Observe the status until the deployment has rolled back to the desired revision.

### Step 4: Verify the Rollback

After the rollback is complete, verify that the deployment has reverted to the previous state by checking the pod status:

```bash
kubectl get pods
```

You should see the pods running the previous version of your application.

By following these steps, you can successfully rollback a deployment update in Kubernetes to a specific revision, ensuring you can quickly recover from issues that may arise during updates or deployments.

---

## Create a Filebeat DaemonSet

### Step 1: Create a Filebeat DaemonSet

Create a Filebeat DaemonSet using a YAML configuration file. Below is an example of a Filebeat DaemonSet configuration (`filebeat-daemonset.yaml`):

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: filebeat
spec:
  selector:
    matchLabels:
      app: filebeat
  template:
    metadata:
      labels:
        app: filebeat
    spec:
      containers:
      - name: filebeat
        image: docker.elastic.co/beats/filebeat:7.15.1
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 100Mi
        volumeMounts:
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

This YAML creates a DaemonSet named "filebeat" that deploys Filebeat as a sidecar container to collect logs from other pods.

Apply the DaemonSet to create the Filebeat pods:

```bash
kubectl apply -f filebeat-daemonset.yaml
```

### Step 2: Check Which Nodes the Filebeat Pods Were Deployed On

To check which nodes the Filebeat pods were deployed on, use the `kubectl get pods -o wide` command with the `--selector` flag to filter the pods by the "app" label you specified for Filebeat. For example:

```bash
kubectl get pods -o wide --selector=app=filebeat
```

This command displays a list of Filebeat pods along with their associated nodes, allowing you to see which nodes have Filebeat pods deployed.

By using DaemonSets, Filebeat ensures that there is one pod running on each node in your Kubernetes cluster, making it easy to collect logs from every node.

---

## Use an NFS Server as a PV

### Step 1: Set Up an NFS Server

1. Set up an NFS server on a machine or server of your choice. The steps for setting up an NFS server depend on your operating system. Ensure that the NFS server exports a directory that you want to use for sharing files.

2. Share a directory using NFS.

 For example, export the directory `/nfs_share` by adding an entry to your NFS server's configuration (e.g., `/etc/exports` on Linux).

3. Start or restart the NFS server to apply the changes.

### Step 2: Create an Nginx Config File

1. Create a basic Nginx configuration file. For example, create a file named `nginx-config.conf` with your desired Nginx configuration.

   ```nginx
   server {
       listen 80;
       server_name localhost;

       location / {
           root /usr/share/nginx/html;
           index index.html;
       }
   }
   ```

   This configuration sets up a basic Nginx server that listens on port 80 and serves content from the `/usr/share/nginx/html` directory.

2. Save this configuration file to a location on your local machine.

### Step 3: Set Up Kubernetes Resources for NFS

1. Create a PersistentVolume (PV) that represents the NFS shared directory. Create a YAML file named `nfs-pv.yaml` with the following content:

   ```yaml
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: nfs-pv
   spec:
     capacity:
       storage: 1Gi
     accessModes:
       - ReadWriteMany
     nfs:
       server: <nfs-server-ip>
       path: /nfs_share  # Replace with the actual NFS path
   ```

   Replace `<nfs-server-ip>` with the IP address or hostname of your NFS server.

2. Create a PersistentVolumeClaim (PVC) to request storage from the PV. Create a YAML file named `nfs-pvc.yaml` with the following content:

   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: nfs-pvc
   spec:
     accessModes:
       - ReadWriteMany
     resources:
       requests:
         storage: 1Gi
   ```

### Step 4: Deploy Nginx with Mounted NFS Volume

1. Create an Nginx deployment YAML file (`nginx-deployment.yaml`) that mounts the NFS PVC and the config file:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deployment
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: nginx
     template:
       metadata:
         labels:
           app: nginx
       spec:
         volumes:
           - name: nginx-config-volume
             persistentVolumeClaim:
               claimName: nfs-pvc
           - name: nginx-config
             configMap:
               name: nginx-config
         containers:
           - name: nginx-container
             image: nginx:latest
             volumeMounts:
               - name: nginx-config-volume
                 mountPath: /etc/nginx/conf.d
               - name: nginx-config
                 mountPath: /usr/share/nginx/html/nginx-config.conf
                 subPath: nginx-config.conf
   ```

   In this example, we mount the NFS PVC as `/etc/nginx/conf.d` and the Nginx config file as `/usr/share/nginx/html/nginx-config.conf`.

2. Create a ConfigMap for the Nginx configuration:

   ```bash
   kubectl create configmap nginx-config --from-file=nginx-config.conf=<path-to-nginx-config.conf>
   ```

   Replace `<path-to-nginx-config.conf>` with the path to your local Nginx config file.

3. Deploy the Nginx deployment:

   ```bash
   kubectl apply -f nginx-deployment.yaml
   ```

Now, you have an Nginx deployment running with the NFS volume mounted. The Nginx configuration file is stored in the shared NFS folder and used by the Nginx container. The Nginx service is accessible via the Kubernetes service.

---

## Advanced Exercise: Use a Colleague's NFS Server as a PV

### Step 1: Coordinate with Your Colleague

1. Obtain the following details from your colleague:
   - NFS server IP address or hostname
   - NFS export path (the shared directory)
   - NFS server export options (if any, e.g., read/write permissions)

2. Request the necessary access permissions or credentials from your colleague to mount the NFS share from your Kubernetes cluster.

### Step 2: Create Kubernetes Resources

Once you have the NFS server details and access credentials, you can create the necessary Kubernetes resources.

1. Create a Kubernetes Secret to store the NFS access credentials. Create a YAML file named `nfs-secret.yaml` with the following content:

   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: nfs-secret
   type: Opaque
   data:
     username: <base64-encoded-username>
     password: <base64-encoded-password>
   ```

   Replace `<base64-encoded-username>` and `<base64-encoded-password>` with the Base64-encoded NFS username and password. You can use the `echo -n '<username>' | base64` command to encode the username and password.

   Apply the secret:

   ```bash
   kubectl apply -f nfs-secret.yaml
   ```

2. Create a PersistentVolume (PV) that represents the NFS shared directory. Create a YAML file named `nfs-pv.yaml` with the following content:

   ```yaml
   apiVersion: v1
   kind: PersistentVolume
   metadata:
     name: nfs-pv
   spec:
     capacity:
       storage: 1Gi
     accessModes:
       - ReadWriteMany
     nfs:
       server: <nfs-server-ip>
       path: /nfs_share  # Replace with the actual NFS path
     mountOptions:
       - nfsvers=4.1
       - noatime
       - nodiratime
     persistentVolumeReclaimPolicy: Retain
     volumeMode: Filesystem
     accessModes:
       - ReadWriteMany
     storageClassName: nfs-storage
     securityContext:
       runAsUser: 1000  # Use an appropriate UID that has access to the NFS share
   ```

   Replace `<nfs-server-ip>` with the IP address or hostname of your colleague's NFS server.

3. Create a PersistentVolumeClaim (PVC) to request storage from the PV. Create a YAML file named `nfs-pvc.yaml` with the following content:

   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: nfs-pvc
   spec:
     accessModes:
       - ReadWriteMany
     resources:
       requests:
         storage: 1Gi
   ```

4. Create a pod or deployment YAML file that uses the PVC as a volume mount for your application.

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: nfs-app-pod
   spec:
     containers:
       - name: app-container
         image: your-app-image
         volumeMounts:
           - name: nfs-volume
             mountPath: /path/to/mount
     volumes:
       - name: nfs-volume
         persistentVolumeClaim:
           claimName: nfs-pvc
   ```

   Replace `your-app-image` with the image of your application, and specify the mount path accordingly.

### Step 3: Deploy the Application

1. Deploy your application using the pod or deployment YAML file you created in the previous step:

   ```bash
   kubectl apply -f your-app-pod.yaml
   ```

2. Verify that your application pod is running:

   ```bash
   kubectl get pods
   ```

3. Check the logs or access the application to confirm that it can read and write data to the NFS volume.

With this setup, you have successfully used your colleague's NFS server as a PersistentVolume in your Kubernetes cluster. Your application can now interact with the shared NFS storage as needed. Ensure that you handle the NFS access credentials securely, as they are stored in a Kubernetes Secret.
