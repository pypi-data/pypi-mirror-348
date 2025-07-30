"""This is a test file to test the new connection to redshift using the roche-datachapter-team-lib library."""
from roche_datachapter_team_lib.db_config import DB_CONFIG
from roche_datachapter_team_lib.db_config import ResultType

QUERY="""SELECT table_schema, table_name
         FROM information_schema.tables
         WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema') LIMIT 5;
        """

df = DB_CONFIG.execute_custom_select_query(QUERY, "redshift", ResultType.PANDAS_DATA_FRAME)
print("Conexión OK, df:", df, "\nShape:", df.shape)
