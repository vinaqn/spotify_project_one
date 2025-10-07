from sqlalchemy import create_engine
from sqlalchemy.engine import URL

class PostgreSqlClient:
    """a client to connect to a postgresql database"""
    
    def __init__(self,
                 db_server_name: str,
                 db_database_name:str, 
                 db_username: str,
                 db_password: str,
                 db_port: int =5432
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
            database=db_database_name,
        )

        #engine
        try: 
            self.engine=create_engine(connection_url)

            with self.engine.connect() as connection:
                    connection.execute("SELECT 1")
                    print("Connection is alive and responsive.")
        
        except:
             print("Could not connect to the database. Check your connection string.")

<<<<<<< HEAD
=======
        

>>>>>>> 2d1bee272d193988675377c1da45c3584fea54f0
