from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class SentimentAxis(BaseModel):
    axis: str = Field(..., description="Axe d'analyse (ex: Performance, Design, Autonomie, Prix)")
    rationale: str = Field(..., description="Justification technique")

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
    seller_info: Optional[SellerInfo] = Field(None, description="Informations sur le vendeur")
    raw_review_summary: str = Field("", description="Résumé brut des avis clients")

class MultimodalResponse(BaseModel):
    """
    Réponse structurée pour le double flux WhatsApp et TTS (PBI-1701.3).
    """
    text_whatsapp: str = Field(..., description="Texte riche avec emojis, puces et liens pour WhatsApp")
    text_tts: str = Field(..., description="Texte fluide et naturel en Darija pour la synthèse vocale, sans emojis ni caractères techniques")
    media_url: Optional[str] = Field(None, description="URL de l'image du produit recommandé (si disponible)")
