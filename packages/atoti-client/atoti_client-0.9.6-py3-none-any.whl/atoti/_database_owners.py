from collections.abc import Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_not_none import check_data_model_not_none
from ._collections import DelegatingMutableSet
from ._graphql_client import UpdateDatabaseInput, UpdateDataModelInput
from ._identification import Role
from ._require_live_extension import require_live_extension
from ._transaction import get_data_model_transaction_id


@final
class DatabaseOwners(DelegatingMutableSet[Role]):
    def __init__(self, *, atoti_client: AtotiClient) -> None:
        self._atoti_client: Final = atoti_client

    @override
    def _get_delegate(self) -> AbstractSet[Role]:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        output = graphql_client.get_database_owners(
            data_model_transaction_id=data_model_transaction_id
        )
        data_model = check_data_model_not_none(
            output.data_model,
            data_model_transaction_id=data_model_transaction_id,
        )
        return set(data_model.database.owners)

    @override
    def _set_delegate(self, new_set: AbstractSet[Role], /) -> None:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        mutation_input = UpdateDataModelInput(
            data_model_transaction_id=data_model_transaction_id,
            database=UpdateDatabaseInput(owners=list(new_set)),
        )
        graphql_client.update_data_model(mutation_input)
