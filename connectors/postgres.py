from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import URL
from assets.pipeline_logger import PipelineLogger

class PostgreSqlClient:
    """a client to connect to a postgresql database"""
    
    def __init__(self,
                 db_server_name: str,
                 db_database_name:str, 
                 db_username: str,
                 db_password: str,
                 logger: PipelineLogger,
                 db_port: int =5432,
                 ):
        
        #set the database details
        self.host_name=db_server_name
        self.database_name=db_database_name
        self.username=db_username
        self.password=db_password
        self.port=db_port

        #connection url to pass into create engine
        connection_url = URL.create(
            drivername="postgresql+pg8000",
            username=db_username,
            password=db_password,
            host=db_server_name,
            port=db_port,
            database=db_database_name
        )

        #engine
        try: 
            self.engine=create_engine(connection_url,connect_args={"ssl_context": True}, pool_pre_ping=True, echo=False)

            with self.engine.connect() as connection:
                    connection.execute("SELECT 1")

                    logger.logger.info(f"Connection is alive and responsive.")
                
        
        except:
             logger.logger.error(f"Could not connect to database.")

    #Creates tables provided in the metadata object"
    def create_all_tables(self, metadata: MetaData) -> None:
        metadata.create_all(self.engine)


        

