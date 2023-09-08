import requests
import stem.process

# API endpoints to request
api_endpoints = [
    "https://api.ktgamez.com/ooredoo/send-otp",
    "https://api.ktgamez.com/ooredoo/validate-otp",
    # Add more endpoints as needed
]

def start_tor():
    return stem.process.launch_tor_with_config(
        config={
            'SocksPort': '9050',
        }
    )

def make_tor_request(endpoint):
    try:
        with requests.Session() as session:
            session.proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
            response = session.get(endpoint)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

def main():
    tor_process = start_tor()

    try:
        for endpoint in api_endpoints:
            response_data = make_tor_request(endpoint)
            if response_data:
                print("Response:", response_data)
    finally:
        tor_process.kill()  # Stop the Tor process when done

if __name__ == "__main__":
    main()
