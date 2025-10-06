import logging
import time

class PipelineLogger:
    def __init__(self,
                 pipeline_name: str,
                 log_folder_path:str):
        
        self.pipeline_name=pipeline_name
        self.log_folder_path=log_folder_path


        #creating the logger
        logger=logging.getLogger(self.pipeline_name)

        #specifies the lowest-severity log message a logger will capture; will ignore DEBUG messages
        logger.setLevel(logging.INFO)
        
        #set file path to store logs
        self.file_path=f"{self.log_folder_path}/{self.pipeline_name}_{time.time()}.log"


        #format messages
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        #file handler to write log messages to file path; will ignore DEBUG messages
        file_handler = logging.FileHandler(self.file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        #stream handler to write messages to the console in real-time; will ignore DEBUG messages
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        #attach handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        #saves configured logger to be called
        self.logger=logger