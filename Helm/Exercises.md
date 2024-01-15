### Exercise 1: Installation and Basic Usage


#### Step 1: Install Helm on your local machine.

- Depending on your operating system, you can install Helm using package managers like `apt`, `brew`, or by downloading and installing the binary manually. Here's an example of how to install Helm on a Linux-based system using `curl`:

```bash
# Download Helm binary
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3

# Make the script executable
chmod 700 get_helm.sh

# Run the script to install Helm
./get_helm.sh
```

- Verify the installation by running `helm version`. You should see the Helm client version displayed.

#### Step 2: Initialize Helm on your Kubernetes cluster (if not already done).

- Helm 3 does not require initialization with Tiller, unlike Helm 2. Simply ensure you have a working Kubernetes cluster that Helm can interact with.

- You can confirm that Helm can communicate with your cluster by running `helm list`. If you receive no errors and it shows an empty list of releases, Helm is configured correctly to interact with your cluster.

#### Step 3: Add a Helm chart repository using `helm repo add`.

- Helm chart repositories are sources from which you can install charts. You can add a repository using the `helm repo add` command. Replace `repository-name` with a name for the repository and `repository-url` with the actual URL of the repository.

```bash
helm repo add repository-name repository-url
```

For example, to add the official Helm stable charts repository:

```bash
helm repo add stable https://charts.helm.sh/stable
```

- Verify that the repository was added successfully by running `helm repo list`. You should see the newly added repository listed.

#### Step 4: Search for available charts in the repository using `helm search repo`.

- To search for available charts in the added repository, use the `helm search repo` command followed by a search query. For example:

```bash
helm search repo search-query
```

For example, to search for charts related to PostgreSQL:

```bash
helm search repo postgresql
```

- Helm will display a list of matching charts from the repository along with their names, versions, and descriptions.

#### Step 5: Install a Helm chart using `helm install`.

- To install a Helm chart, use the `helm install` command followed by a release name and the name of the chart you want to install. You can also specify a namespace and customize the chart's values by providing a `values.yaml` file.

For example, to install the PostgreSQL chart from the stable repository:

```bash
helm install my-postgresql stable/postgresql
```

This command installs the PostgreSQL chart with the release name `my-postgresql`. You can customize the installation by providing additional flags like `--namespace` or `--set` to configure specific values.

#### Step 6: Check the status of the deployed release using `helm status`.

- To check the status of the deployed release, use the `helm status` command followed by the release name.

For example, to check the status of the `my-postgresql` release:

```bash
helm status my-postgresql
```

- Helm will display detailed information about the release, including its status, resources, and notes (if any).

#### Step 7: List all installed releases using `helm list`.

- To list all installed releases on your Kubernetes cluster, use the `helm list` command.

```bash
helm list
```

- Helm will display a list of releases, including their names, namespaces, revision numbers, status, and more.



### Exercise 2: Chart Management

#### Step 8: Upgrade the installed release to a new version using `helm upgrade`.

- To upgrade the installed release to a new version, use the `helm upgrade` command followed by the release name and the name of the updated chart. You can also specify the path to the updated chart if it's not from a repository.

For example, to upgrade the `my-postgresql` release to a new version of the PostgreSQL chart:

```bash
helm upgrade my-postgresql stable/postgresql
```

This command will compare the existing release configuration with the new chart, apply any changes, and update the Kubernetes resources accordingly.

#### Step 9: Rollback the release to a previous version using `helm rollback`.

- If an upgrade results in issues or unexpected behavior, you can perform a rollback. To rollback a release to a previous version, use the `helm rollback` command followed by the release name and the revision number to which you want to roll back.

For example, to rollback the `my-postgresql` release to revision 2:

```bash
helm rollback my-postgresql 2
```

Helm will revert the release to the specified revision, restoring the application to a known good state.

#### Step 10: Uninstall a Helm release using `helm uninstall`.

- To uninstall a Helm release, use the `helm uninstall` command followed by the release name.

For example, to uninstall the `my-postgresql` release:

```bash
helm uninstall my-postgresql
```

This command will delete all resources associated with the release and remove it from your cluster.

#### Step 11: Check the release history using `helm history`.

- To view the revision history of a Helm release, use the `helm history` command followed by the release name.

For example, to view the history of the `my-postgresql` release:

```bash
helm history my-postgresql
```

Helm will display a list of all previous releases, including their revision numbers, timestamps, and any changes made to the release.


### Exercise 3: Chart Customization

#### Step 12: Create a custom Helm chart using `helm create`.

- To create a custom Helm chart, use the `helm create` command followed by the name of your chart. This will generate a directory structure for your chart with template files and a `values.yaml` file.

For example, to create a custom chart named `my-custom-chart`:

```bash
helm create my-custom-chart
```

This command will create a directory called `my-custom-chart` with the necessary files and directories for your chart.

#### Step 13: Customize values in the `values.yaml` file to modify the chart's behavior.

- Edit the `values.yaml` file in your custom chart directory to specify configuration values for your application. Customize the values to match your application's requirements.

For example, in `my-custom-chart/values.yaml`:

```yaml
myApp:
  enabled: true
  replicas: 3
  ...
```

You can set different configuration values as needed for your application.

#### Step 14: Package the custom Helm chart using `helm package`.

- To package your custom Helm chart into a `.tgz` file, use the `helm package` command in the directory containing your chart.

For example, if your chart is in the `my-custom-chart` directory:

```bash
helm package my-custom-chart
```

This command will create a `.tgz` file containing your chart and its dependencies.

#### Step 15: Install the custom Helm chart on your Kubernetes cluster.

- To install your custom Helm chart, use the `helm install` command followed by a release name and the path to the packaged chart `.tgz` file.

For example, to install the `my-custom-chart` with the release name `my-release`:

```bash
helm install my-release ./my-custom-chart-0.1.0.tgz
```

This command will deploy your custom application using the settings defined in the `values.yaml` file.

#### Step 16: Verify that the custom settings are applied.

- To verify that the custom settings in your chart's `values.yaml` file are applied, you can use various Helm commands like `helm status`, `helm get`, or `kubectl` commands to check the deployed resources and configurations.

For example, to check the status of your release:

```bash
helm status my-release
```

This will display detailed information about the deployed release, including the configuration values.


