from gbatchkit.types import (
    ComputeConfig,
    NetworkInterfaceConfig,
    ServiceAccountConfig,
    Runnable,
    ContainerRunnable,
)


def create_standard_job(
    region: str,
    compute_config: ComputeConfig,
    task_count: int,
    runnables: list[Runnable],
    parallelism: int = 1,
    task_count_per_node: int = 1,
    tmp_dir: str = None,
    tmp_dir_size_gb: int = None,
    network_interface: NetworkInterfaceConfig = None,
    service_account: ServiceAccountConfig = None,
    depends_on_job_ids: list[str] = None,
) -> dict:
    job = create_job_base(
        task_count, task_count_per_node=task_count_per_node, parallelism=parallelism
    )
    for runnable in runnables:
        add_runnable(job, runnable)

    apply_allocation_policy(job, region, compute_config)
    apply_cloud_log_policy(job)

    if tmp_dir:
        add_tmp_dir(job, tmp_dir, tmp_dir_size_gb)

    if network_interface:
        add_networking_interface(job, network_interface)

    if service_account:
        add_service_account(job, service_account)

    if depends_on_job_ids:
        add_job_dependencies(job, depends_on_job_ids)

    return job


def create_job_base(
    task_count: int,
    task_count_per_node: int,
    parallelism: int,
    preemption_retry_count: int = 3,
) -> dict:
    parallelism = parallelism or 1
    return {
        "taskGroups": [
            {
                "taskSpec": {
                    "runnables": [],
                    "maxRetryCount": preemption_retry_count,
                    "lifecyclePolicies": [
                        {
                            "action": "RETRY_TASK",
                            "actionCondition": {"exitCodes": [50001]},
                        }
                    ],
                },
                "taskCount": task_count,
                "taskCountPerNode": task_count_per_node,
                "parallelism": parallelism,
            }
        ]
    }


def add_runnable(job: dict, runnable: Runnable) -> None:
    """
    Add a runnable to the job definition.
    """
    runnables = job["taskGroups"][0]["taskSpec"].setdefault("runnables", [])

    if isinstance(runnable, ContainerRunnable):
        runnables.append({"container": runnable.model_dump()})
    else:
        raise TypeError("Unsupported runnable type: {}".format(type(runnable)))


def apply_allocation_policy(
    job: dict,
    region: str,
    compute_config: ComputeConfig,
) -> None:
    """
    Apply an allocation policy to the job definition: machine type, provisioning model, and GPU.
    """
    if (compute_config.accelerator_type and not compute_config.accelerator_count) or (
        compute_config.accelerator_count and not compute_config.accelerator_type
    ):
        raise ValueError("GPU type and GPU count must be set together")
    if compute_config.provisioning_model not in ["SPOT", "STANDARD"]:
        raise ValueError("Provisioning model must be either SPOT or STANDARD")

    job["allocationPolicy"] = {
        "instances": [
            {
                "policy": {
                    "machineType": compute_config.machine_type,
                    "provisioningModel": compute_config.provisioning_model,
                },
            }
        ],
        "location": {"allowedLocations": [f"regions/{region}"]},
    }

    if compute_config.accelerator_type:
        job["allocationPolicy"]["instances"][0]["installGpuDrivers"] = True
        job["allocationPolicy"]["instances"][0]["policy"]["accelerators"] = [
            {
                "type": compute_config.accelerator_type,
                "count": compute_config.accelerator_count,
            }
        ]


def apply_cloud_log_policy(job: dict) -> None:
    """
    Apply a cloud logging policy to the job definition.
    """
    job["logsPolicy"] = {
        "destination": "CLOUD_LOGGING",
    }


def add_tmp_dir(
    job: dict,
    tmp_dir: str,
    tmp_dir_size_gb: int,
) -> None:
    """
    Add a temporary directory to the job definition.
    """
    volume_name = "job-workspace"
    add_attached_disk(job, volume_name, tmp_dir_size_gb)
    add_job_storage_volume(job, tmp_dir, volume_name)
    set_job_environment_variable(job, "TMPDIR", tmp_dir)


def add_attached_disk(
    job: dict,
    device_name: str,
    size_gb: int,
    disk_type: str = "pd-balanced",
) -> None:
    """
    Set the boot disk size for the job definition.
    """
    disks = job["allocationPolicy"]["instances"][0]["policy"].setdefault("disks", [])
    disks.append(
        {
            "deviceName": device_name,
            "newDisk": {
                "type": disk_type,
                "sizeGb": max(size_gb, 1),
            },
        }
    )


def add_job_storage_volume(job: dict, tmp_dir: str, volume_name: str):
    """
    Add a volume to the job definition.
    """
    volumes = job["taskGroups"][0]["taskSpec"].setdefault("volumes", [])
    volumes.append(
        {
            "mountPath": tmp_dir,
            "deviceName": volume_name,
        }
    )
    pass


def set_job_environment_variable(
    job: dict,
    key: str,
    value: str,
) -> None:
    """
    Set an environment variable for the task in the job definition.
    """
    env = job["taskGroups"][0]["taskSpec"].setdefault("environment", {})
    env_vars = env.setdefault("variables", {})
    env_vars[key] = value


def add_networking_interface(job: dict, networking_interface: NetworkInterfaceConfig):
    network_interfaces = (
        job["allocationPolicy"]
        .setdefault("network", {})
        .setdefault("networkInterfaces", [])
    )
    network_interfaces.append(networking_interface.model_dump())


def add_service_account(job: dict, service_account: ServiceAccountConfig):
    job["allocationPolicy"]["serviceAccount"] = service_account.model_dump()


def add_job_dependencies(job: dict, job_ids: list[str]):
    """
    Add job dependencies to the job definition.
    """
    job_ids = filter(None, job_ids)
    if not job_ids:
        return

    dependencies = job.setdefault("dependencies", [{"items": {}}])[0]
    for job_id in job_ids:
        dependencies["items"][job_id] = "SUCCEEDED"
