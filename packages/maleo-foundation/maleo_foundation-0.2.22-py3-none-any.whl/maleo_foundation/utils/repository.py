import asyncio
from functools import wraps
from pydantic import ValidationError
from typing import Optional, Type, Union
from maleo_foundation.types import BaseTypes
from maleo_foundation.models.transfers.results.service.repository import \
    BaseServiceRepositoryResultsTransfers

class BaseRepositoryUtils:
    @staticmethod
    def result_processor(
        fail_class:Type[BaseServiceRepositoryResultsTransfers.Fail],
        data_found_class:Union[
            Type[BaseServiceRepositoryResultsTransfers.SingleData],
            Type[BaseServiceRepositoryResultsTransfers.UnpaginatedMultipleData],
            Type[BaseServiceRepositoryResultsTransfers.PaginatedMultipleData]
        ],
        no_data_class:Optional[Type[BaseServiceRepositoryResultsTransfers.NoData]] = None,
    ):
        """Decorator to handle repository-related exceptions consistently."""
        def decorator(func):
            def _processor(result:BaseTypes.StringToAnyDict):
                if "success" not in result or "data" not in result:
                    raise ValueError("Result did not have both 'success' and 'data' field")
                success = result.get("success")
                data = result.get("data")
                if success is False:
                    validated_result = fail_class.model_validate(result)
                    return validated_result
                if success is True:
                    if data is None:
                        if no_data_class is None:
                            raise ValueError("'no_data_class' must be given to validate No Data")
                        validated_result = no_data_class.model_validate(result)
                        return validated_result
                    else:
                        validated_result = data_found_class.model_validate(result)
                        return validated_result
            if asyncio.iscoroutinefunction(func):
                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    try:
                        result:BaseTypes.StringToAnyDict = await func(*args, **kwargs)
                        return _processor(result=result)
                    except ValidationError as e:
                        raise
                    except Exception as e:
                        raise
                return async_wrapper
            else:
                @wraps(func)
                def sync_wrapper(*args, **kwargs):
                    try:
                        result:BaseTypes.StringToAnyDict = func(*args, **kwargs)
                        return _processor(result=result)
                    except ValidationError as e:
                        raise
                    except Exception as e:
                        raise
                return sync_wrapper
        return decorator