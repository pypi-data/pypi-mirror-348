from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataBloodTypeControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.blood_type import MaleoMetadataBloodTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.blood_type import MaleoMetadataBloodTypeClientParametersTransfers
from maleo_metadata.models.transfers.results.client.blood_type import MaleoMetadataBloodTypeClientResultsTransfers
from maleo_metadata.types.results.client.blood_type import MaleoMetadataBloodTypeClientResultsTypes

class MaleoMetadataBloodTypeClientService(ClientService):
    def __init__(self, logger, controllers:MaleoMetadataBloodTypeControllers):
        super().__init__(logger)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataBloodTypeControllers:
        raise self._controllers

    async def get_blood_types(
        self,
        parameters:MaleoMetadataBloodTypeClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataBloodTypeClientResultsTypes.GetMultiple:
        """Retrieve blood types from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving blood types",
            logger=self._logger,
            fail_result_class=MaleoMetadataBloodTypeClientResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataBloodTypeClientResultsTransfers.Fail(message=message, description=description)
            #* Retrieve blood types using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_blood_types(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataBloodTypeClientResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoMetadataBloodTypeClientResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                if controller_result.content["data"] is None:
                    return MaleoMetadataBloodTypeClientResultsTransfers.NoData.model_validate(controller_result.content)
                else:
                    return MaleoMetadataBloodTypeClientResultsTransfers.MultipleData.model_validate(controller_result.content)
        return await _impl()

    async def get_blood_type(
        self,
        parameters:MaleoMetadataBloodTypeGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataBloodTypeClientResultsTypes.GetSingle:
        """Retrieve blood type from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving blood type",
            logger=self._logger,
            fail_result_class=MaleoMetadataBloodTypeClientResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataBloodTypeClientResultsTransfers.Fail(message=message, description=description)
            #* Retrieve blood type using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_blood_type(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataBloodTypeClientResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoMetadataBloodTypeClientResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoMetadataBloodTypeClientResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()