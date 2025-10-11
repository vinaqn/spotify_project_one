from jinja2 import Environment
from connectors.postgres import PostgreSqlClient

class SqlTransform:
    def __init__(self, PostgreSqlClient: PostgreSqlClient, environment: Environment, table_name: str):
        self.engine = PostgreSqlClient.engine
        self.environment = environment
        self.table_name = table_name

        #this loads the sql file
        self.template = self.environment.get_template(f"{table_name}.sql")

    def create_table_as(self) -> None:
        """
        Drops the table if it exists and creates a new copy of the table using the provided select statement.
        """
        exec_sql = f"""
            drop table if exists {self.table_name};
            create table {self.table_name} as (
                {self.template.render()}
            )
        """
        self.engine.execute(exec_sql)
        print(f"{self.table_name} has been created in the database")
    
    