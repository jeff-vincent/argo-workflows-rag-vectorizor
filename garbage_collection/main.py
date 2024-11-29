import datetime
import os
from kubernetes import client, config

# Load Kubernetes configuration
if "KUBERNETES_SERVICE_HOST" in os.environ:
    config.load_incluster_config()
else:
    config.load_kube_config()
# Define the namespace and age threshold
NAMESPACE = "default"  # Replace with your target namespace
AGE_THRESHOLD_DAYS = 1  # ConfigMaps older than this will be deleted

# Get current time
now = datetime.datetime.now(datetime.timezone.utc)

# Initialize Kubernetes API client
v1 = client.CoreV1Api()

def delete_old_configmaps():
    print(f"Scanning ConfigMaps in namespace: {NAMESPACE}")
    try:
        # List all ConfigMaps in the namespace
        configmaps = v1.list_namespaced_config_map(namespace=NAMESPACE)
        for cm in configmaps.items:
            # Get the creation timestamp of the ConfigMap
            creation_timestamp = cm.metadata.creation_timestamp

            # Calculate the age of the ConfigMap
            age = (now - creation_timestamp).days

            if age > AGE_THRESHOLD_DAYS:
                print(f"Deleting ConfigMap: {cm.metadata.name} (Age: {age} days)")
                v1.delete_namespaced_config_map(
                    name=cm.metadata.name,
                    namespace=NAMESPACE
                )
            else:
                print(f"Skipping ConfigMap: {cm.metadata.name} (Age: {age} days)")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    delete_old_configmaps()
