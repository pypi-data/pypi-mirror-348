"""
Trajectory Synthesis module representing the analysis and summary of multiple Event Records.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
import uuid
import json

from .event_record import DomainType, ConfidenceLevel

@dataclass
class TimeFrame:
    """Represents a time period for a Trajectory Synthesis."""
    start: datetime
    end: datetime
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary with ISO format dates."""
        return {
            'start': self.start.isoformat(),
            'end': self.end.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'TimeFrame':
        """Create from dictionary with ISO format dates."""
        return cls(
            start=datetime.fromisoformat(data['start']),
            end=datetime.fromisoformat(data['end'])
        )

@dataclass
class SignificantEvent:
    """Represents a significant event referenced in a Trajectory Synthesis."""
    re_id: str
    description: str
    significance: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'SignificantEvent':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class Metric:
    """Represents a metric analyzed in a Trajectory Synthesis."""
    value: float
    trend: str  # improving, stable, declining
    analysis: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Metric':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class SynthesisReviewer:
    """Represents the reviewer of a Trajectory Synthesis."""
    id: str
    name: str
    role: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'SynthesisReviewer':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class SynthesisMetadata:
    """Represents metadata for a Trajectory Synthesis."""
    generated_by: str
    generated_on: datetime
    reviewed_by: Optional[SynthesisReviewer] = None
    reviewed_on: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'generated_by': self.generated_by,
            'generated_on': self.generated_on.isoformat()
        }
        
        if self.reviewed_by:
            result['reviewed_by'] = self.reviewed_by.to_dict()
        
        if self.reviewed_on:
            result['reviewed_on'] = self.reviewed_on.isoformat()
            
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SynthesisMetadata':
        """Create from dictionary."""
        metadata_data = data.copy()
        
        # Handle datetime
        if 'generated_on' in metadata_data and isinstance(metadata_data['generated_on'], str):
            metadata_data['generated_on'] = datetime.fromisoformat(metadata_data['generated_on'])
            
        if 'reviewed_on' in metadata_data and isinstance(metadata_data['reviewed_on'], str):
            metadata_data['reviewed_on'] = datetime.fromisoformat(metadata_data['reviewed_on'])
            
        # Handle reviewer
        if 'reviewed_by' in metadata_data and metadata_data['reviewed_by']:
            metadata_data['reviewed_by'] = SynthesisReviewer.from_dict(metadata_data['reviewed_by'])
            
        return cls(**metadata_data)

@dataclass
class TrajectorySynthesis:
    """
    Represents a Synthesis of Trajectory (ST) in the Universal History system.
    
    A Trajectory Synthesis condenses and analyzes information from multiple
    Event Records to provide a summary of the subject's progress in a specific domain.
    """
    subject_id: str
    domain_type: DomainType
    time_frame: TimeFrame
    summary: str
    
    st_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    level: int = 1  # Hierarchical level (1=most detailed, higher numbers=more summarized)
    source_events: List[str] = field(default_factory=list)  # List of RE IDs
    key_insights: List[str] = field(default_factory=list)
    significant_events: List[SignificantEvent] = field(default_factory=list)
    metrics: Dict[str, Metric] = field(default_factory=dict)
    patterns: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    domain_specific_data: Dict[str, Any] = field(default_factory=dict)
    metadata: SynthesisMetadata = field(default_factory=lambda: SynthesisMetadata(
        generated_by="system",
        generated_on=datetime.now()
    ))
    confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM
    next_review_date: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the TrajectorySynthesis to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the TrajectorySynthesis
        """
        domain_type_value = self.domain_type.value if isinstance(self.domain_type, DomainType) else self.domain_type
        
        result = {
            'st_id': self.st_id,
            'subject_id': self.subject_id,
            'domain_type': domain_type_value,
            'level': self.level,
            'time_frame': self.time_frame.to_dict(),
            'summary': self.summary,
            'source_events': self.source_events,
            'key_insights': self.key_insights,
            'significant_events': [event.to_dict() for event in self.significant_events],
            'metrics': {k: v.to_dict() for k, v in self.metrics.items()},
            'patterns': self.patterns,
            'recommendations': self.recommendations,
            'domain_specific_data': self.domain_specific_data,
            'metadata': self.metadata.to_dict(),
            'confidence_level': self.confidence_level.value if isinstance(self.confidence_level, ConfidenceLevel) else self.confidence_level
        }
        
        if self.next_review_date:
            result['next_review_date'] = self.next_review_date.isoformat()
            
        return result
    
    def to_json(self) -> str:
        """
        Convert the TrajectorySynthesis to a JSON string.
        
        Returns:
            str: JSON representation of the TrajectorySynthesis
        """
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrajectorySynthesis':
        """
        Create a TrajectorySynthesis from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing TrajectorySynthesis data
            
        Returns:
            TrajectorySynthesis: New TrajectorySynthesis instance
        """
        # Create a copy to avoid modifying the original
        synthesis_data = data.copy()
        
        # Handle domain_type
        if 'domain_type' in synthesis_data:
            synthesis_data['domain_type'] = DomainType(synthesis_data['domain_type'])
        
        # Handle time_frame
        if 'time_frame' in synthesis_data:
            synthesis_data['time_frame'] = TimeFrame.from_dict(synthesis_data['time_frame'])
        
        # Handle significant_events
        if 'significant_events' in synthesis_data:
            synthesis_data['significant_events'] = [
                SignificantEvent.from_dict(event) for event in synthesis_data['significant_events']
            ]
        
        # Handle metrics
        if 'metrics' in synthesis_data:
            synthesis_data['metrics'] = {
                k: Metric.from_dict(v) for k, v in synthesis_data['metrics'].items()
            }
        
        # Handle metadata
        if 'metadata' in synthesis_data:
            synthesis_data['metadata'] = SynthesisMetadata.from_dict(synthesis_data['metadata'])
        
        # Handle confidence_level
        if 'confidence_level' in synthesis_data:
            synthesis_data['confidence_level'] = ConfidenceLevel(synthesis_data['confidence_level'])
        
        # Handle next_review_date
        if 'next_review_date' in synthesis_data and isinstance(synthesis_data['next_review_date'], str):
            synthesis_data['next_review_date'] = datetime.fromisoformat(synthesis_data['next_review_date'])
        
        return cls(**synthesis_data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TrajectorySynthesis':
        """
        Create a TrajectorySynthesis from a JSON string.
        
        Args:
            json_str (str): JSON string containing TrajectorySynthesis data
            
        Returns:
            TrajectorySynthesis: New TrajectorySynthesis instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)