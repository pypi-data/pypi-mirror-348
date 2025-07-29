"""
Reward Kit Agent Evaluation Framework V2 Components.

This package contains the core components for the new, resource-centric
agent evaluation framework, including the ForkableResource ABC, Orchestrator,
and concrete resource implementations.
"""

# Make key components easily importable from reward_kit.agent
from .resource_abc import ForkableResource
from .orchestrator import Orchestrator
from .resources import (
    PythonStateResource,
    SQLResource,
    FileSystemResource,
    DockerResource,
)

__all__ = [
    "ForkableResource",
    "Orchestrator",
    "PythonStateResource",
    "SQLResource",
    "FileSystemResource",
    "DockerResource",
]
