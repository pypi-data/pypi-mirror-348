import aiohttp
import asyncio
import sys
import base64
import os
import json

class epic_client():
    def __init__(self):
        self.launcherAppClient2 = ('34a02cf8f4414e29b15921876da36f9a', 'daafbccc737745039dffe53d94fc76cf')
        self.uefn = ('3e13c5c57f594a578abe516eecb673fe', '530e316c337e409893c55ec44f22cd62')
        self.fortniteAndroidGameClient = ('3f69e56c7649492c8cc29f1af08a8a12', 'b51ee9cb12234f50a69efa67ef53812e')
        self.fortniteSwitchGameClient = ('5229dcd3ac3845208b496649092f251b', 'e3bd2d3e-bf8c-4857-9e7d-f3d947d220c7')
        self.fortniteIosGameClient = ('af43dc71dd91452396fcdffbd7a8e8a9', '4YXvSEBLFRPLh1hzGZAkfOi5mqupFohZ')

        self.choice = {
            'LauncherAppClient2': self.launcherAppClient2,
            'UEFN': self.uefn,
            'FortniteAndroidGameClient': self.fortniteAndroidGameClient,
            'fortniteSwitchGameClient': self.fortniteSwitchGameClient,
            'fortniteIosGameClient': self.fortniteIosGameClient
        }

if sys.platform.startswith("win"):
    import asyncio.proactor_events
    from asyncio.proactor_events import _ProactorBasePipeTransport

    def silent_close(self):
            try:
                if self._loop.is_closed():
                    return
                self._loop.call_soon(self._call_connection_lost, None)
            except Exception:
                pass

    _ProactorBasePipeTransport.__del__ = silent_close

