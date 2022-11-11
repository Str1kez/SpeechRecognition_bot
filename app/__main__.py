from time import sleep
import boto3
import requests as r

bucket_name = ''
url = 'https://storage.yandexcloud.net'
Recognition_API_KEY = ''
AWS_KEY_ID = ''
AWS_SECRET_KEY = ''

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url=url,
    region_name='ru-central1',
    aws_access_key_id='',
    aws_secret_access_key='',
)

# Создать новый бакет
# s3.create_bucket(Bucket='bucket-name')

# Загрузить объекты в бакет

## Из строки
# s3.put_object(Bucket='bucket-name', Key='object_name', Body='TEST', StorageClass='COLD')

## Из файла
name = ''
s3.upload_file('audio_2022-11-11_04-32-27.ogg', '', name)
# s3.upload_file('this_script.py', 'bucket-name', 'script/py_script.py')

# Получить список объектов в бакете
# for key in s3.list_objects(Bucket='bucket-name')['Contents']:
    # print(key['Key'])

# Удалить несколько объектов
# forDeletion = [{'Key':'object_name'}, {'Key':'script/py_script.py'}]
# response = s3.delete_objects(Bucket='bucket-name', Delete={'Objects': forDeletion})

# Получить объект
# get_object_response = s3.get_object(Bucket=bucket_name, Key='test')
# print(get_object_response)

header = {"Authorization": f"Api-Key {Recognition_API_KEY}"}
url_object = url + '/' + bucket_name + '/' + name
data = {
        "config": {
        "specification": {
            "languageCode": "ru-RU",
            "model": "general",
            "profanityFilter": False,
            "audioEncoding": "OGG_OPUS",
            "sampleRateHertz": 48000
        }
    },
        'audio': {
        'uri': url_object
    }
}

response = r.post(url='https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize',
                  headers=header,
                  json=data)

operation_id = response.json().get('id')
# operation_id = 'e039vd70gp9vlcllaa3a'

sleep(10)

response = r.get(url=f'https://operation.api.cloud.yandex.net/operations/{operation_id}',
                 headers=header)

response_data = response.json()

if response_data.get('done'):
    s = ' '.join(chunk['alternatives'][0]['text'] for chunk in response_data['response']['chunks'])

print(s)
