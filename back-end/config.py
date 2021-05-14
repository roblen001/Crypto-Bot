from dotenv import dotenv_values
env = dotenv_values(".env")

API_KEY = env['API_KEY']
API_SECRET = env['API_SECRET']
