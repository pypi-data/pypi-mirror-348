from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Optional, Any
import datetime

# --- Severity Enum ---

class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    ERROR = "error"  # Useful for wrapping exceptions


# --- Insight Object ---

@dataclass
class Insight:
    id: str
    title: str
    description: str
    severity: Severity = Severity.INFO
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.UTC).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return f"[{self.severity.value.upper()}] {self.title} - {self.description}"


# --- Result Wrapper for Rules ---

@dataclass
class Result:
    rule: str
    success: bool
    insight: Optional[Insight] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.rule,
            "success": self.success,
            "insight": self.insight.to_dict() if self.insight else None,
            "error": self.error
        }

    def __str__(self):
        if self.error:
            return f"[ERROR] Rule '{self.rule}' failed: {self.error}"
        if self.insight:
            return str(self.insight)
        return f"[OK] Rule '{self.rule}' passed with no issues."
