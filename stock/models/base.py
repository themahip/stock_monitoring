from ramailo.models.base import BaseModel

class BaseStockModel(BaseModel):
    """Add the BaseStock Model here"""
    class Meta:
        abstract = True