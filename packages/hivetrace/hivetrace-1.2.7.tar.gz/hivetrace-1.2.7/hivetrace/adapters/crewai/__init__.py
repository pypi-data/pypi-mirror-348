"""
CrewAI adapter package.
"""

from hivetrace.adapters.crewai.adapter import CrewAIAdapter
from hivetrace.adapters.crewai.decorators import track_crew

__all__ = ["CrewAIAdapter", "track_crew"]
