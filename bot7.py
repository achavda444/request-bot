import requests
import json
import random
import time
import psutil

api_url = 'https://api.ktgamez.com/ooredoo/send-otp'
numbers_file_path = './new_numbers.json'  # Path to the numbers JSON file
response_file_path = './response.json'

def generate_random_mobile_number():
    return str(random.randint(60000000, 69999999))

def generate_random_otp():
    return str(random.randint(1000, 9999))

def start_tor():
    # Kill existing Tor processes on the specified port (e.g., 9050)
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "tor.exe" in process.info['name']:
            try:
                process.kill()
            except psutil.NoSuchProcess:
                pass

def make_post_requests():
    new_mobile_number = generate_random_mobile_number()
    new_otp = generate_random_otp()
    timestamp = int(time.time())

    start_tor()  # Start a new Tor session for each request

    response_data = json.loads(open(response_file_path, 'r').read())
    response_arr = {
        'mobile': new_mobile_number,
        'timestamp': timestamp,
    }

    try:
        with open(numbers_file_path, 'r') as numbers_file:
            numbers_data = json.load(numbers_file)
            print(len(numbers_data))

            for entry in numbers_data:
                if entry['number'] == new_mobile_number:
                    print('Duplicate number. Generating a new one...')
                    return  # Exit the function if a duplicate number is found

        new_number_entry = {
            'number': new_mobile_number,
            'timestamp': timestamp,
        }

        numbers_data.append(new_number_entry)
        with open(numbers_file_path, 'w') as numbers_file:
            json.dump(numbers_data, numbers_file, indent=4)

        # Make the request using a SOCKS proxy
        session = requests.Session()
        session.proxies = {
            'http': 'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050',
        }

        response = session.post(api_url, data={'mobile': new_mobile_number})
        response_arr['send-otp'] = response.json()

        if response.json().get('statusCode') == '200':
            validate_object = {
                'mobile': '965' + new_mobile_number,
                'otp': new_otp,
                'transId': response.json()['body']['transId'],
            }

            try:
                response2 = session.post('https://api.ktgamez.com/ooredoo/validate-otp', json=validate_object)
                response_arr['validate-otp'] = response2.json()
            except Exception as err:
                response_arr['validate-otp'] = str(err)
                print('Request error: validate-otp', str(err))
            finally:
                session.close()
    except Exception as error:
        response_arr['send-otp'] = str(error)
        print('Request error:', str(error))
    finally:
        response_data.append(response_arr)
        with open(response_file_path, 'w') as response_file:
            json.dump(response_data, response_file, indent=4)

# Run the loop every 10 seconds
while True:
    make_post_requests()
    time.sleep(10)
