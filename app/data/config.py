from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
BUCKET_NAME = env.str("BUCKET_NAME")
STORAGE_URL = "https://storage.yandexcloud.net"
RECOGNITION_URL = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"
RECOGNITION_API_KEY = env.str("RECOGNITION_API_KEY")
AWS_KEY_ID = env.str("AWS_KEY_ID")
AWS_SECRET_KEY = env.str("AWS_SECRET_KEY")
