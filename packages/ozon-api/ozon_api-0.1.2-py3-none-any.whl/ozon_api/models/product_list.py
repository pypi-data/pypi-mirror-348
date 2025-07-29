from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union

class ProductListFilter(BaseModel):
    offer_id: Optional[List[str]] = Field(None, description="Артикулы товаров (offer_id)")
    product_id: Optional[List[int]] = Field(None, description="ID товаров (product_id)")
    visibility: Optional[str] = Field(None, description="Видимость товара (ALL, VISIBLE, INVISIBLE)")
    # Можно добавить другие поля фильтра по необходимости

class ProductListRequest(BaseModel):
    filter: ProductListFilter = Field(..., description="Фильтр товаров")
    last_id: Optional[str] = Field(None, description="Идентификатор последнего товара для пагинации")
    limit: int = Field(1000, description="Максимальное количество товаров в ответе (1-1000)")
    sort_by: Optional[str] = Field(None, description="Сортировка (например, 'product_id')")
    sort_dir: Optional[Literal["ASC", "DESC"]] = Field(None, description="Направление сортировки")

class ProductListItem(BaseModel):
    product_id: int = Field(..., description="ID товара в системе Ozon")
    offer_id: str = Field(..., description="Артикул товара (offer_id)")
    visibility: str = Field(..., description="Видимость товара")
    # Можно добавить другие поля из ответа по необходимости

class ProductListResponse(BaseModel):
    items: List[ProductListItem] = Field(..., description="Список товаров")
    total: int = Field(..., description="Общее количество товаров")
    last_id: Optional[str] = Field(None, description="Идентификатор последнего товара для пагинации") 