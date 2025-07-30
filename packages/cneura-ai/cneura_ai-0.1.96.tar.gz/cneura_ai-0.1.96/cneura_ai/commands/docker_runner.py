import docker
import json
import os
from docker.models.containers import Container
from typing import List, Dict, Optional, Union


class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.running_containers: Dict[str, Container] = {}

    def pull_image(self, image_name: str) -> None:
        print(f"Pulling image: {image_name}")
        self.client.images.pull(image_name)

    def build_image(self, dockerfile_path: str, tag: str) -> None:
        print(f"Building image from: {dockerfile_path} with tag: {tag}")
        self.client.images.build(path=dockerfile_path, tag=tag)

    def run_container(self, image: str, name: Optional[str] = None,
                      ports: Optional[Dict[str, int]] = None,
                      env: Optional[Dict[str, str]] = None,
                      detach: bool = True) -> Container:
        print(f"Running container: {name} from image: {image}")
        container = self.client.containers.run(
            image=image,
            name=name,
            ports=ports,
            environment=env,
            detach=detach
        )
        self.running_containers[container.id] = container
        return container

    def bulk_run_containers(self, image: str, count: int,
                            base_name: str = "bulk_container",
                            port_start: int = 8000,
                            ports: Optional[Dict[str, int]] = None,
                            env: Optional[Dict[str, str]] = None) -> List[Container]:
        print(f"Running {count} containers from image: {image}")
        containers = []
        for i in range(count):
            name = f"{base_name}_{i}"
            dynamic_ports = {}
            if ports:
                for idx, (container_port, host_port) in enumerate(ports.items()):
                    dynamic_ports[container_port] = port_start + i + idx
            container = self.run_container(image, name=name, ports=ports, env=env)
            containers.append(container)
        return containers

    def health_check(self, container_id: str) -> Optional[str]:
        container = self.running_containers.get(container_id)
        if container:
            container.reload()
            return container.attrs.get("State", {}).get("Health", {}).get("Status", "unknown")
        return None

    def list_running_containers(self) -> List[Dict]:
        self._refresh_running_containers()
        container_info = []
        for container in self.running_containers.values():
            ports = container.attrs['NetworkSettings']['Ports']
            exposed_ports = {k: [p['HostPort'] for p in v] if v else [] for k, v in ports.items()}
            container_info.append({
                "id": container.id[:12],
                "name": container.name,
                "status": container.status,
                "image": container.image.tags,
                "ports": exposed_ports
            })
        return container_info

    def get_logs(self, container_id: str, tail: int = 100) -> Optional[str]:
        container = self.running_containers.get(container_id)
        if container:
            return container.logs(tail=tail).decode("utf-8")
        return None

    def load_from_config(self, json_path: str, default_port_start: int = 8000) -> None:
        if not os.path.exists(json_path):
            print(f"Config file {json_path} not found.")
            return

        with open(json_path, 'r') as f:
            configs = json.load(f)

        port_counter = default_port_start

        for cfg in configs:
            name = cfg.get("name", "container")
            image = cfg.get("image")
            dockerfile_path = cfg.get("dockerfile_path")
            tag = cfg.get("tag", f"{name}_tag")
            ports = cfg.get("ports", {})
            env = cfg.get("env", {})
            count = cfg.get("count", 1)

            if dockerfile_path:
                self.build_image(dockerfile_path, tag)
                image = tag

            elif image:
                self.pull_image(image)

            print(f"Launching {count} instance(s) of {name}...")

            self.bulk_run_containers(
                image=image,
                count=count,
                base_name=name,
                port_start=port_counter,
                ports=ports,
                env=env
            )

            port_counter += count 

    def _refresh_running_containers(self):
        self.running_containers = {
            c.id: c for c in self.client.containers.list(all=True)
        }

    def stop_all(self):
        print("Stopping all running containers...")
        for container in self.running_containers.values():
            container.stop()
        self.running_containers.clear()


# # --- Example usage ---
# if __name__ == "__main__":
#     manager = DockerManager()
#     manager.load_from_config("containers_config.json")

#     print("\n--- Running Containers ---")
#     for info in manager.list_running_containers():
#         print(info)
