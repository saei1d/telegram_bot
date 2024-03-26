import uuid
import json
import requests


#                                         make client


def hiddify_api_put(client_code, dayss, limit):
    pk = uuid.uuid4()
    json_str = json.dumps({"pk": pk}, default=str)
    data = json.loads(json_str)
    pk_value = data.get('pk')
    mmd = str(client_code)
    user_data = {
        "added_by_uuid": "80e67893-7490-43e8-aa8b-c8fa5adbb822",
        "mode": "no_reset",
        "name": mmd,
        "package_days": dayss,
        "usage_limit_GB": limit,
        "uuid": pk_value

    }
    url = "https://dub.barfarazabr.fun/awHquJhtnP/api/v2/admin/user/"
    secret_code = "a964952d-17d8-4e77-b1b5-0a42bdb0553c"

    response = requests.put(url, json=user_data, auth=(secret_code, ''))

    if response.status_code == 200:
        return hiddify_api_get_conf(pk_value)

    else:
        print("Error adding user", response.status_code, response.reason)


#        get config
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


#              configs


def show_configs(chat_id):
    url = "https://dub.barfarazabr.fun/awHquJhtnP/api/v2/admin/user/"
    secret_code = "a964952d-17d8-4e77-b1b5-0a42bdb0553c"
    response = requests.get(url, auth=(secret_code, ''))
    if response.status_code == 200:
        data = response.json()
        data_str = json.dumps(data)
        parsed_data = json.loads(data_str)
        user_configs = []

        for user in parsed_data:
            name_value = user['name']
            if str(name_value) == str(chat_id):
                current_usages = user['current_usage_GB']
                usage_limit = user['usage_limit_GB']
                rounded_usage_limit = round(usage_limit, 2)  # گرد کردن به دو رقم اعشار
                pakages_date = user['package_days']
                start_date = user['start_date']
                if start_date is None:
                    start_date = "هنوز شروع به استفاده نکردید"

                uuid = user['uuid']
                link = hiddify_api_get_conf(uuid)
                message = f"استفاده فعلی: {current_usages} GB\nسقف مصرف:  لینک دسترسی:{link}   \n{rounded_usage_limit} GB\n روزهای باقی مانده: {pakages_date}\n\n تاریخ شروع: {start_date}\nکد uuid: {uuid}"
                user_configs.append(message)
        print(user_configs)
        return user_configs
    else:
        print("Error adding user", response.status_code, response.reason)
