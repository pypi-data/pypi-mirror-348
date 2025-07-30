"""
Domain Catalog module defining the semantic framework for a specific domain.
"""
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Dict, List, Optional, Any, Union
import uuid
import json

from .event_record import DomainType

@dataclass
class TermDefinition:
    """Definition of a term in the domain catalog."""
    definition: str
    context: Optional[str] = None
    examples: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TermDefinition':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class MetricDefinition:
    """Definition of a metric in the domain catalog."""
    description: str
    unit: str
    range: Dict[str, float]  # min, max
    interpretation: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MetricDefinition':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class Classification:
    """Classification scheme in the domain catalog."""
    categories: List[str]
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Classification':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class AttributeLevel:
    """Level definition for an attribute."""
    level: int
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AttributeLevel':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class Attribute:
    """Definition of an attribute in a framework."""
    id: str
    name: str
    description: str
    levels: List[AttributeLevel] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'levels': [level.to_dict() for level in self.levels]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Attribute':
        """Create from dictionary."""
        attr_data = data.copy()
        
        if 'levels' in attr_data:
            attr_data['levels'] = [AttributeLevel.from_dict(level) for level in attr_data['levels']]
            
        return cls(**attr_data)

@dataclass
class AttributeFramework:
    """Framework of attributes in the domain catalog."""
    name: str
    attributes: List[Attribute] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'attributes': [attr.to_dict() for attr in self.attributes]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AttributeFramework':
        """Create from dictionary."""
        framework_data = data.copy()
        
        if 'attributes' in framework_data:
            framework_data['attributes'] = [Attribute.from_dict(attr) for attr in framework_data['attributes']]
            
        return cls(**framework_data)

@dataclass
class MappedAttribute:
    """Mapping between local and external attribute IDs."""
    local_id: str
    external_id: str
    confidence: str  # high, medium, low
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'MappedAttribute':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class ExternalFrameworkMapping:
    """Mapping to an external framework."""
    url: str
    version: str
    mapped_attributes: List[MappedAttribute] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'url': self.url,
            'version': self.version,
            'mapped_attributes': [mapping.to_dict() for mapping in self.mapped_attributes]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExternalFrameworkMapping':
        """Create from dictionary."""
        mapping_data = data.copy()
        
        if 'mapped_attributes' in mapping_data:
            mapping_data['mapped_attributes'] = [
                MappedAttribute.from_dict(attr) for attr in mapping_data['mapped_attributes']
            ]
            
        return cls(**mapping_data)

