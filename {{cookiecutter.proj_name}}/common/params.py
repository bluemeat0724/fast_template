"""
Author: G
Time: 2023 2023/9/26 14:54
File: params.py
"""
from typing import List

from fastapi.encoders import jsonable_encoder
from pydantic import ConfigDict, BaseModel, Field, create_model


class PageNation(BaseModel):
    page_no: int = Field(default=1, alias='page_no')
    page_size: int = Field(default=20, alias='page_size')


def paging_params(page_no: int = 1, page_size: int = 20):
    return PageNation(page_no=page_no, page_size=page_size)


def filter_params(attributes: dict):
    return create_model("filter_param", **attributes)


def param_combine(*args: List[BaseModel]):
    """将多个 pydantic BaseModel 合并为一个"""

    class AnyFieldModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True, extra='allow')

    return AnyFieldModel.model_validate({k: v for p in args for k, v in p.model_dump().items()}, )


