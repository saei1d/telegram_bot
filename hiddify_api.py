import uuid
import json
import requests

#    make client

url = "https://dub.barfarazabr.fun/awHquJhtnP/api/v2/admin/user/"

secret_code = "a964952d-17d8-4e77-b1b5-0a42bdb0553c"


def hiddify_api_put(client_code, dayss, limit):
    pk = uuid.uuid4()
    json_str = json.dumps({"pk": pk}, default=str)
    data = json.loads(json_str)
    pk_value = data.get('pk')

    user_data = {
        "added_by_uuid": "80e67893-7490-43e8-aa8b-c8fa5adbb822",
        "mode": "no_reset",
        "name": client_code,
        "package_days": dayss,
        "usage_limit_GB": limit,
        "uuid": pk_value

    }

    response = requests.put(url, json=user_data, auth=(secret_code, ''))

    if response.status_code == 200:
        return hiddify_api_get_conf(pk_value)

    else:
        print("Error adding user", response.status_code, response.reason)



def hiddify_api_get_conf(uuid):

    url = f"https://dub.barfarazabr.fun/gbrBNWz1ma/{uuid}/api/v2/user/all-configs/"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        data_str = json.dumps(data)
        parsed_data = json.loads(data_str)
        first_link = parsed_data[0]['link']
        return first_link
    else:
        print("Error: %s - %s", response.status_code, response.reason)