@dataclass
class CustomExtension:
    """Custom extension for the domain catalog."""
    description: str
    schema: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomExtension':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class Organization:
    """Organization that owns the domain catalog."""
    id: str
    name: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Organization':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class DomainCatalog:
    """
    Represents a Catalog of Domain Definitions (CDD) in the Universal History system.
    
    A Domain Catalog establishes the semantic framework for interpreting and standardizing
    information in Event Records and Trajectory Syntheses within a specific domain.
    """
    domain_type: DomainType
    organization: Organization
    
    cdd_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "1.0"
    last_updated: date = field(default_factory=date.today)
    definitions: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        'terms': {},
        'metrics': {},
        'classifications': {},
        'attributes': {}
    })
    mappings: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        'external_frameworks': {}
    })
    custom_extensions: Dict[str, CustomExtension] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the DomainCatalog to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the DomainCatalog
        """
        domain_type_value = self.domain_type.value if isinstance(self.domain_type, DomainType) else self.domain_type
        
        # Process definitions dictionary
        definitions_dict = {}
        
        # Terms
        if 'terms' in self.definitions:
            definitions_dict['terms'] = {
                k: v.to_dict() if hasattr(v, 'to_dict') else v 
                for k, v in self.definitions['terms'].items()
            }
        
        # Metrics
        if 'metrics' in self.definitions:
            definitions_dict['metrics'] = {
                k: v.to_dict() if hasattr(v, 'to_dict') else v 
                for k, v in self.definitions['metrics'].items()
            }
        
        # Classifications
        if 'classifications' in self.definitions:
            definitions_dict['classifications'] = {
                k: v.to_dict() if hasattr(v, 'to_dict') else v 
                for k, v in self.definitions['classifications'].items()
            }
        
        # Attributes
        if 'attributes' in self.definitions:
            definitions_dict['attributes'] = {
                k: v.to_dict() if hasattr(v, 'to_dict') else v 
                for k, v in self.definitions['attributes'].items()
            }
        
        # Process mappings dictionary
        mappings_dict = {}
        
        # External frameworks
        if 'external_frameworks' in self.mappings:
            mappings_dict['external_frameworks'] = {
                k: v.to_dict() if hasattr(v, 'to_dict') else v 
                for k, v in self.mappings['external_frameworks'].items()
            }
        
        return {
            'cdd_id': self.cdd_id,
            'domain_type': domain_type_value,
            'version': self.version,
            'last_updated': self.last_updated.isoformat(),
            'organization': self.organization.to_dict(),
            'definitions': definitions_dict,
            'mappings': mappings_dict,
            'custom_extensions': {
                k: v.to_dict() for k, v in self.custom_extensions.items()
            }
        }
    
    def to_json(self) -> str:
        """
        Convert the DomainCatalog to a JSON string.
        
        Returns:
            str: JSON representation of the DomainCatalog
        """
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DomainCatalog':
        """
        Create a DomainCatalog from a dictionary.
        
        Args:
            data (Dict[str, Any]): Dictionary containing DomainCatalog data
            
        Returns:
            DomainCatalog: New DomainCatalog instance
        """
        # Create a copy to avoid modifying the original
        catalog_data = data.copy()
        
        # Handle domain_type
        if 'domain_type' in catalog_data:
            catalog_data['domain_type'] = DomainType(catalog_data['domain_type'])
        
        # Handle organization
        if 'organization' in catalog_data:
            catalog_data['organization'] = Organization.from_dict(catalog_data['organization'])
        
        # Handle definitions
        if 'definitions' in catalog_data:
            definitions_data = catalog_data['definitions']
            definitions_dict = {}
            
            # Terms
            if 'terms' in definitions_data:
                definitions_dict['terms'] = {
                    k: TermDefinition.from_dict(v) if isinstance(v, dict) else v
                    for k, v in definitions_data['terms'].items()
                }
            
            # Metrics
            if 'metrics' in definitions_data:
                definitions_dict['metrics'] = {
                    k: MetricDefinition.from_dict(v) if isinstance(v, dict) else v
                    for k, v in definitions_data['metrics'].items()
                }
            
            # Classifications
            if 'classifications' in definitions_data:
                definitions_dict['classifications'] = {
                    k: Classification.from_dict(v) if isinstance(v, dict) else v
                    for k, v in definitions_data['classifications'].items()
                }
            
            # Attributes
            if 'attributes' in definitions_data:
                definitions_dict['attributes'] = {
                    k: AttributeFramework.from_dict(v) if isinstance(v, dict) else v
                    for k, v in definitions_data['attributes'].items()
                }
            
            catalog_data['definitions'] = definitions_dict
        
        # Handle mappings
        if 'mappings' in catalog_data:
            mappings_data = catalog_data['mappings']
            mappings_dict = {}
            
            # External frameworks
            if 'external_frameworks' in mappings_data:
                mappings_dict['external_frameworks'] = {
                    k: ExternalFrameworkMapping.from_dict(v) if isinstance(v, dict) else v
                    for k, v in mappings_data['external_frameworks'].items()
                }
            
            catalog_data['mappings'] = mappings_dict
        
        # Handle custom extensions
        if 'custom_extensions' in catalog_data:
            catalog_data['custom_extensions'] = {
                k: CustomExtension.from_dict(v) if isinstance(v, dict) else v
                for k, v in catalog_data['custom_extensions'].items()
            }
        
        # Handle last_updated
        if 'last_updated' in catalog_data and isinstance(catalog_data['last_updated'], str):
            catalog_data['last_updated'] = date.fromisoformat(catalog_data['last_updated'])
        
        return cls(**catalog_data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'DomainCatalog':
        """
        Create a DomainCatalog from a JSON string.
        
        Args:
            json_str (str): JSON string containing DomainCatalog data
            
        Returns:
            DomainCatalog: New DomainCatalog instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def add_term(self, term_key: str, definition: str, context: Optional[str] = None, 
                 examples: Optional[List[str]] = None) -> None:
        """
        Add a term definition to the catalog.
        
        Args:
            term_key (str): Key for the term
            definition (str): Definition of the term
            context (Optional[str]): Context for the term
            examples (Optional[List[str]]): Examples of the term's usage
        """
        if 'terms' not in self.definitions:
            self.definitions['terms'] = {}
            
        self.definitions['terms'][term_key] = TermDefinition(
            definition=definition,
            context=context,
            examples=examples or []
        )
        
        self.last_updated = date.today()
    
    def add_metric(self, metric_key: str, description: str, unit: str, 
                   min_value: float, max_value: float, 
                   interpretation: Optional[str] = None) -> None:
        """
        Add a metric definition to the catalog.
        
        Args:
            metric_key (str): Key for the metric
            description (str): Description of the metric
            unit (str): Unit of measurement
            min_value (float): Minimum value
            max_value (float): Maximum value
            interpretation (Optional[str]): How to interpret the metric values
        """
        if 'metrics' not in self.definitions:
            self.definitions['metrics'] = {}
            
        self.definitions['metrics'][metric_key] = MetricDefinition(
            description=description,
            unit=unit,
            range={'min': min_value, 'max': max_value},
            interpretation=interpretation
        )
        
        self.last_updated = date.today()
    
    def add_classification(self, classification_key: str, categories: List[str], 
                           description: str) -> None:
        """
        Add a classification scheme to the catalog.
        
        Args:
            classification_key (str): Key for the classification
            categories (List[str]): Categories in the classification
            description (str): Description of the classification scheme
        """
        if 'classifications' not in self.definitions:
            self.definitions['classifications'] = {}
            
        self.definitions['classifications'][classification_key] = Classification(
            categories=categories,
            description=description
        )
        
        self.last_updated = date.today()
    
    def get_term_definition(self, term_key: str) -> Optional[TermDefinition]:
        """
        Get a term definition from the catalog.
        
        Args:
            term_key (str): Key for the term
            
        Returns:
            Optional[TermDefinition]: The term definition or None if not found
        """
        if 'terms' not in self.definitions:
            return None
            
        return self.definitions['terms'].get(term_key)
    
    def get_metric_definition(self, metric_key: str) -> Optional[MetricDefinition]:
        """
        Get a metric definition from the catalog.
        
        Args:
            metric_key (str): Key for the metric
            
        Returns:
            Optional[MetricDefinition]: The metric definition or None if not found
        """
        if 'metrics' not in self.definitions:
            return None
            
        return self.definitions['metrics'].get(metric_key)
    
    def get_classification(self, classification_key: str) -> Optional[Classification]:
        """
        Get a classification scheme from the catalog.
        
        Args:
            classification_key (str): Key for the classification
            
        Returns:
            Optional[Classification]: The classification or None if not found
        """
        if 'classifications' not in self.definitions:
            return None
            
        return self.definitions['classifications'].get(classification_key)
