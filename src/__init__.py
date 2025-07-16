from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env.secrets"))
load_dotenv(find_dotenv(".env.config"))