class fnclient:
    _config_data = {}

    @staticmethod
    def config(func):
        def wrapper(*args, **kwargs):
            if 'exchange_code' in kwargs:
                fnclient._config_data['exchange_code'] = kwargs['exchange_code']
            if 'authorization_code' in kwargs:
                fnclient._config_data['authorization_code'] = kwargs['authorization_code']
            if 'device_auth' in kwargs:
                fnclient._config_data['device_auth'] = kwargs['device_auth']
            if 'client' in kwargs:
                fnclient._config_data['client'] = kwargs['client']
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def access_token(func):
        async def get_token():
            data = fnclient._config_data
            if 'client' not in data:
                raise Exception("you have not configured your client")

            client_id, client_secret = epic_client().choice[data['client']]
            auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            payload = {}

            if "exchange_code" in data:
                payload = {
                    "grant_type": "exchange_code",
                    "exchange_code": data["exchange_code"],
                    "token_type": "eg1"
                }
                headers["Authorization"] = f"Basic {auth}"

            elif "authorization_code" in data:
                payload = {
                    "grant_type": "authorization_code",
                    "code": data["authorization_code"],
                }
                headers["Authorization"] = f"Basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="

            elif "device_auth" in data:
                device = data["device_auth"]
                payload = {
                    "grant_type": "device_auth",
                    "account_id": device["account_id"],
                    "device_id": device["device"],
                    "secret": device["secret"]
                }
                headers["Authorization"] = f"Basic {auth}"

            else:
                raise Exception("Aucune méthode d'authentification fournie.")

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
                    data=payload,
                    headers=headers
                ) as resp:
                    response_json = await resp.json()
                    return response_json.get("access_token"), response_json.get('account_id')

        def wrapper(*args, **kwargs):
            return asyncio.run(get_token())
        return wrapper
    
    @staticmethod
    def create_device(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        device_id = data.get("deviceId")
                        secret = data.get("secret")
                        if device_id and secret:
                            return account_id, device_id, secret
            return None, None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

    @staticmethod
    def device_info(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and device_id required.")
            access_token, account_id, device_id = args[0], args[1], args[2]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth/{device_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
        
    @staticmethod
    def device_list(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id and device_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth/"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def lookup_id(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def stat_alltime(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/stats/accountId/{account_id}/bulk/window/alltime"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def friend_list(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def add_friend(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends/{friend_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as resp:
                    if resp.status == 204:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def delete_friend(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id and friend_id required.")
            access_token, account_id, friend_id = args[0], args[1], args[2]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends/{friend_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    if resp.status == 204:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def clear_friend_list(func):
        async def inner(*args, **kwargs):
            if len(args) < 3:
                raise ValueError("access_token and account_id required.")
            access_token, account_id = args[0], args[1]
            url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account_id}/friends/"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    if resp.status == 204:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

    @staticmethod
    def lookup_display(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id required.")
            access_token, displayName = args[0], args[1]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/displayName/{displayName}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data
            return f"{displayName} was not found"

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def update_account(func):
        async def inner(*args, **kwargs):
            if len(args) < 2:
                raise ValueError("access_token and account_id and payload required.")
            access_token, account_id, payload = args[0], args[1], args[2]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json=payload) as resp:
                    if resp:
                        data = await resp.json()
                        return data
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def generate_exchange_code(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def acceptEula(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/corrections/acceptEula"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json={"continuation": ""}) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def acceptPrivacyPolicy(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/corrections/acceptPrivacyPolicy"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json={"continuation": ""}) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper


    @staticmethod
    def CancelAccountDeletion(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/corrections/cancelPendingDeletion"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json={"continuation": ""}) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper

    @staticmethod
    def ConfirmDisplayName(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/corrections/confirmDisplayName"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json={"continuation": ""}) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('code')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def fortnite_status(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://lightswitch-public-service-prod.ol.epicgames.com/lightswitch/api/service/Fortnite/status"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp:
                        data = await resp.json()
                        return data.get('status')
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    @staticmethod
    def fortnite_ban(func):
        async def inner(*args, **kwargs):
            if len(args) < 1:
                raise ValueError("access_token required.")
            access_token = args[0]
            url = f"https://lightswitch-public-service-prod.ol.epicgames.com/lightswitch/api/service/Fortnite/status"
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp:
                        data = await resp.json()
                        ban = data.get('banned')
                        if ban == 'true':
                            return 'you are banned'
                        else:
                            return  'you are not banned'
            return None

        def wrapper(*args, **kwargs):
            return asyncio.run(inner(*args, **kwargs))
        return wrapper
    
    class party:

        @staticmethod
        def get_party_revision(func):
            async def revison(*args, **kwargs):
                if len(args) < 2:
                    raise ValueError("access_token and account_id required.")
                access_token, account_id = args[0], args[1]

                async with aiohttp.ClientSession() as session:
                    url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                    headers = {
                        "Authorization": f"bearer {access_token}",
                        "Content-Type": "application/json"
                    }

                    async with session.get(url, headers=headers) as response:
                        data = await response.json()
                        if "current" not in data or not data["current"]:
                            return None, None

                        current_party = data["current"][0]
                        party_id = current_party["id"]
                        revision = None
                        for member in current_party["members"]:
                            if member["account_id"] == account_id:
                                revision = member["revision"]
                                break

                        if revision is None:
                            return None, None
                        return revision
            def wrapper(*args, **kwargs):
                return asyncio.run(revison(*args, **kwargs))

            return wrapper
        
        @staticmethod
        def meta(func):
            async def metaset(*args, **kwargs):
                if len(args) < 3:
                    raise ValueError("access_token and account_id and payload required.")
                access_token, account_id, payload = args[0], args[1], args[2]

                async with aiohttp.ClientSession() as session:
                    url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                    headers = {
                        "Authorization": f"bearer {access_token}",
                        "Content-Type": "application/json"
                    }

                    async with session.get(url, headers=headers) as response:
                        data = await response.json()
                        if "current" not in data or not data["current"]:
                            return None, None

                        current_party = data["current"][0]
                        party_id = current_party["id"]
                        revision = None
                        for member in current_party["members"]:
                            if member["account_id"] == account_id:
                                revision = member["revision"]
                                break

                        if revision is None:
                            return None, None

                    payload["revision"] = revision
                    if "update" in payload:
                        payload["update"] = {
                            key: json.dumps(value) for key, value in payload["update"].items()
                        }

                    patch_url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/parties/{party_id}/members/{account_id}/meta'

                    async with session.patch(patch_url, headers=headers, json=payload) as response:
                        pass

                    return func(*args, **kwargs)

            def wrapper(*args, **kwargs):
                return asyncio.run(metaset(*args, **kwargs))

            return wrapper   

        @staticmethod
        def invite(func):
            async def invite_former(*args, **kwargs):
                if len(args) < 3:
                    raise ValueError("access_token and account_id and payload and default_meta required.")
                access_token, account_id, friend_id = args[0], args[1], args[2]

                async with aiohttp.ClientSession() as session:
                    url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                    headers = {
                        "Authorization": f"bearer {access_token}",
                        "Content-Type": "application/json"
                    }

                    async with session.get(url, headers=headers) as response:
                        data = await response.json()
                        if "current" not in data or not data["current"]:
                            return None, None
                        build_id = data['current'][0]['meta']['urn:epic:cfg:build-id_s']
                        current_party = data["current"][0]
                        party_id = current_party["id"]
                        user = data['current'][0]['members'][0]['meta']['urn:epic:member:dn_s']
                        platform = data['current'][0]['members'][0]['connections'][0]['meta'].get('urn:epic:conn:platform_s')
                        revision = None
                        for member in current_party["members"]:
                            if member["account_id"] == account_id:
                                revision = member["revision"]
                                break

                    if revision is None:
                        return None, None
                    
                    invite_url = f"https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{friend_id}/pings/{account_id}"

                    data = {
                        "urn:epic:cfg:build-id_s": build_id,
                        "urn:epic:conn:platform_s": platform,
                        "urn:epic:conn:type_s": "game",
                        "urn:epic:invite:platformdata_s": "",
                        "urn:epic:member:dn_s": user
                        }
                    
                    async with session.post(invite_url, headers=headers, json=data) as response:
                        print(f'Friend Invite Requests: {await response.text()}')
                              
            def wrapper(*args, **kwargs):
                return asyncio.run(invite_former(*args, **kwargs))

            return wrapper
        

        @staticmethod
        def requests_to_join(func):
            async def requests_former(*args, **kwargs):
                if len(args) < 3:
                    raise ValueError("access_token and account_id and friend_id required.")
                access_token, account_id, friend_id = args[0], args[1], args[2]

                async with aiohttp.ClientSession() as session:
                    url = f'https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/user/{account_id}'
                    headers = {
                        "Authorization": f"bearer {access_token}",
                        "Content-Type": "application/json"
                    }

                    async with session.get(url, headers=headers) as response:
                        data = await response.json()
                        if "current" not in data or not data["current"]:
                            return None, None
                        build_id = data['current'][0]['meta']['urn:epic:cfg:build-id_s']
                        current_party = data["current"][0]
                        party_id = current_party["id"]
                        user = data['current'][0]['members'][0]['meta']['urn:epic:member:dn_s']
                        platform = data['current'][0]['members'][0]['connections'][0]['meta'].get('urn:epic:conn:platform_s')
                        revision = None
                        for member in current_party["members"]:
                            if member["account_id"] == account_id:
                                revision = member["revision"]
                                break

                    if revision is None:
                        return None, None
                    
                    invite_url = f"https://party-service-prod.ol.epicgames.com/party/api/v1/Fortnite/members/{friend_id}/intentions/{account_id}"

                    data = {
                        "urn:epic:cfg:build-id_s": build_id,
                        "urn:epic:conn:platform_s": platform,
                        "urn:epic:conn:type_s": "game",
                        "urn:epic:invite:platformdata_s": "",
                        "urn:epic:member:dn_s": user
                        }
                    
                    async with session.post(invite_url, headers=headers, json=data) as response:
                        print(f'Friend Invite Requests: {await response.text()}')
                              
            def wrapper(*args, **kwargs):
                return asyncio.run(requests_former(*args, **kwargs))

            return wrapper
    
    class stw_operation:

        @staticmethod
        def compose(func):
            async def mcp(*args, **kwargs):
                if len(args) < 4:
                    raise ValueError("access_token, account_id, profile, and operation required.")
                access_token, account_id, profile, operation = args[0], args[1], args[2], args[3]

                headers = {
                    "Authorization": f"bearer {access_token}",
                    "Content-Type": "application/json"
                }
                url = f"https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/{operation}?profileId={profile}&rvm=-1"

                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json={}) as response:
                        pass

            def wrapper(*args, **kwargs):
                return asyncio.run(mcp(*args, **kwargs))

            return wrapper
        

