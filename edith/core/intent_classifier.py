"""Intent classification for EDITH."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class IntentType(str, Enum):
    COMMUNICATION = "communication"
    PROFESSIONAL_PRESENCE = "professional_presence"
    DEVELOPER = "developer"
    LIVE_SEARCH = "live_search"
    DOCUMENT = "document"
    WEB_NAVIGATION = "web_navigation"
    CHAT = "chat"


@dataclass
class IntentResult:
    intent: IntentType
    confidence: float


class IntentClassifier:
    """Classify user intent into EDITH capability buckets."""

    def classify(self, message: str) -> IntentResult:
        lowered = message.lower()
        if any(keyword in lowered for keyword in ["gmail", "email", "inbox"]):
            return IntentResult(IntentType.COMMUNICATION, 0.85)
        if any(keyword in lowered for keyword in ["linkedin", "post"]):
            return IntentResult(IntentType.PROFESSIONAL_PRESENCE, 0.82)
        if any(keyword in lowered for keyword in ["github", "repo", "repository"]):
            return IntentResult(IntentType.DEVELOPER, 0.8)
        if any(keyword in lowered for keyword in ["latest", "today", "news", "price", "now"]):
            return IntentResult(IntentType.LIVE_SEARCH, 0.78)
        if any(keyword in lowered for keyword in ["pdf", "docx", "spreadsheet", "document"]):
            return IntentResult(IntentType.DOCUMENT, 0.76)
        if any(keyword in lowered for keyword in ["browser", "open", "navigate", "website"]):
            return IntentResult(IntentType.WEB_NAVIGATION, 0.75)
        return IntentResult(IntentType.CHAT, 0.6)
