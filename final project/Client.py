import requests
import base64


def send_request(name, id, hr, mi, ECG_image):
    new_patient = {"medical_record_number": id, "name": name, "medical_image": mi, 'bpm':hr, 'ECG_image':ECG_image}
    r = requests.post('http://127.0.0.1:5000/api/patient_client_upload', json=new_patient)
    return r.status_code, r.text

'''
#patient1 = {"patient_id": "2", "attending_username": "Smith.J", "patient_age": "33"}
#r = requests.post('http://127.0.0.1:5000/api/new_patient', json=patient1)

patient1 = {"patient_id": 2, "heart_rate":150}
r = requests.post('http://127.0.0.1:5000/api/heart_rate', json=patient1)

#patient1 = {"patient_id": 2, "heart_rate":144}
#r = requests.post('http://127.0.0.1:5000/heart_rate', json=patient1)
#r = requests.get('http://127.0.0.1:5000/heart_rate/average/1')
#patient1 = {"patient_id": 2,"heart_rate_average_since": "2021-10-31 22:15:03"}
#r = requests.post('http://127.0.0.1:5000/api/heart_rate/interval_average', json=patient1)

print(r.status_code)
print(r.text)
'''