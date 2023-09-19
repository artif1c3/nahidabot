import os
import dotenv

dotenv.load_dotenv(dotenv_path="resources/secret.env")

# Used to convert an environment variable to int
def _get_int_env(env_var: str, default: str = None) -> int:
    try:
        print(f'Loading {env_var} (default={default}).')
        if default:
            return int(os.getenv(env_var, default))
        var = os.getenv(env_var)
        if var:
            return int(var)
        else:
            print(f'Environment variable {env_var} was not present!')
            exit(1)
    except KeyError as e:
        print(f'ERROR: {e}')
        exit(1)

class SecretVars:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = _get_int_env('MONGO_PORT', '27017')    # Default port 27017 for mongodb
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'nahida') # Default database nahida for mongodb
    MONGO_USER = os.getenv('MONGO_USER', 'root') # Default admin root
    MONGO_PASS = os.getenv('MONGO_PASS', None)
    if MONGO_PASS is None:
        MONGO_ROOT_PASS = os.getenv('MONGO_ROOT_PASS', 'root')

class AutomationVars:
    DISCORD_CHANNEL = _get_int_env('DISCORD_CHANNEL', 1) # Replace 1 with desired discord channel if Discord Channel not set
    DATATYPE = os.getenv('DATATYPE', 'snippet')
    YOUTUBE_CHANNELID = os.getenv('YOUTUBE_CHANNELID', 'UCiS882YPwZt1NfaM0gR0D9Q') # If youtube channel not set, defaults to Genshin Impact YT