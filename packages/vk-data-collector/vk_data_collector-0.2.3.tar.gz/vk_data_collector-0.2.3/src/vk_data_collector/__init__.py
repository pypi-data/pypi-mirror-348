from vk_data_collector.client.client import Client
from vk_data_collector.collector.collector import Collector
from vk_data_collector.service.service import Service

__version__ = "0.2.3"


def create_collector(token: str) -> Collector:
    """
    Create and initialize a new Collector instance with all required dependencies.
    This is the main entry point for the library.

    Args:
        token: VK API service token

    Returns:
        Collector: A fully initialized collector instance ready to use
    """
    client = Client(token)
    service = Service(client)
    return Collector(service)


# Expose main classes for advanced usage if needed
__all__ = ["create_collector", "Collector", "Service", "Client"]
