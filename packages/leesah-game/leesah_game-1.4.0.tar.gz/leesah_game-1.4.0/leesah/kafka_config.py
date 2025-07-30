"""Create configuration for Kafka clients."""


def base_config(creds: dict) -> dict:
    """Create a base configuration for Kafka clients."""
    broker = creds["broker"]
    if ":" not in broker:
        broker += ":26484"

    return {
        "bootstrap.servers": broker,
        "security.protocol": "SSL",
        "ssl.ca.pem": creds["ca"],
        "ssl.key.pem": creds["user"]["access_key"],
        "ssl.certificate.pem": creds["user"]["access_cert"],
    }


def consumer_config(creds: dict, group_id: str, auto_commit: bool):
    """Create a configuration for Kafka consumers."""
    config = base_config(creds)
    return config | {
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": str(auto_commit),
    }


def producer_config(creds: dict) -> dict:
    """Create a configuration for Kafka producers."""
    return base_config(creds) | {"broker.address.family": "v4"}
