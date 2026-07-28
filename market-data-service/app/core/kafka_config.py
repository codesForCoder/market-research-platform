from dataclasses import dataclass

from app.core.config import get_settings


@dataclass(frozen=True, slots=True)
class KafkaConfig:
    bootstrap_servers: str
    username: str
    password: str
    ca_cert_path: str
    security_protocol: str = "SASL_SSL"
    sasl_mechanism: str = "PLAIN"
    client_id: str = "market-research-platform"


kafka_config = KafkaConfig(
    bootstrap_servers=get_settings().kafka_bootstrap_servers,
    username=get_settings().kafka_username,
    password=get_settings().kafka_password,
    ca_cert_path=get_settings().kafka_ca_cert_path,
)