"""
Models for the LinkedIn API client.
"""

from .ai import PromptInput, OutputJson, RelevanceInput, RelevanceOutput, UsageMetadata
from .user import User, UserBotSettings, UserCreateDTO, UserSearchSettings, Location, AIFilter, LinkedinFilters
from .vacancy import Vacancy
from .telegram import Notification

__all__ = [
    'PromptInput',
    'OutputJson',
    'RelevanceInput',
    'RelevanceOutput',
    'UsageMetadata',
    'User',
    'UserBotSettings',
    'UserCreateDTO',
    'UserSearchSettings',
    'Location',
    'AIFilter',
    'LinkedinFilters',
    'Vacancy',
    'Notification',
] 