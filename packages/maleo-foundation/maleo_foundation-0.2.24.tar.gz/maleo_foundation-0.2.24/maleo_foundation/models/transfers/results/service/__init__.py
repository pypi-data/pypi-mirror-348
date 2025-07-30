from __future__ import annotations
from .general import BaseServiceGeneralResultsTransfers
from .query import BaseServiceQueryResultsTransfers
from .repository import BaseServiceRepositoryResultsTransfers
from .controllers import BaseServiceControllerResultsTransfers

class BaseServiceResultsTransfers:
    General = BaseServiceGeneralResultsTransfers
    Query = BaseServiceQueryResultsTransfers
    Repository = BaseServiceRepositoryResultsTransfers
    Controller = BaseServiceControllerResultsTransfers