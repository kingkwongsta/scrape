from pydantic import BaseModel

class PokemonCards(BaseModel):
    card_name: str
    card_list_from: float
    card_market_price: float
    card_set_name: str
    card_set_number: int
    card_set_rarity: str
