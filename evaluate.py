import json
import requests
import sys
import argparse


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    elif v.lower() in ('none', 'null', ""):
        return None
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def fetchArguments():
    parse = argparse.ArgumentParser(description='Import scan results to DefectDojo')
    parse.add_argument('--host', dest='host')
    parse.add_argument('--project_id', dest='project_id')
    parse.add_argument('--pipeline_run_id', dest='pipeline_run_id')
    parse.add_argument('--latest_request', dest='latest_request',  type=str2bool)

    return parse.parse_args()   

        

def evaluate(host, project_id, pipeline_run_id, latest_request):


    params = {
        'project_id': project_id,
        'pipeline_run_id': pipeline_run_id,
        'latest_request': str(latest_request).lower()
    }
    headers = {'accept': 'application/json'}
    url = f"{host}/api/pipeline-runs/evaluate"

    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        sys.exit(f'Get failed: {r.text}')
    data = json.loads(r.text)
    if not data.get('data', {}).get('evaluate', True):
        sys.exit(f'[ERROR] The Pipeline failed: {data.get("data")}')
    


if __name__ == "__main__":
    args = fetchArguments()
    print(args)

    evaluate(args.host, args.project_id, args.pipeline_run_id, args.latest_request)
