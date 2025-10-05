from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.dialects import postgresql

class PosgreSqlClient:
    """a client to connect to a postgresql database"""
    
    def __init__(self,
                 server_name: str,
                 database_name:str, 
                 username: str,
                 password: str,
                 port: int =5432
                 ):
        
        #set the database details
        self.host_name=server_name
        self.database_name=database_name
        self.username=username
        self.password=password
        self.port=port

        #connection url to pass into create engine
        connection_url = URL.create(
            drivername="postgresql+pg8000",
            username=username,
            password=password,
            host=server_name,
            port=port,
            database=database_name,
        )

        #engine
        try: 
            self.engine=create_engine(connection_url)
            print("Database connected")
        except:
            print("Did not connect to database")