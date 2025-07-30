import os
from pathlib import Path
from typing import Dict, List, Optional

from docker import DockerClient
from docker.models.networks import Network
from docker.models.containers import Container
from docker.errors import ImageNotFound, APIError, NotFound

from vlem.helper import read_json, read_data_from_api
from vlem.constants import LABS_URL, CONTAINER_IDENTIFIER
from vlem.error import LabNotFoundError


def format_ports(ports: List[str]) -> Dict[int, int]:
    port_bindings = {}
    for p in ports:
        host_port, container_port = p.split(":")
        port_bindings[container_port] = int(host_port)
    return port_bindings


def fetch_lab_environment(name: str) -> Dict:
    if os.getenv("DEBUG", None):
        labs: List[Dict] = read_json(Path("./data/labs.json"))

        lab = next((lab for lab in labs if lab.get("name") == name), None)
        if not lab:
            raise LabNotFoundError(name)

        return lab
    else:
        return read_data_from_api(url=LABS_URL)


def image_available(client: DockerClient, image_name: str) -> bool:
    try:
        client.images.get(image_name)
        return True
    except ImageNotFound:
        return False
    except APIError as e:
        return False


def pull_image(client: DockerClient, image: str) -> List:
    return client.api.pull(image, stream=True, decode=True)


def list_containers(client: DockerClient) -> list[Container]:
    """
    Lists Docker containers with a specific label.

    Args:
        client: The Docker client object.

    Returns:
        A list of Docker container objects that have the specified label.
    """
    return client.containers.list(
        all=True, filters={"label": f"id={CONTAINER_IDENTIFIER}"}
    )


def fetch_container(client: DockerClient, container_name: str):
    try:
        return client.containers.get(container_name)
    except NotFound:
        return None


def remove_container(client: DockerClient, force: bool = True) -> None:
    client.remove(force=force)
    return


def stop_container(client: DockerClient) -> None:
    client.stop()
    return


def create_network(client: DockerClient, network_name: str) -> Network:
    """
    Creates a Docker network.

    Args:
        client: The Docker client object.
        network_name: The name of the network to create.

    Returns:
        The created Docker network object.

    Raises:
        docker.errors.APIError: If an error occurs during network creation.
    """
    try:
        # Check if the network already exists
        if client.networks.list(names=[network_name]):
            print(f"Network '{network_name}' already exists.")
            return client.networks.get(network_name)  # Return the existing network

        network: Network = client.networks.create(
            name=network_name,
            driver="bridge",
        )
        print(f"Network '{network_name}' created with ID: {network.id}")
        return network
    except APIError as e:
        raise APIError(f"Error creating network '{network_name}': {e}")


def fetch_network(client: DockerClient, network_name: str) -> Optional[Network]:
    """
    Fetches an existing Docker network.

    Args:
        client: The Docker client object.
        network_name: The name of the network to fetch.

    Returns:
        The Docker network object if found, None otherwise.
    """
    try:
        network: Network = client.networks.get(network_name)
        print(f"Network '{network_name}' found with ID: {network.id}")
        return network
    except NotFound:
        print(f"Network '{network_name}' not found.")
        return None


def create_container(
    client: DockerClient,
    image_name: str,
    container_name: str,
    network_name: str,
    restart_policy: str = "no",  # Added default value
    environment_variables: Optional[Dict[str, str]] = None,
    ports: Optional[Dict[int, int]] = None,
    volumes: Optional[Dict[str, Dict]] = None,
) -> Container:
    """
    Creates a Docker container with network configuration and other options.

    Args:
        client: The Docker client object.
        image_name: The name of the Docker image to use.
        container_name: The name of the container.
        network_name: The name of the Docker network to connect to.
        restart_policy: The restart policy for the container (e.g., "always", "on-failure", "no").
            Defaults to "no".
        environment_variables: A dictionary of environment variables to set in the container.
            Defaults to None.
        ports: A dictionary mapping container ports to host ports. Defaults to None.
        volumes: A dictionary mapping host file/folder locations to container mounts.
            Defaults to None.

    Returns:
        The created Docker container object.

    Raises:
        docker.errors.APIError: If an error occurs during container creation.
        ValueError: If the network name is invalid.
    """

    container_config = {
        "image": image_name,
        "name": container_name,
        "environment": environment_variables,
        "labels": {"id": CONTAINER_IDENTIFIER},
        "network": network_name,
        "restart_policy": {"name": restart_policy},
        "ports": ports,
        "volumes": volumes,
        "detach": False,
    }

    try:
        container: Container = client.containers.create(**container_config)
        print(
            f"Container '{container_name}' created from image '{image_name}' and connected to network '{network_name}'"
        )
        return container
    except APIError as e:
        raise APIError(f"Error creating container '{container_name}': {e}")
