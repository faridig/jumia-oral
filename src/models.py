from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class SentimentAxis(BaseModel):
    axis: str = Field(..., description="Axe d'analyse (ex: Performance, Design, Autonomie, Prix)")
    score: Optional[float] = Field(None, description="Score de 0 à 10")
    rationale: str = Field(..., description="Justification du score")

class SellerInfo(BaseModel):
    name: Optional[str] = Field(None, description="Nom du vendeur")
    rating_percentage: Optional[str] = Field(None, description="Évaluation du vendeur en pourcentage")
    follower_count: Optional[str] = Field(None, description="Nombre d'abonnés du vendeur")
    shipping_speed: Optional[str] = Field(None, description="Performance: Vitesse d'expédition")
    quality_score: Optional[str] = Field(None, description="Performance: Score Qualité")
    customer_reviews_score: Optional[str] = Field(None, description="Performance: Avis des consommateurs")

class CoreMetadata(BaseModel):
    name: str = Field(..., description="Nom complet du produit")
    current_price: Optional[float] = Field(None, description="Prix actuel")
    old_price: Optional[float] = Field(None, description="Ancien prix")
    currency: str = Field("Dhs", description="Devise")
    brand: Optional[str] = Field(None, description="Marque")
    images: List[str] = Field(default_factory=list, description="URLs des images")
    url: str = Field(..., description="URL du produit")
    category: Optional[str] = Field(None, description="Catégorie du produit")
    rating: float = Field(0.0, description="Note moyenne")
    review_count: int = Field(0, description="Nombre d'avis")

class CategoryAgnosticProduct(BaseModel):
    core_metadata: CoreMetadata = Field(..., description="Métadonnées de base")
    category_specs: Dict[str, Any] = Field(..., description="Spécifications normalisées selon la catégorie")
    sentiment_analysis: List[SentimentAxis] = Field(default_factory=list, description="Analyse de sentiment par axe")
    value_for_money_score: float = Field(0.0, description="Score rapport qualité-prix (0-10)")
    trust_score: float = Field(0.0, description="Score de confiance basé sur les avis (0-5)")
    seller_info: Optional[SellerInfo] = Field(None, description="Informations sur le vendeur")
    raw_review_summary: str = Field("", description="Résumé brut des avis clients")
