from pydantic import BaseModel, Field


class ComputeConfig(BaseModel):
    machine_type: str = Field(
        default="n1-standard-1",
        title="Machine Type",
        description="The machine type to use for the job.",
    )
    provisioning_model: str = Field(
        default="SPOT",
        title="Provisioning Model",
        description="The provisioning model to use for the job.",
    )
    accelerator_count: int = Field(
        default=0,
        title="Accelerator Count",
        description="The number of accelerators to use for the job.",
    )
    accelerator_type: str = Field(
        default="",
        title="Accelerator Type",
        description="The type of accelerator to use for the job.",
    )


class NetworkInterfaceConfig(BaseModel):
    network: str = Field(
        default="",
        title="Network",
        description="The network to use for the job.",
    )
    subnetwork: str = Field(
        default="",
        title="Subnetwork",
        description="The subnetwork to use for the job.",
    )
    no_external_ip_address: bool = Field(
        default=False,
        title="No External IP Address",
        description="True if there is no external IP address on the VM.",
    )


class ServiceAccountConfig(BaseModel):
    email: str = Field(
        default="",
        title="Service Account Email",
        description="The email of the service account to use for the job.",
    )
    scopes: list[str] = Field(
        default_factory=list,
        title="Service Account Scopes",
        description="The scopes to use for the service account.",
    )


class Runnable(BaseModel):
    pass


class ContainerRunnable(Runnable):
    image_uri: str = Field(
        title="Container Image URI",
        description="The URI of the container image to use for the job.",
    )
    entrypoint: str = Field(
        title="Entrypoint",
        description="The entrypoint to use for the container.",
    )
    commands: list[str] = Field(
        title="Commands",
        description="The command arguments.",
    )