"""
Model-specific services for the shoebill_ai package.

This package contains service classes for specific LLM models.
"""

__all__ = ['GraniteService', 'NomicService', 'BaseModelService']

from .granite_service import GraniteService
from .nomic_service import NomicService
from .base_model_service import BaseModelService
