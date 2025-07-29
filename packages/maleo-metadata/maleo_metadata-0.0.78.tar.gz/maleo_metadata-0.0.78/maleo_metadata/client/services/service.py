from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataServiceControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.service import MaleoMetadataServiceGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.service import MaleoMetadataServiceClientParametersTransfers
from maleo_metadata.models.transfers.results.client.service import MaleoMetadataServiceClientResultsTransfers
from maleo_metadata.types.results.client.service import MaleoMetadataServiceClientResultsTypes

class MaleoMetadataServiceClientService(ClientService):
    def __init__(self, logger, controllers:MaleoMetadataServiceControllers):
        super().__init__(logger)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataServiceControllers:
        raise self._controllers

    async def get_services(
        self,
        parameters:MaleoMetadataServiceClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataServiceClientResultsTypes.GetMultiple:
        """Retrieve services from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving services",
            logger=self._logger,
            fail_result_class=MaleoMetadataServiceClientResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataServiceClientResultsTransfers.Fail(message=message, description=description)
            #* Retrieve services using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_services(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataServiceClientResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoMetadataServiceClientResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                if controller_result.content["data"] is None:
                    return MaleoMetadataServiceClientResultsTransfers.NoData.model_validate(controller_result.content)
                else:
                    return MaleoMetadataServiceClientResultsTransfers.MultipleData.model_validate(controller_result.content)
        return await _impl()

    async def get_service(
        self,
        parameters:MaleoMetadataServiceGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataServiceClientResultsTypes.GetSingle:
        """Retrieve service from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving service",
            logger=self._logger,
            fail_result_class=MaleoMetadataServiceClientResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataServiceClientResultsTransfers.Fail(message=message, description=description)
            #* Retrieve service using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_service(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataServiceClientResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoMetadataServiceClientResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoMetadataServiceClientResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()