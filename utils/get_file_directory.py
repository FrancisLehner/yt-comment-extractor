from dotenv import load_dotenv
import os

load_dotenv()


def get_file_directory():
    file_directory = os.getenv('directory')
    return file_directory
