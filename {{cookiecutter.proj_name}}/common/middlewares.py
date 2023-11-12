"""
Author: G
Time: 2023 2023/10/10 10:36
File: middlewares.py
"""
from fastapi import Request, Response
from common.response import StructuredResponse


def pub_exception_handler(request, exc):
    return StructuredResponse(content=str(exc), success=False, status_code=400)
