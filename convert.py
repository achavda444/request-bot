import csv

input_file_path = 'Free_Proxy_List.txt'
output_file_path = 'output.txt'

def extract_ips(input_file_path, output_file_path):
    ips = []

    with open(input_file_path, 'r', encoding='utf-8') as input_file:  # Specify encoding
        csv_reader = csv.reader(input_file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            ip = row[0].strip('"')  # Extract the first column and remove double quotes
            ips.append(ip)

    with open(output_file_path, 'w') as output_file:
        for ip in ips:
            output_file.write(ip + '\n')

if __name__ == '__main__':
    extract_ips(input_file_path, output_file_path)
