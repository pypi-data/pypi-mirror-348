from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_not_none import check_data_model_not_none, check_named_object_not_none
from ._collections import (
    DelegatingKeyDisambiguatingMapping,
    SupportsUncheckedMappingLookup,
)
from ._identification import ColumnIdentifier, ColumnName, TableIdentifier
from ._require_live_extension import require_live_extension
from ._transaction import get_data_model_transaction_id
from .column import Column


@final
class Columns(
    SupportsUncheckedMappingLookup[ColumnName, ColumnName, Column],
    DelegatingKeyDisambiguatingMapping[ColumnName, ColumnName, Column],
):
    def __init__(
        self, *, atoti_client: AtotiClient, table_identifier: TableIdentifier
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._table_identifier: Final = table_identifier

    @override
    def _create_lens(self, key: ColumnName, /) -> Column:
        return Column(
            ColumnIdentifier(self._table_identifier, key),
            atoti_client=self._atoti_client,
        )

    @override
    def _get_unambiguous_keys(self, *, key: ColumnName | None) -> list[ColumnName]:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        data_model_transaction_id = get_data_model_transaction_id()

        if key is None:
            output = graphql_client.get_table_columns(
                data_model_transaction_id=data_model_transaction_id,
                table_name=self._table_identifier.table_name,
            )
            data_model = check_data_model_not_none(
                output.data_model,
                data_model_transaction_id=data_model_transaction_id,
            )
            table = check_named_object_not_none(
                data_model.database.table,
                "table",
                self._table_identifier.table_name,
            )
            return [column.name for column in table.columns]

        output = graphql_client.find_column(  # type: ignore[assignment] # See https://github.com/python/mypy/issues/12968.
            column_name=key,
            data_model_transaction_id=data_model_transaction_id,
            table_name=self._table_identifier.table_name,
        )
        data_model = check_data_model_not_none(
            output.data_model,
            data_model_transaction_id=data_model_transaction_id,
        )
        table = check_named_object_not_none(
            data_model.database.table,
            "table",
            self._table_identifier.table_name,
        )
        column = check_named_object_not_none(  # type: ignore[var-annotated]
            table.column,  # type: ignore[attr-defined]
            "column",
            key,
            error_type=KeyError,
        )
        return [column.name]
