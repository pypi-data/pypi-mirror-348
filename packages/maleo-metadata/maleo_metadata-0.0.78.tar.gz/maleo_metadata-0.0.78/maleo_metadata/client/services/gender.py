from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.client.controllers import MaleoMetadataGenderControllers
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.models.transfers.parameters.general.gender import MaleoMetadataGenderGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.gender import MaleoMetadataGenderClientParametersTransfers
from maleo_metadata.models.transfers.results.client.gender import MaleoMetadataGenderClientResultsTransfers
from maleo_metadata.types.results.client.gender import MaleoMetadataGenderClientResultsTypes

class MaleoMetadataGenderClientService(ClientService):
    def __init__(self, logger, controllers:MaleoMetadataGenderControllers):
        super().__init__(logger)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoMetadataGenderControllers:
        raise self._controllers

    async def get_genders(
        self,
        parameters:MaleoMetadataGenderClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataGenderClientResultsTypes.GetMultiple:
        """Retrieve genders from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving genders",
            logger=self._logger,
            fail_result_class=MaleoMetadataGenderClientResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataGenderClientResultsTransfers.Fail(message=message, description=description)
            #* Retrieve genders using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_genders(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataGenderClientResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoMetadataGenderClientResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                if controller_result.content["data"] is None:
                    return MaleoMetadataGenderClientResultsTransfers.NoData.model_validate(controller_result.content)
                else:
                    return MaleoMetadataGenderClientResultsTransfers.MultipleData.model_validate(controller_result.content)
        return await _impl()

    async def get_gender(
        self,
        parameters:MaleoMetadataGenderGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataGenderClientResultsTypes.GetSingle:
        """Retrieve gender from MaleoMetadata"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving gender",
            logger=self._logger,
            fail_result_class=MaleoMetadataGenderClientResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoMetadataGenderClientResultsTransfers.Fail(message=message, description=description)
            #* Retrieve gender using chosen controller
            if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_gender(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoMetadataGenderClientResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoMetadataGenderClientResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoMetadataGenderClientResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()