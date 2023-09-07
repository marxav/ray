import os

from ci.ray_ci.container import Container, _DOCKER_ECR_REPO
from ci.ray_ci.builder_container import PYTHON_VERSIONS
from ci.ray_ci.utils import docker_pull

PLATFORM = ["cu118"]


class DockerContainer(Container):
    def __init__(self, python_version: str, platform: str, image_type: str) -> None:
        super().__init__(
            "forge",
            volumes=[
                f"{os.environ['RAYCI_CHECKOUT_DIR']}:/rayci",
                "/var/run/docker.sock:/var/run/docker.sock",
            ],
        )
        self.python_version = python_version
        self.platform = platform
        self.image_type = image_type

    def run(self) -> None:
        base_image = (
            f"{_DOCKER_ECR_REPO}:{os.environ['RAYCI_BUILD_ID']}"
            f"-{self.image_type}{self.python_version}{self.platform}base"
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
            f"rayproject/{self.image_type}:{os.environ['BUILDKITE_COMMIT'][:6]}-"
            f"{self.python_version}-{self.platform}"
        )
        self.run_script(
            [
                "./ci/build/build-ray-docker.sh "
                f"{wheel_name} {base_image} {constraints_file} {ray_image}"
            ]
        )
