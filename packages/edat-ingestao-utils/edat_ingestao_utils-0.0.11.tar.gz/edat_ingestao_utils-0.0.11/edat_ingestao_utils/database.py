import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table
from sqlalchemy.engine.base import Engine as sql_engine
from sqlalchemy.ext.automap import automap_base


def upsert_database(df_input: pd.DataFrame, engine: sql_engine, table: str, schema: str) -> None:
    """
    Realiza um upsert dos dados contidos no dataframe 'df_input' para a tabela 'table'
    :param self:
    :param df_input: dataframe com dados a serem salvos/atualizados
    :param engine: engine do bd
    :param table: tabela do bd a ser atualizada
    :param schema: esquema do bd
    :return:
    """

    if df_input is None or len(df_input) == 0:
        return None
    flattened_input = df_input.to_dict('records')
    with engine.connect() as conn:
        base = automap_base()
        base.prepare(engine, reflect=True, schema=schema)
        target_table = Table(table, base.metadata,
                             autoload=True, autoload_with=engine, schema=schema)
        chunks = [flattened_input[i:i + 1000] for i in range(0, len(flattened_input), 1000)]
        for chunk in chunks:
            stmt = insert(target_table).values(chunk)
            update_dict = {c.name: c for c in stmt.excluded if not c.primary_key}
            conn.execute(stmt.on_conflict_do_update(
                constraint=f'{table}_pk',
                set_=update_dict)
            )