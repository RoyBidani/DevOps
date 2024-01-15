

1. **Commands and Arguments**:
   - **Commands**: Specifies the command to be executed when a container starts. It overrides the default command specified in the container image.
   - **Arguments**: Allows you to provide additional arguments to the command defined in the container image.

   Example:
   ```yaml
   spec:
     containers:
       - name: my-container
         image: my-image
         command: ["echo"]
         args: ["Hello, Kubernetes!"]
   ```

2. **Environment variables**:
   - Environment variables are key-value pairs that can be injected into a container. They are often used to configure and parameterize containerized applications.

   Example:
   ```yaml
   spec:
     containers:
       - name: my-container
         image: my-image
         env:
           - name: DATABASE_URL
             value: "mongodb://mydbserver:27017/mydb"
   ```

3. **Secrets**:
   - Secrets are Kubernetes resources used to store sensitive information, such as API keys or passwords, securely. They can be mounted as files or exposed as environment variables in containers.

   Example:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: my-secret
   data:
     username: <base64-encoded-username>
     password: <base64-encoded-password>
   ```

4. **Configmaps**:
   - ConfigMaps are Kubernetes resources that store configuration data in key-value pairs. They can be used to configure containers and decouple configuration from application code.

   Example:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: my-config
   data:
     config.ini: |
       [database]
       host = dbserver
       port = 5432
   ```

5. **Labels**:
   - Labels are key-value pairs attached to Kubernetes resources (e.g., pods, services) to provide metadata and enable grouping or filtering of resources.

   Example:
   ```yaml
   metadata:
     labels:
       app: my-app
       environment: production
   ```

6. **Selectors**:
   - Selectors are used to filter and select resources with specific labels. For example, when defining a service, you can use selectors to target pods with specific labels.

   Example:
   ```yaml
   spec:
     selector:
       matchLabels:
         app: my-app
     ports:
       - protocol: TCP
         port: 80
   ```

7. **Node Selectors**:
   - Node selectors are used to schedule pods onto nodes based on labels assigned to nodes. This allows you to control pod placement.

   Example:
   ```yaml
   spec:
     nodeSelector:
       disk: ssd
   ```

8. **Node Affinity**:
   - Node affinity rules allow you to constrain pod placement based on node attributes, such as node labels or node affinity rules.

   Example:
   ```yaml
   spec:
     affinity:
       nodeAffinity:
         requiredDuringSchedulingIgnoredDuringExecution:
           nodeSelectorTerms:
             - matchExpressions:
               - key: disktype
                 operator: In
                 values:
                   - ssd
   ```

9. **Taints**:
   - Taints are used to repel pods from nodes unless the pod has a corresponding toleration. Taints are typically used for node-specific conditions.

   Example:
   ```yaml
   spec:
     tolerations:
       - key: "app"
         operator: "Equal"
         value: "my-app"
         effect: "NoSchedule"
   ```

10. **Tolerations**:
    - Tolerations are pod-specific rules that allow pods to tolerate node taints.

   Example:
   ```yaml
   spec:
     tolerations:
       - key: "disktype"
         operator: "Equal"
         value: "ssd"
         effect: "NoSchedule"
   ```

11. **Rolling Updates and Rollbacks**:
    - Rolling updates are a strategy for updating deployments with minimal disruption. Kubernetes gradually replaces old pods with new ones.
    - Rollbacks allow you to revert to a previous version of a deployment if issues arise.

12. **Init Containers**:
    - Init containers are containers that run before the main containers in a pod. They are typically used for setup tasks, such as database schema initialization.

   Example:
   ```yaml
   spec:
     initContainers:
       - name: setup
         image: setup-image
   ```

13. **DaemonSets**:
    - DaemonSets ensure that a specific pod runs on every node in a cluster. They are often used for system-level tasks like monitoring or logging.

   Example:
   ```yaml
   apiVersion: apps/v1
   kind: DaemonSet
   metadata:
     name: my-daemonset
   ```

14. **PV (Persistent Volume)**:
    - A Persistent Volume is a storage resource in a cluster that can be dynamically provisioned or statically allocated to pods. It provides durable storage for applications.

15. **PVC (Persistent Volume Claim)**:
    - A Persistent Volume Claim is a request for storage by a pod. It binds to a Persistent Volume and allows pods to use the storage.

   Example:
   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: my-claim
   ```

16. **Storage Class**:
    - A Storage Class is a way to define storage provisioning in a cluster. It specifies how PVs are dynamically provisioned and what type of storage is used.

   Example:
   ```yaml
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: fast
   provisioner: my-storage-provisioner
   parameters:
     type: ssd
   ```

These keywords and concepts are essential for working with containers and Kubernetes, as they enable you to manage and orchestrate containerized applications effectively in a Kubernetes cluster.
