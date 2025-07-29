from fastapi import status
from functools import wraps
from typing import Awaitable, Callable, Dict, List
from maleo_foundation.types import BaseTypes
from maleo_foundation.models.responses import BaseResponses
from maleo_foundation.models.transfers.parameters.general \
    import BaseGeneralParametersTransfers
from maleo_foundation.models.transfers.results.service.controllers.rest \
    import BaseServiceRESTControllerResults
from maleo_foundation.expanded_types.general import BaseGeneralExpandedTypes

class BaseControllerUtils:
    @staticmethod
    def field_expansion_handler(
        expandable_fields_dependencies_map:BaseTypes.OptionalStringToListOfStringDict = None,
        field_expansion_processors:BaseGeneralExpandedTypes.OptionalListOfFieldExpansionProcessor = None
    ):
        """
        Decorator to handle expandable fields validation and processing.
        
        Args:
            expandable_fields_dependencies_map: Dictionary where keys are dependency fields and values are lists of dependent fields
            field_expansion_processors: List of processor functions that handle that field's data
        """
        def decorator(func:Callable[..., Awaitable[BaseServiceRESTControllerResults]]):
            @wraps(func)
            async def wrapper(parameters, *args, **kwargs):
                expand:BaseTypes.OptionalListOfStrings = getattr(parameters, 'expand', None)

                #* Validate expandable fields dependencies
                if expand is not None and expandable_fields_dependencies_map is not None:
                    for dependency, dependents in expandable_fields_dependencies_map.items():
                        if dependency not in expand:
                            for dependent in dependents:
                                if dependent in expand:
                                    other = f"'{dependency}' must also be expanded if '{dependent}' is expanded"
                                    content = BaseResponses.InvalidExpand(other=other).model_dump()
                                    return BaseServiceRESTControllerResults(
                                        success=False,
                                        content=content,
                                        status_code=status.HTTP_400_BAD_REQUEST
                                    )

                #* Call the original function
                result = await func(parameters, *args, **kwargs)

                if not isinstance(result.content, Dict):
                    return result

                #* Process the fields if needed
                if (result.success
                    and result.content.get("data", None) is not None
                    and field_expansion_processors is not None
                ):
                    data = result.content["data"]
                    if isinstance(data, List):
                        for idx, dt in enumerate(data):
                            for processor in field_expansion_processors:
                                raw_parameters = {"data": dt, "expand": expand}
                                parameters = (
                                    BaseGeneralParametersTransfers
                                    .FieldExpansionProcessor
                                    .model_validate(raw_parameters)
                                )
                                dt = processor(parameters)
                                data[idx] = dt
                    elif isinstance(data, Dict):
                        raw_parameters = {"data": data, "expand": expand}
                        parameters = (
                            BaseGeneralParametersTransfers
                            .FieldExpansionProcessor
                            .model_validate(raw_parameters)
                        )
                        for processor in field_expansion_processors:
                            data = processor(parameters)
                    result.content["data"] = data
                    result.process_response()

                return result
            return wrapper
        return decorator