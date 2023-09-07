import os

from ci.ray_ci.container import Container, _DOCKER_ECR_REPO
from ci.ray_ci.builder_container import PYTHON_VERSIONS
from ci.ray_ci.utils import docker_pull


class DockerContainer(Container):
    def __init__(self, python_version: str) -> None:
        super().__init__(
            "forge",
            volumes=[
                f"{os.environ['RAYCI_CHECKOUT_DIR']}:/rayci",
                "/var/run/docker.sock:/var/run/docker.sock",
            ],
        )
        self.python_version = python_version

    def run(self) -> None:
        base_image = (
            f"{_DOCKER_ECR_REPO}:{os.environ['RAYCI_BUILD_ID']}-raypy38cu118base"
        )
        docker_pull(base_image)
        wheel_name = (
            "ray-3.0.0.dev0-"
            f"{PYTHON_VERSIONS[self.python_version]['bin_path']}-"
            "manylinux2014_x86_64.whl"
        )
        constraints_file = (
            "requirements_compiled_py37.txt"
            if self.python_version == "py37"
            else "requirements_compiled.txt"
        )
        ray_image = (
            "rayproject/ray:"
            f"{os.environ['BUILDKITE_COMMIT'][:6]}-"
            f"{self.python_version}-cu118"
        )
        self.run_script(
            [
                "./ci/build/build-ray-docker.sh "
                f"{wheel_name} {base_image} {constraints_file} {ray_image}"
            ]
        )
