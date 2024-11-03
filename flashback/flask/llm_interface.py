import requests

def get_response_for_prompt(prompt):
    response = requests.get("http://xiaoquankong.ai:10990/query", params = {"query_param" : prompt})
    return response.json()['response']