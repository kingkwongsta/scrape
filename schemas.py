from pydantic import BaseModel
from langchain_core.pydantic_v1 import BaseModel, Field

class Pokemon(BaseModel):
    card_name: str = Field(description="The name of the card")
class PokemonCards(BaseModel):
    card_name: str
    # card_list_from: float
    # card_market_price: float
    # card_set_name: str
    # card_set_number: int
    # card_set_rarity: str
    
Pokemon_schema = {
  "properties": {
    "card_name": {
      "type": "string"
    },
  },
  "required": ["card_name"],
}