import requests
import json
import random
import time

api_url = 'https://api.ktgamez.com/ooredoo/send-otp'
numbers_file_path = './numbers.json'
response_file_path = './response.json'

def generate_random_mobile_number():
    return str(random.randint(60000000, 69999999))

def generate_random_otp():
    return str(random.randint(1000, 9999))

def make_post_requests():
    new_mobile_number = generate_random_mobile_number()
    new_otp = generate_random_otp()
    
    with open(response_file_path, 'r') as response_file:
        response_data = json.load(response_file)
    
    response_arr = {
        'mobile': new_mobile_number,
        'otp': new_otp
    }

    try:
        with open(numbers_file_path, 'r') as numbers_file:
            numbers_data = json.load(numbers_file)
            
        if new_mobile_number in numbers_data:
            print('Duplicate number. Generating a new one...')
            return

        numbers_data.append(new_mobile_number)
        with open(numbers_file_path, 'w') as numbers_file:
            json.dump(numbers_data, numbers_file, indent=4)
        
        response = requests.post(api_url, json={'mobile': new_mobile_number})
        print('Response send-otp:', response.json())
        response_arr['send-otp'] = response.json()

        if response.json().get('statusCode') == '200':
            validate_object = {
                'mobile': new_mobile_number,
                'otp': new_otp,
                'transId': response.json()['body']['transId']
            }

            try:
                response2 = requests.post('https://api.ktgamez.com/ooredoo/validate-otp', json=validate_object)
                print(response2.json())
                response_arr['validate-otp'] = response2.json()
            except requests.exceptions.RequestException as err:
                response_arr['validate-otp'] = str(err)
                print('Request error: validate-otp', err)

    except Exception as error:
        response_arr['send-otp'] = str(error)
        print('Request error:', error)
    
    response_data.append(response_arr)
    with open(response_file_path, 'w') as response_file:
        json.dump(response_data, response_file, indent=4)

while True:
    make_post_requests()
    time.sleep(10)  # Sleep for 10 seconds
