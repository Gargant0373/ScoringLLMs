import re
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import docker

from utils import write_header_if_empty, append_to_csv

class ModelConfig:
    def __init__(
        self,
        model_name="",
        instance_description="",
        container_name='ollama',
        container_id=None,
        results_dir=None,
        results_header=None,
        logging_dir=None,
    ):
        self.name = model_name
        self.instance_description = instance_description
        self.container_id = container_id
        self.container_name = container_name

        load_dotenv()
        self.results_header = results_header
        self.results_dir = results_dir
        if self.results_dir is None:
            self.results_dir = os.getenv('RESULTS_DIR')
        self.fps = {}
        self._setup_output_file()

        self.logging_dir = logging_dir
        if self.logging_dir is None:
            self.logging_dir = os.getenv('LOG_DIR')

        # Setup logging
        self.logger = self._setup_logging()

        # Load docker image
        self._load_model()

    #
    # Public methods
    #

    # Add another output file to the config
    def add_outfile(self, filename_addition):
        if filename_addition == "":
            base_fp = f"{self.name}-{self.instance_description}"
        else:
            base_fp = f"{self.name}-{self.instance_description}-{filename_addition}"
        if filename_addition in self.fps:
            raise ValueError(f"File {base_fp} already present!")
        
        result_file_path = os.path.join(self.results_dir, f"{base_fp}-{self.count}.csv")
        
        self.fps[filename_addition] = result_file_path

        if self.results_header[filename_addition] is not None:
            write_header_if_empty(result_file_path, self.results_header[filename_addition])

        return result_file_path

    # Write to desired file
    def write(self, contents, addition=""):
        append_to_csv(self.fps[addition], contents)

    #
    # Private methods
    #
    def _setup_logging(self):
        # Ensure the log directory exists
        os.makedirs(self.logging_dir, exist_ok=True)

        # Create a custom logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)  # Set the base level to DEBUG to capture all messages

        # Create handlers
        log_filename = f"{self.name}-{datetime.now().strftime('%d-%m-%Y')}.log"
        file_handler = logging.FileHandler(os.path.join(self.logging_dir, log_filename))
        file_handler.setLevel(logging.DEBUG)  # Log all messages to the file

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Log only INFO and above to the console

        # Create formatters and add them to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


    def _load_model(self):
        client = docker.from_env()

        if self.container_name is None and self.container_id is None:
            raise ValueError("Both container id and name cannot be none!")

        call_id = self.container_id if self.container_id is not None else self.container_name

        try:
            container = client.containers.get(call_id)

            if container.status != 'running':
                print(f"Starting container {call_id}")
                container.start()
                container.reload()

            print(f"Executing ollama run {self.name}")
            container.exec_run(f"ollama run {self.name}")
        except docker.errors.NotFound:
            print(f"Container {call_id} not found!")
        except docker.errors.APIError as e:
            print(f"Error occurred starting container: {e}")

    def _setup_output_file(self, addition=""):
        # Create the directory if it doesn't exist
        os.makedirs(self.results_dir, exist_ok=True)

        pattern = re.compile(fr'{self.name}-{self.instance_description}-\d+\.csv')
        self.count = len([name for name in os.listdir(self.results_dir) if pattern.match(name)])

        return self.add_outfile("")
