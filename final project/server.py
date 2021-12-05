from flask import Flask, request, jsonify
import logging
from datetime import datetime
import requests
import urllib
from ecg import get_bpm
from pymodm import connect, MongoModel, fields
from pymodm import errors as pymodm_errors
import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

# Define variable to contain Flask class for server
app = Flask(__name__)

format = "%Y-%m-%d %H:%M:%S"
time = datetime.now().strftime(format)

class Patient(MongoModel):
    medical_record_number = fields.CharField(primary_key=True)
    name = fields.CharField()
    medical_image = fields.ListField()
    mi_time = fields.ListField()
    bpm = fields.ListField()
    ECG_image = fields.ListField()
    ECG_time = fields.ListField()


def initialize_server():
    connect('mongodb+srv://qz125:2747Reign@bme547.a9zto.'
            'mongodb.net/bme547project?retryWrites=true&w=majority')
    print("connected!")


@app.route("/", methods=["GET"])
def server_status():
    """Used to indicate that the server is running
    """
    return "Server is on"


@app.route("/api/patient_client_upload", methods=["POST"])
def patient_client_upload():
    """Implements /new_patient route for adding a new patient to server
    database
    The /new_patient route is a POST request that should receive a JSON-encoded
    string with the following format:
    {"name": str, "id": int, "blood_type": str}
    The function then calls validation functions to ensure that the needed
    keys and data types exist in the received JSON, then calls a function to
    add the patient data to the database.  The function then returns to the
    caller either a status code of 200 and the patient info if it was
    successfully added, or a status code of 400 and an error message if there
    was a validation problem.
    Returns:
        str, int: message including patient data if successfully added to the
                  database or error message if not, followed by a status code
    """
    format = "%Y-%m-%d %H:%M:%S"
    time = datetime.now().strftime(format)
    in_data = request.get_json()
    check_mrn(in_data)
    mrn = in_data["medical_record_number"]
    patient = has_patient(mrn)

    if patient is False:
        new_patient = add_new_patient(in_data)
        patient = add_info(new_patient, in_data, time)
    else:
        patient = add_info(patient, in_data, time)
    return "Patient info added {}".format(patient)


def int_convert(in_data):
    for key in in_data:
        try:
            in_data[key] = int(in_data[key])
        except ValueError:
            in_data[key] = in_data[key]
    return in_data


def has_patient(mrn):
    try:
        db_item = Patient.objects.raw({"_id": mrn}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return db_item


def check_mrn(in_data):
    if in_data["medical_record_number"] is None:
        return "Please enter the medical record number"


def add_new_patient(in_data):
    """Creates new patient database entry
    This function receives information about the patient, creates a dictionary,
    and appends that dictionary to the database list.  The patient dictionary
    has the following format:
    {"name": str, "id_no": int, "blood_type": str, "tests": list}
    The "tests" list is initialized as an empty list while the values for the
    other keys are taken from the input parameters.  After the new patient
    is added, the database is printed to the console for debugging purposes.
    The created dictionary is returned to enable this function to be tested.
    Args:
        patient_name (str): name of patient
        id_no (int):  patient id number, usually a medical record number
        blood_type (str):  patient blood type, ex. "AB+"
    Returns:
        dict: the patient database entry
    """
    new_patient = Patient(medical_record_number=in_data["medical_record_number"])
    new_patient.save()
    return new_patient


def add_info(patient, in_data, time):
    if in_data["name"] != '':
        patient.name = in_data['name']
    if in_data["medical_image"] != '':
        patient.medical_image.append(in_data["medical_image"])
        patient.mi_time.append(time)
    if in_data["ECG_image"] != '':
        patient.bpm.append(in_data["bpm"])
        patient.ECG_image.append(in_data['ECG_image'])
        patient.ECG_time.append(time)
    patient.save()
    return patient


def validate_input_type(input_data, expected_keys):
    """ This function will validate the types of input data and types of
    each key in the input dictionary. It will help avoid server error.
    The expected types are:
    input_data: dict
    {"attending_username": str,
     "attending_email": str,
     "attending_phone": str}
     Args:
         input_data (any type): a JSON got from the client
         expected_keys (dict): a dictionary containing expected type for
         each key
    Returns:
        str or bool, int: if validation is successful, return True, 200.
        if validation is failed, return error string, 400
    """
    if type(input_data) is not dict:
        return "The input is not a dictionary", 400
    for key in expected_keys:
        if key not in input_data:
            return "The key {} is missing.".format(key), 400
        if type(input_data[key]) is not expected_keys[key]:
            return "The key {} has the wrong type.".format(key), 400
    return True, 200

@app.route("/api/all_patient_num", methods=["GET"])
def get_all_patient_num():
    results = Patient.objects.raw({})
    answer = []
    for item in results:
        answer.append(item.medical_record_number)
    return jsonify(answer)


@app.route("/api/get_info/<patient_id>", methods=["GET"])
def get_patient_info(patient_id):
    patient_id = int(patient_id)
    patient = has_patient(patient_id)
    if patient is not False:
        answer = generate_output(patient)
        return jsonify(answer)
    else:
        return "Patient Not Found"


def has_patient(mrn):
    try:
        db_item = Patient.objects.raw({"_id": mrn}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return db_item


def generate_output(patient):
    output_dict = {"MRN": patient.medical_record_number,
                   "name": patient.name,
                   "HR": patient.bpm,
                   "ecg_images": patient.ECG_image,
                   "ecg_time": patient.ECG_time,
                   "medical_images": patient.medical_image,
                   "mi_time": patient.mi_time
    }
    return output_dict

if __name__ == '__main__':
    initialize_server()
    app.run()
