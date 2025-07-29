from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataUserTypeControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.user_type import MaleoMetadataUserTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.user_type import MaleoMetadataUserTypeClientParametersTransfers
from maleo_metadata.models.transfers.results.client.user_type import MaleoMetadataUserTypeClientResultsTransfers
from maleo_metadata.types.results.client.user_type import MaleoMetadataUserTypeClientResultsTypes

class MaleoMetadataUserTypeClientService(ClientService):
    def __init__(self, logger, controllers:MaleoMetadataUserTypeControllers):
        super().__init__(logger)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataUserTypeControllers:
        raise self._controllers

    async def get_user_types(
        self,
        parameters:MaleoMetadataUserTypeClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataUserTypeClientResultsTypes.GetMultiple:
        """Retrieve user types from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user types",
            logger=self._logger,
            fail_result_class=MaleoMetadataUserTypeClientResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataUserTypeClientResultsTransfers.Fail(message=message, description=description)
            #* Retrieve user types using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_user_types(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataUserTypeClientResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoMetadataUserTypeClientResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                if controller_result.content["data"] is None:
                    return MaleoMetadataUserTypeClientResultsTransfers.NoData.model_validate(controller_result.content)
                else:
                    return MaleoMetadataUserTypeClientResultsTransfers.MultipleData.model_validate(controller_result.content)
        return await _impl()

    async def get_user_type(
        self,
        parameters:MaleoMetadataUserTypeGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataUserTypeClientResultsTypes.GetSingle:
        """Retrieve user type from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user type",
            logger=self._logger,
            fail_result_class=MaleoMetadataUserTypeClientResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataUserTypeClientResultsTransfers.Fail(message=message, description=description)
            #* Retrieve user type using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_user_type(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataUserTypeClientResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoMetadataUserTypeClientResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoMetadataUserTypeClientResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()