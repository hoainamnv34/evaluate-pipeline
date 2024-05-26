import json
import requests
import sys
import argparse


def fetchArguments():
    parse = argparse.ArgumentParser(description='Import scan results to DefectDojo')
    parse.add_argument('--host', dest='host')
    parse.add_argument('--product', dest='product_name')
    parse.add_argument('--engagement', dest='engagement_name')
    parse.add_argument('--token', dest='token')

    return parse.parse_args()   


def get_product_id(product_name, token, url):
    headers = {"Accept": "application/json", "Authorization": "Token " + token}

    r = requests.get(url + '/api/v2/products',headers=headers)
    if r.status_code != 200:
        sys.exit(f'Get failed: {r.text}')
    data = json.loads(r.text)
    for product in data['results']:
        if product['name'] == product_name:
            return product['id']
        

def evaluate(product_name, engagement_name, token, url):
    product_id = get_product_id(product_name, token, url)
    if not product_id:
        sys.exit('[ERROR] Not found product')
    else:
        print('[INFO] Product ID:', product_id)


    headers = {"Accept": "application/json", "Authorization": "Token " + token}

    r = requests.get(url + '/api/v2/engagements',headers=headers)
    if r.status_code != 200:
        sys.exit(f'Get failed: {r.text}')
    data = json.loads(r.text)
    for engagement in data['results']:
        if engagement['name'] == engagement_name:
            if engagement['product'] == product_id:
                if engagement['is_successful'] == False:
                    sys.exit('[ERROR] The Pipeline failed')
    


if __name__ == "__main__":
    args = fetchArguments()
    print(args)

    evaluate(args.product_name, args.engagement_name, args.token, args.host)
