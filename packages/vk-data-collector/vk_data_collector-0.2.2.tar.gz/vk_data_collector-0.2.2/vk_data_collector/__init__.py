from src.client.client import Client
from src.collector.collector import Collector
from src.service.service import Service

__version__ = "0.1.0"


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
