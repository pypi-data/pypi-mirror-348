from pydantic import BaseModel, Field
from typing import List, Optional


class ProductImportInfo(BaseModel):
    task_id: int = Field(
        description="Идентификатор задачи импорта.",
        title="Идентификатор задачи импорта",
    )


class ProductPicturesInfoRequest(BaseModel):
    task_id: int = Field(..., description="Идентификатор задачи загрузки изображений.")


class ProductPicturesInfoResponseItem(BaseModel):
    product_id: int = Field(..., description="Идентификатор товара в системе продавца")
    status: str = Field(..., description="Статус обработки изображений для товара")
    errors: Optional[List[str]] = Field(
        default_factory=list, description="Ошибки при обработке изображений, если есть"
    )


class ProductPicturesInfoResponse(BaseModel):
    items: List[ProductPicturesInfoResponseItem] = Field(
        ..., description="Список товаров и статусов обработки изображений"
    )
    status: str = Field(..., description="Общий статус задачи")
