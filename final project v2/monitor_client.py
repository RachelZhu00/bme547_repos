import requests
import base64
import json

server_name = 'http://127.0.0.1:5000'


def request_patient_info(mrn):
    path = server_name+'/api/get_info/'+mrn
    r = requests.get(path)
    answer = r.text
    answer = json.loads(answer)
    return answer

def get_nums():
    path = server_name + '/api/all_patient_num'
    r = requests.get(path)
    answer = r.text
    answer = json.loads(answer)
    return answer


def main():
    get_nums()
    request_patient_info(12)


if __name__ == '__main__':
    main()