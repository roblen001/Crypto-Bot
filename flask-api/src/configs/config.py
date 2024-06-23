from dotenv import dotenv_values
env = dotenv_values("../../.env")

API_KEY = env['API_KEY']
API_SECRET = env['API_SECRET']

TEST_API_KEY = env['TEST_API_KEY']
TEST_SECRET_KEY = env['TEST_SECRET_KEY']

PERSONAL_EMAIL = env['PERSONAL_EMAIL']
DEV_EMAIL = env['DEV_EMAIL']
EMAIL_PASS = env['EMAIL_PASS']

TAAPI = env['TAAPI']