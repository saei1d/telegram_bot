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
    print('lkjhgfdfghjkl')
    user_data = {
        "added_by_uuid": "80e67893-7490-43e8-aa8b-c8fa5adbb822",
        "mode": "no_reset",
        "name": mmd,
        "package_days": dayss,
        "usage_limit_GB": limit,
        "uuid": pk_value

    }
    proxy_path_client = "gbrBNWz1ma"
    proxy_path_admin = "awHquJhtnP"
    url1 = f"https://dub.barfarazabr.fun/{proxy_path_admin}/"
    secret_code = "a964952d-17d8-4e77-b1b5-0a42bdb0553c"
    url = f'{url1}api/v2/admin/user/'
    url5 = f"https://dub.barfarazabr.fun/{proxy_path_client}/"

    response_get = requests.get(url, auth=(secret_code, ''))
    lennnn = len(response_get.json())
    if lennnn >= 250:
        proxy_path_client = "nCbhYTw45iU17uynCnusqg3F"
        proxy_path_admin = "KmEnSzHyFdmJO9sfbMo8790ckxuie"
        url1 = f"https://wub.jimboserver1.fun/{proxy_path_admin}/"
        url = f'{url1}api/v2/admin/user/'
        url5 = f"https://wub.jimboserver1.fun/{proxy_path_client}/"
        secret_code = "c7e64d9b-812b-43f9-aa8b-b8ba1cd1158b"

    response_put = requests.put(url, json=user_data, auth=(secret_code, ''))

    if response_put.status_code == 200:
        return hiddify_api_get_conf(pk_value, url5)

    else:
        print("Error adding user", response_put.status_code, response_put.reason)


def hiddify_api_get_conf(uuid, url5):
    url = f"{url5}{uuid}/api/v2/user/all-configs/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        data_str = json.dumps(data)
        parsed_data = json.loads(data_str)
        first_link = parsed_data[0]['link']
        print(parsed_data)
        return first_link


#              configs


def show_configs(chat_id):
    user_configs = []
    url = "https://dub.barfarazabr.fun/awHquJhtnP/api/v2/admin/user/"
    secret_code = "a964952d-17d8-4e77-b1b5-0a42bdb0553c"
    url2 = "https://wub.jimboserver1.fun/KmEnSzHyFdmJO9sfbMo8790ckxuie/api/v2/admin/user/"
    secret_code2 = "c7e64d9b-812b-43f9-aa8b-b8ba1cd1158b"
    response = requests.get(url, auth=(secret_code, ''))
    response2 = requests.get(url2, auth=(secret_code2, ''))
    if response.status_code == 200:
        data = response.json()
        data_str = json.dumps(data)
        parsed_data = json.loads(data_str)

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
                url5 = f"https://dub.barfarazabr.fun/gbrBNWz1ma/"
                uuid = user['uuid']
                link = hiddify_api_get_conf(uuid, url5)
                message = f'لینک دسترسی:{link} \n استفاده فعلی: {current_usages}  \n سقف مصرف:{rounded_usage_limit} GB روزهای باقی مانده: {pakages_date}\n\n تاریخ شروع: {start_date}\n\n کد شناسایی: {uuid}'
                user_configs.append(message)

    if response2.status_code == 200:
        data2 = response2.json()
        data2_str = json.dumps(data2)
        parsed_data2 = json.loads(data2_str)

        for user2 in parsed_data2:
            name_value = user2['name']
            if str(name_value) == str(chat_id):
                current_usages = user2['current_usage_GB']
                usage_limit = user2['usage_limit_GB']
                rounded_usage_limit = round(usage_limit, 2)  # گرد کردن به دو رقم اعشار
                pakages_date = user2['package_days']
                start_date = user2['start_date']
                if start_date is None:
                    start_date = "هنوز شروع به استفاده نکردید"
                url5 = f"https://wub.jimboserver1.fun/nCbhYTw45iU17uynCnusqg3F/"
                uuid2 = user2['uuid']
                link2 = hiddify_api_get_conf(uuid2, url5)
                message = f'لینک دسترسی:{link2} \n استفاده فعلی: {current_usages}  \n سقف مصرف:{rounded_usage_limit} GB روزهای باقی مانده: {pakages_date}\n\n تاریخ شروع: {start_date}\n\n کد شناسایی: {uuid2}'
                user_configs.append(message)
    else:
        print("Error adding user", response2.status_code, response.reason)
    return user_configs
