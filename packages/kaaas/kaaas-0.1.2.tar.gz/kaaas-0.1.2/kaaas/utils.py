import subprocess
import logging

logger = logging.getLogger('KAAS')

# Get events for a resource (Pod, Deployment, Service, ReplicaSet, ConfigMap, etc.)
def get_resource_events(resource_type, namespace, name):
    try:
        result = subprocess.run(
            f"kubectl describe {resource_type.lower()} {name} -n {namespace}",
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get events for {resource_type} {name} in {namespace}: {e.stderr}")
        return f"Error: {e.stderr}"
