#!/usr/bin/env python3

import os

import dotenv
import requests

dotenv.load_dotenv()
token = os.environ['DO_API_TOKEN']
domain = os.environ['DO_DOMAIN']
subdomain = os.environ['DO_SUBDOMAIN']
print(domain, subdomain)

records_url = f'https://api.digitalocean.com/v2/domains/{domain}/records/'
session = requests.Session()
session.headers = {
    'Authorization': 'Bearer ' + token
}


def get_current_ip():
    ip = requests.get('https://api.ipify.org').text.rstrip()
    print("New ip:", ip)
    return ip


def get_sub_info():
    records = session.get(records_url).json()
    print("Records", records)
    for record in records['domain_records']:
        if record['name'] == subdomain:
            return record


def update_dns():
    current_ip_address = get_current_ip()
    sub_info = get_sub_info()
    print(sub_info)
    subdomain_ip_address = sub_info['data']
    subdomain_record_id = sub_info['id']
    if current_ip_address == subdomain_ip_address:
        print('Subdomain DNS record does not need updating.')
    else:
        response = session.put(records_url + str(subdomain_record_id), json={'data': current_ip_address})
        if response.ok:
            print('Subdomain IP address updated to ' + current_ip_address)
        else:
            print('IP address update failed with message: ' + response.text)


if __name__ == '__main__':
    update_dns()