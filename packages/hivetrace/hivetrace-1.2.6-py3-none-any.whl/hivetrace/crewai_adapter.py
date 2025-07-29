"""
HiveTrace CrewAI integration.

This module provides integration between CrewAI and HiveTrace for monitoring agents.
"""

from hivetrace.adapters import CrewAIAdapter, track_crew

__all__ = ["CrewAIAdapter", "track_crew"]
