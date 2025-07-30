import uuid
from typing import List, Dict, Union, Optional
from dataclasses import dataclass


@dataclass
class Sentiment:
    """Domain object representing the sentiment of analyzed text"""
    score: float
    label: str  # 'negative', 'neutral', or 'positive'


@dataclass
class DetectedEntity:
    """Domain object representing an entity detected in analyzed text"""
    name: str
    type: str
    mentions: List[str] = None

    def __post_init__(self):
        if self.mentions is None:
            self.mentions = []


@dataclass
class DetectedRelationship:
    """Domain object representing a relationship between entities detected in text"""
    source_entity_name: str
    relation_type: str
    target_entity_name: str
    confidence: float = 0.0  # Confidence score of this relationship detection


@dataclass
class ExtractedFact:
    """Domain object representing a factual statement extracted from text"""
    statement: str
    referenced_entities: List[str] = None  # Names of entities referenced in this fact

    def __post_init__(self):
        if self.referenced_entities is None:
            self.referenced_entities = []


@dataclass
class TextAnalysisResult:
    """Root aggregate for the result of analyzing a piece of text"""
    text_id: str
    category: str
    topic: str
    sentiment: Sentiment
    entities: List[DetectedEntity]
    relationships: List[DetectedRelationship]
    facts: List[ExtractedFact]

    def __init__(self, text_id: str, category: str, topic: str,
                 sentiment_score: float = 0.0,
                 sentiment_label: str = "neutral",
                 entities: Optional[List[Dict[str, Union[str, List[str]]]]] = None,
                 relationships: Optional[List[Dict[str, Union[str, float]]]] = None,
                 facts: Optional[List[Dict[str, Union[str, List[str]]]]] = None):

        self.text_id = text_id
        self.category = category
        self.topic = topic
        self.sentiment = Sentiment(sentiment_score, sentiment_label)

        # Process entities
        self.entities = []
        if entities:
            for entity_data in entities:
                entity = DetectedEntity(
                    name=entity_data["name"],
                    type=entity_data["type"],
                    mentions=entity_data.get("mentions", [])
                )
                self.entities.append(entity)

        # Process relationships
        self.relationships = []
        if relationships:
            for rel_data in relationships:
                rel = DetectedRelationship(
                    source_entity_name=rel_data["source_entity_name"],
                    relation_type=rel_data["relation_type"],
                    target_entity_name=rel_data["target_entity_name"],
                    confidence=rel_data.get("confidence", 0.0)
                )
                self.relationships.append(rel)

        # Process facts
        self.facts = []
        if facts:
            for fact_data in facts:
                fact = ExtractedFact(
                    statement=fact_data["statement"],
                    referenced_entities=fact_data.get("referenced_entities", [])
                )
                self.facts.append(fact)

    def to_dict(self) -> Dict[str, Union[str, Dict, List]]:
        """Convert the TextAnalysisResult to a dictionary"""
        return {
            "text_id": self.text_id,
            "category": self.category,
            "topic": self.topic,
            "sentiment": {
                "score": self.sentiment.score,
                "label": self.sentiment.label
            },
            "entities": [
                {
                    "name": entity.name,
                    "type": entity.type,
                    "mentions": entity.mentions
                } for entity in self.entities
            ],
            "relationships": [
                {
                    "source_entity_name": rel.source_entity_name,
                    "relation_type": rel.relation_type,
                    "target_entity_name": rel.target_entity_name,
                    "confidence": rel.confidence
                } for rel in self.relationships
            ],
            "facts": [
                {
                    "statement": fact.statement,
                    "referenced_entities": fact.referenced_entities
                } for fact in self.facts
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TextAnalysisResult':
        """Create a TextAnalysisResult from a dictionary"""
        random_guid = uuid.uuid4()
        random_guid_str = str(uuid.uuid4())

        return cls(
            text_id=random_guid_str,
            category=data["category"],
            topic=data["topic"],
            sentiment_score=data["sentiment"]["score"],
            sentiment_label=data["sentiment"]["label"],
            entities=data.get("entities", []),
            relationships=data.get("relationships", []),
            facts=data.get("facts", [])
        )
