from http import cookies
from sys import exception
import requests
from requests.exceptions import Timeout, RequestException
import time
import re
import json
from urllib.parse import urlencode, urlparse
import http.client as http_client
import logging
import base64

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('requests.packages.urllib3').setLevel(logging.DEBUG)
http_client.HTTPConnection.debuglevel = 1

# Custom exceptions mirroring PHP equivalents
class CurlExtensionNotLoadedException(Exception):
    def __init__(self):
        super().__init__("The Python requests library (or equivalent HTTP client) is not available. Please install it before proceeding!")
class CurlGeneralErrorException(Exception):
    """
    Exception raised for general CURL-related errors.

    Attributes:
        http_response_code: The HTTP response code returned by the request.
        curl_getinfo_results: The result of curl_getinfo (or equivalent diagnostics).
    """

    def __init__(self, message: str, http_response_code, curl_getinfo_results):
        super().__init__(message)
        self._http_response_code = http_response_code
        self._curl_getinfo_results = curl_getinfo_results

    def get_http_reponse_code(self):
        return self._http_response_code
    
    def get_curl_getinfo_results(self):
        return self._curl_getinfo_results
class CurlTimeoutException(Exception): 
    """
    Exception raised for cURL timeout errors.

    Attributes:
        http_response_code: The HTTP response code returned by the request.
        curl_getinfo_results: The result of curl_getinfo (or equivalent diagnostics).
    """

    def __init__(self, message: str, http_response_code, curl_getinfo_results):
        super().__init__(message)
        self._http_response_code = http_response_code
        self._curl_getinfo_results = curl_getinfo_results

    def get_http_response_code(self):
        return self._http_response_code

    def get_curl_getinfo_results(self):
        return self._curl_getinfo_results
class EmailInvalidException(Exception): 
    def __init__(self):
        super().__init__("Invalid email address provided")
class InvalidBaseUrlException(Exception): 
    def __init__(self):
        super().__init__("The base URL provided is invalid.")
class InvalidCurlMethodException(Exception): 
    def __init__(self):
        super().__init__("Invalid cURL method provided")
class InvalidSiteNameException(Exception): 
    def __init__(self):
        super().__init__("Invalid site name provided")
class JsonDecodeException(Exception): pass
class LoginFailedException(Exception): pass
class LoginRequiredException(Exception): pass
class MethodDeprecatedException(Exception): pass
class NotAUnifiOsConsoleException(Exception): 
    def __init__(self):
        super().__init__("This is not a Unifi OS console.")

class Client:
    CLASS_VERSION = '2.0.5'
    CURL_METHODS_ALLOWED = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
    DEFAULT_CURL_METHOD = 'GET'

    def __init__(self, user, password, baseurl='https://32.218.193.188', site='default', version='8.0.28', ssl_verify=False, unificookie_name='unificookie'):
        # Initial setup mirrors PHP constructor
        self._check_curl()
        self._check_base_url(baseurl)
        self._check_site(site)

        self._user = user.strip()
        self._password = password.strip()
        self._baseurl = baseurl.strip()
        self._site = site.strip().lower()
        self._version = version.strip()
        self._unificookie_name = unificookie_name.strip()

        self._timeout = 5

        self._verify_ssl_cert = ssl_verify
        self._http_version = None
        self._curl_method = self.DEFAULT_CURL_METHOD
        self._request_timeout = 30
        self._connect_timeout = 10
        self._is_loggedin = False
        self._unifi_os = False
        self._session = requests.Session()
        self._last_response_code = None
        self._last_error_message = ''
        self._last_results_raw = None
        self._cookies_created_at = 0
        self._exec_retries = 0

        self._curl_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Expect': ''
        }

    def _check_curl(self):
        if not hasattr(requests, 'Session'):
            raise CurlExtensionNotLoadedException("requests library is not functioning correctly")

    def _check_base_url(self, baseurl):
        if not baseurl.startswith('https://'):
            raise InvalidBaseUrlException("Base URL must start with 'https://'")

    def _check_site(self, site):
        if not site or '/' in site:
            raise InvalidSiteNameException("Invalid site name")
    
    def update_unificookie(self) -> bool:
        """
        Load stored cookie from session store.
        """
        store = getattr(self, '_session_store', {})
        cookie = store.get(self._unificookie_name)
        if cookie:
            self._cookies = cookie
            self._cookies_created_at = int(time.time())
            if 'TOKEN' in cookie:
                self._unifi_os = True
            return True
        return False

    def login(self) -> bool:
        # Skip if already logged in via valid cookie
        self._verify_ssl_cert = False

        if self.update_unificookie():
            self._is_loggedin = True

        if self._is_loggedin:
            return True

        # 1) Prepare GET curl_options to detect controller type
        get_options = {
            'method': 'GET',
            'url': f"{self._baseurl}/",
            'headers': self._curl_headers,
            'timeout': (self.get_connection_timeout(), self.get_curl_request_timeout()),
            'verify': self._verify_ssl_cert
        }
        try:
            resp = self._session.request(**get_options)
        except Timeout as e:
            raise CurlTimeoutException(str(e), None, None)
        except RequestException as e:
            raise CurlGeneralErrorException(str(e), None, None)

        http_code = resp.status_code

        # 2) Build POST curl_options for actual login
        post_url = f"{self._baseurl}/api/login"
        if http_code == 200:
            self._unifi_os = True
            post_url = f"{self._baseurl}/api/auth/login"

        post_options = {
            'method': 'POST',
            'url': post_url,
            'headers': {
                **self._curl_headers,
                'Referer': f"{self._baseurl}/login",
                'Content-Type': 'application/json'
            },
            'data': json.dumps({
                'username': self._user,
                'password': self._password
            }),
            'timeout': (self.get_connection_timeout(), self.get_curl_request_timeout()),
            'verify': self._verify_ssl_cert
        }

        try:
            resp2 = self._session.request(**post_options)    
        except Timeout as e:
            raise CurlTimeoutException(str(e), None, None)
        except RequestException as e:
            raise CurlGeneralErrorException(str(e), None, None)

        if self.get_debug:
            print("\n-----------LOGIN-------------")
            print("GET Options:", get_options)
            print("POST Options:", post_options)
            print("Status Code:", resp2.status_code)
            print("Response Body:", resp2.text)
            #print("-----------------------------\n")

        if resp2.status_code == 200:
            token = resp2.headers.get('x-updated-csrf-token') or resp2.headers.get('X-Csrf-Token')
            if token:
                self._session.headers.update({'x-csrf-token': token,
                                              'Referer': f"{self._baseurl}/login"})
            self._is_loggedin = True
            return True

        raise LoginFailedException(f"HTTP response: {resp2.status_code}")

    def logout(self) -> bool:
        """
        Log out of the UniFi Controller.
        """
        opts = self.get_curl_handle()
        logout_path = "/logout"

        # UniFi OS-specific handling
        if self._unifi_os:
            logout_path = "/api/auth/logout"
            opts['method'] = 'POST'
            self.create_x_csrf_token_header()

        # Always POST with headers
        opts.update({
            'url': f"{self._baseurl}{logout_path}",
            'method': 'POST',
            'headers': self._curl_headers,
            'verify': False
        })

        # Perform the request
        try:
            resp = self._session.request(**opts)
        except Timeout as e:
            raise CurlTimeoutException(str(e), None, None)
        except RequestException as e:
            raise CurlGeneralErrorException(str(e), None, None)

        # Cleanup state
        self._is_loggedin = False
        self._cookies = ''
        self._cookies_created_at = 0

        return True

    # === API Endpoint Methods ===
    # The following methods are directly converted from the PHP class to Python, preserving functionality and parameters.

    def get_site_stats(self):
        return self.fetch_results(f"/api/s/{self._site}/stat/sysinfo")

    def get_clients(self):
        return self._request(f"/api/s/{self._site}/stat/sta")

    def block_client(self, mac):
        return self._request(f"/api/s/{self._site}/cmd/stamgr", method='POST', payload={'cmd': 'block-sta', 'mac': mac})

    def unblock_client(self, mac):
        return self._request(f"/api/s/{self._site}/cmd/stamgr", method='POST', payload={'cmd': 'unblock-sta', 'mac': mac})

    def reconnect_client(self, mac):
        return self._request(f"/api/s/{self._site}/cmd/stamgr", method='POST', payload={'cmd': 'kick-sta', 'mac': mac})

    def authorize_guest(self, mac, minutes, up=None, down=None, megabytes=None, ap_mac=None):
        payload = {
            'cmd': 'authorize-guest',
            'mac': mac.lower(),
            'minutes': minutes
        }
        if up is not None:        payload['up'] = up
        if down is not None:      payload['down'] = down
        if megabytes is not None: payload['bytes'] = megabytes
        if ap_mac is not None:    payload['ap_mac'] = ap_mac.lower()
        return self._request(f"/api/s/{self._site}/cmd/stamgr", method='POST', payload=payload)

    """
        Unauthorize a client device.

        Param string mac client MAC address
        returns bool true upon success
        throws Exception
    """
    def unauthorize_guest(self, mac):
        return self._request(
            f"/api/s/{self._site}/cmd/stamgr",
            method='POST',
            payload={'cmd': 'unauthorize-guest', 'mac': mac}
        )

    def reconnect_sta(self, mac):
        return self._request(
            f"/api/s/{self._site}/cmd/stamgr",
            method='POST',
            payload={'cmd': 'kick-sta', 'mac': mac.lower()}
        )

    def block_sta(self, mac):
        return self._request(
            f"/api/s/{self._site}/cmd/stamgr",
            method='POST',
            payload={'cmd': 'block-sta', 'mac': mac.lower()}
        )

    def unblock_sta(self, mac):
        return self._request(
            f"/api/s/{self._site}/cmd/stamgr",
            method='POST',
            payload={'cmd': 'unblock-sta', 'mac': mac.lower()}
        )
    
    def forget_sta(self, mac):
        return self._request(
            f"/api/s/{self._site}/cmd/stamgr",
            method='POST',
            payload={'cmd': 'forget-sta', 'mac': mac}
        )

    def set_sta_note(self, user_id: str, note: str = '') -> bool:
        """Add or modify a client device note."""
        payload = {'note': note}
        return self.fetch_results_boolean(f"/api/s/{self._site}/upd/user/{user_id.strip()}", payload=payload)

    def set_sta_name(self, user_id: str, name: str = '') -> bool:
        """Add or modify a client device name."""
        payload = {'name': name}
        return self.fetch_results_boolean(f"/api/s/{self._site}/upd/user/{user_id.strip()}", payload=payload)



    ### Create Users

    def create_user(self, mac: str, user_group_id: str ,name: str = None, note: str = None, is_guest: bool = None, is_wired: bool = None):
            """
            Fully featured user creation matching the PHP client implementation
            """
            new_user = {
                'mac': mac.lower(),
                'usergroup_id': user_group_id
            }
            if name:
                new_user['name'] = name
            if note:
                new_user['note'] = note
            if is_guest is not None:
                new_user['is_guest'] = is_guest
            if is_wired is not None:
                new_user['is_wired'] = is_wired

            payload = {
                'objects': [{'data': new_user}]    
            }

            self._curl_method = "POST"


            return self.fetch_results(
                f"/api/s/{self._site}/rest/user",
                payload=payload
                )

    def delete_user(self, user_id: str):
        """
        Remove a user by ID
        """
        return self._request(f"/api/s/{self._site}/rest/user/{user_id}", method='DELETE')

    def get_user(self, user_id: str):
        """
        Retrieve a single user by ID.
        """
        return self.fetch_results(f"/api/s/{self._site}/rest/user/{user_id}")

    def get_client_by_mac(self, mac: str):
        return self.fetch_results(f"/api/s/{self._site}/stat/user/{mac}")

    def update_user(self, user_id: str, name: str = None, note: str = None, is_guest: bool = None, is_wired: bool = None):
        """
        Update an existing user's details.
        """

        payload = {}
        if name is not None:
            payload['name'] = name
        if note is not None:
            payload['note'] = note
        if is_guest is not None:
            payload['is_guest'] = is_guest
        if is_wired is not None:
            payload['is_wired'] = is_wired

        return self.fetch_results(
            f"/api/s/{self._site}/rest/user/{user_id}",
            payload=payload
        )

    def forget_user(self, mac: str):
        """
        Forget (remove) any record of a client's MAC from the site.
        """
        return self._request(
            f"/api/s/{self._site}/cmd/sitemgr",
            method='POST',
            payload={'cmd': 'forget-sta', 'mac': mac}
        )

    ## Add them here 

    ## ------------- Make sure these are included in the PHP files ------
    def get_clients_summary(self):
        return self._request(f"/api/s/{self._site}/stat/summary/client")

    def get_user_groups(self):
        return self._request(f"/api/s/{self._site}/list/usergroup")

    def get_user_group(self, group_id):
        return self._request(f"/api/s/{self._site}/list/usergroup/{group_id}")

    def create_user_group(self, group_name: str, group_dn: int = -1, group_up: int = -1):
        """
        Create a user group with download and upload QoS limits.
        
        :param group_name:   Name of the group
        :param group_dn:     Max download rate (kbps), -1 for unlimited
        :param group_up:     Max upload rate (kbps),   -1 for unlimited
        """
        payload = {
            'name': group_name,
            'qos_rate_max_down': group_dn,
            'qos_rate_max_up': group_up,
        }
        return self.fetch_results(
            f"/api/s/{self._site}/rest/usergroup",
            payload=payload
        )
    
    def edit_user_group(self, group_id: str, site_id: str, group_name: str, group_dn: int = -1, group_up: int = -1):
        """
        Edit an existing user group with new name or QoS limits.
        """
        payload = {
            '_id': group_id,
            'name': group_name,
            'qos_rate_max_down': group_dn,
            'qos_rate_max_up': group_up,
            'site_id': site_id,
        }
        return self._request(
            f"/api/s/{self._site}/rest/usergroup",
            method='PUT',
            payload=payload
        )

    def delete_user_group(self, group_id):
        return self._request(
            f"/api/s/{self._site}/cmd/usergroup/{group_id}",
            method='DELETE'
        )


    def list_sites(self):
        return self.fetch_results("/api/self/sites")

    def list_apgroups(self):
        """
        Fetch AP groups for the current site.
        """
        return self._request(f"/v2/api/site/{self._site}/apgroups")

    def create_apgroup(self, name: str, description: str = None) -> dict:
        """Create a new AP group with optional description."""
        payload = {'name': name}
        if description:
            payload['description'] = description
        return self.fetch_results(f"/v2/api/site/{self._site}/apgroups", payload=payload)

    def edit_apgroup(self, group_id: str, name: str = None, description: str = None) -> dict:
        """Modify an existing AP group."""
        self._curl_method = 'PUT'
        payload = {'_id': group_id}
        if name:
            payload['name'] = name
        if description:
            payload['description'] = description
        result = self.fetch_results(f"/v2/api/site/{self._site}/apgroups/{group_id}", payload=payload)
        self._curl_method = 'GET'
        return result

    def delete_apgroup(self, group_id: str) -> bool:
        """Delete an AP group."""
        self._curl_method = 'DELETE'
        result = self.fetch_results_boolean(f"/v2/api/site/{self._site}/apgroups/{group_id}")
        self._curl_method = 'GET'
        return result

    def list_dashboard(self, five_minutes: bool = False):
        """Fetch dashboard metrics, 5-minute scale if requested."""
        suffix = '?scale=5minutes' if five_minutes else ''
        return self.fetch_results(f"/api/s/{self._site}/stat/dashboard{suffix}")

    def list_users(self):
        """Fetch known client devices."""
        return self.fetch_results(f"/api/s/{self._site}/list/user", prefix_path=True)

    def list_tags(self):
        """Fetch all device tags (REST)."""
        return self.fetch_results(f"/api/s/{self._site}/rest/tag")

    def create_tag(self, tag_name: str, description: str = None) -> dict:
        """Create a new device tag."""
        payload = {'name': tag_name}
        if description:
            payload['description'] = description
        return self.fetch_results(f"/api/s/{self._site}/rest/tag", payload=payload)

    def delete_tag(self, tag_id: str) -> bool:
        """Delete a device tag."""
        self._curl_method = 'DELETE'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/tag/{tag_id}")
        self._curl_method = 'GET'
        return result

    def get_tag(self, tag_id: str):
        """Retrieve a specific device tag."""
        self._curl_method = 'GET'
        return self.fetch_results(f"/api/s/{self._site}/rest/tag/{tag_id}")

    def list_known_rogueaps(self):
        """Fetch known rogue access points."""
        return self.fetch_results(f"/api/s/{self._site}/rest/rogueknown")

    def get_site(self, site_id) -> str:
        return self._request(f"/api/s/{site_id}/self")

    def create_site(self, description: str):
        """
        Create a new site with a given description.
        """
        payload = {
            'desc': description,
            'cmd': 'add-site',
        }

        self._curl_method = "POST"

        if self._unifi_os:
            # UniFi OS uses the /api/self/sites endpoint
            return self.fetch_results(
                "/api/self/sites",
                payload=payload
            )
        else:
            # Classic controller
            return self.fetch_results(
                f"/api/s/{self._site}/cmd/sitemgr",
                payload=payload
            )

        self._curl_method = "GET"

    def delete_site(self, site_id):
        return self._request(
            f"/api/s/{site_id}",
            method='DELETE',
            payload={'site': site_id, 'cmd': 'delete-site'}
        )

    def set_site(self, site: str) -> str:
        self._check_site(site)
        self._site = site.strip()

        return self._site

    def set_site_name(self, site_name: str) -> bool:
        """Change the current site's long name."""
        payload = {'cmd': 'update-site', 'desc': site_name}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/sitemgr", payload=payload)

    def set_site_locale(self, locale_id: str, payload: dict) -> bool:
        """Update the site's locale settings."""
        self._curl_method = 'PUT'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/setting/locale/{locale_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def set_site_snmp(self, snmp_id: str, payload: dict) -> bool:
        """Update site SNMP settings"""
        self._curl_method = 'PUT'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/setting/snmp/{snmp_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def set_site_mgmt(self, mgmt_id: str, payload: dict) -> bool:
        """Update site management settings"""
        self._curl_method = 'PUT'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/setting/mgmt/{mgmt_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def set_site_guest_access(self, guest_access_id: str, payload: dict) -> bool:
        """Update site guest access settings"""
        self._curl_method = 'PUT'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/setting/guest_access/{guest_access_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def set_site_ntp(self, ntp_id: str, payload: dict) -> bool:
        """Update site NTP settings"""
        self._curl_method = 'PUT'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/setting/ntp/{ntp_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def set_site_connectivity(self, connectivity_id: str, payload: dict) -> bool:
        """Update site connectivity settings"""
        self._curl_method = 'PUT'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/setting/connectivity/{connectivity_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def set_site_country(self, country_id: str, payload) -> bool:
        self._curl_method = "PUT"
        return self.fetch_results_boolean(f"/api/s/{self._site}/rest/setting/country/{country_id.strip()}", payload=payload)

    def get_admins(self):
        """Fetch administrators for current site"""
        payload = {'cmd': 'get-admins'}
        return self.fetch_results(f"/api/s/{self._site}/cmd/sitemgr", payload=payload, prefix_path=True)

    def list_all_admins(self):
        """Fetch all administrators"""
        payload = {'cmd': 'get-all-admins'}
        return self.fetch_results(f"/api/s/{self._site}/cmd/sitemgr", payload=payload)

    def invite_admin(self, name: str, email: str, enable_sso: bool = True, readonly: bool = False,
                     device_adopt: bool = False, device_restart: bool = False) -> bool:
        """Invite a new or existing admin"""
        email = email.strip()
        payload = {'cmd': 'create-admin', 'name': name, 'email': email, 'role': 'admin', 'permissions': []}
        # SSO control
        payload['sso_enabled'] = enable_sso
        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise EmailInvalidException()
        # Role assignment
        if readonly:
            payload['role'] = 'readonly'
        # Permissions
        if device_adopt:
            payload['permissions'].append('API_DEVICE_ADOPT')
        if device_restart:
            payload['permissions'].append('API_DEVICE_RESTART')
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/sitemgr", payload=payload)

    def assign_existing_admin(self, admin_id: str, readonly: bool = False,
                              device_adopt: bool = False, device_restart: bool = False) -> bool:
        """Assign an existing admin to this site"""
        payload = {'cmd': 'grant-admin', 'admin': admin_id.strip(), 'role': 'admin', 'permissions': []}
        if readonly:
            payload['role'] = 'readonly'
        if device_adopt:
            payload['permissions'].append('API_DEVICE_ADOPT')
        if device_restart:
            payload['permissions'].append('API_DEVICE_RESTART')
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/sitemgr", payload=payload)

    def update_admin(self, admin_id: str, name: str, email: str, password: str = '',
                     readonly: bool = False, device_adopt: bool = False, device_restart: bool = False) -> bool:
        """Update admin user properties"""
        email = email.strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise EmailInvalidException()
        payload = {'cmd': 'update-admin', 'admin': admin_id.strip(), 'name': name.strip(), 'email': email, 'password': password, 'role': 'admin', 'permissions': []}
        if readonly:
            payload['role'] = 'readonly'
        if device_adopt:
            payload['permissions'].append('API_DEVICE_ADOPT')
        if device_restart:
            payload['permissions'].append('API_DEVICE_RESTART')
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/sitemgr", payload=payload)

    def revoke_admin(self, admin_id: str) -> bool:
        """Revoke an admin's access to this site"""
        payload = {'cmd': 'revoke-admin', 'admin': admin_id.strip()}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/sitemgr", payload=payload)

    def delete_admin(self, admin_id: str) -> bool:
        """Delete an admin user"""
        payload = {'cmd': 'delete-admin', 'admin': admin_id.strip()}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/sitemgr", payload=payload)

    def list_wlan_groups(self):
        """Fetch WLAN groups"""
        return self.fetch_results(f"/api/s/{self._site}/rest/wlangroup")

    def stat_sysinfo(self):
        """Fetch system info stat"""
        return self.fetch_results(f"/api/s/{self._site}/stat/sysinfo")

    def stat_status(self) -> bool:
        """Fetch controller online status"""
        return self.fetch_results_boolean(
            '/status',
            payload=None,
            login_required=self._unifi_os
        )

    def stat_full_status(self):
        """Fetch full controller status"""
        # Ensure login if required and fetch boolean to populate last_results_raw
        self.fetch_results_boolean(
            '/status',
            payload=None,
            login_required=self._unifi_os
        )
        # Decode and return the last raw JSON results
        raw = self.get_last_results_raw(return_json=False)
        try:
            return json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            return raw

    def list_device_name_mappings(self):
        """Fetch device name MIB mappings"""
        # Populate last_results_raw via boolean fetch
        self.fetch_results_boolean(
            '/dl/firmware/bundles.json',
            payload=None,
            login_required=self._unifi_os
        )
        # Decode and return JSON
        raw = self.get_last_results_raw(return_json=False)
        try:
            return json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            return raw(f"/api/s/{self._site}/list/device/name_mapping")

    def list_self(self):
        """Fetch details of the current user"""
        return self.fetch_results('/api/self')

    def get_devices(self):
        return self.fetch_results(f"/api/s/{self._site}/stat/device", login_required=True, prefix_path=True)

    def get_device(self, device_id):
        return self._request(f"/api/s/{self._site}/stat/device/{device_id}")
    
    def get_wlan(self, wlan_id: str):
        """
        Retrieve WLAN configuration by ID
        """
        return self._request(f"/api/s/{self._site}/rest/wlanconf/{wlan_id}")

    def list_wlanconf(self):
        """
        List all WLAN configurations on the site.
        """
        return self._request(f"/api/s/{self._site}/rest/wlanconf")

    def create_wlan(
        self,
        name: str,
        x_passphrase: str,
        usergroup_id: str,
        wlangroup_id: str,
        enabled: bool = True,
        hide_ssid: bool = False,
        is_guest: bool = False,
        security: str = 'open',
        wpa_mode: str = 'wpa2',
        wpa_enc: str = 'ccmp',
        vlan_enabled: bool = None,
        vlan_id: str = None,
        uapsd_enabled: bool = False,
        schedule_enabled: bool = False,
        schedule: list = None,
        ap_group_ids: list = None,
        payload: dict = None
    ) -> bool:
        """
        Create a new WLAN with full parameter support matching the PHP client.
        """
        data = payload.copy() if payload is not None else {}
        # Merge required/default fields
        data.update({
            'name': name.strip(),
            'usergroup_id': usergroup_id.strip(),
            'wlangroup_id': wlangroup_id.strip(),
            'enabled': enabled,
            'hide_ssid': hide_ssid,
            'is_guest': is_guest,
            'security': security.strip(),
            'wpa_mode': wpa_mode.strip(),
            'wpa_enc': wpa_enc.strip(),
            'uapsd_enabled': uapsd_enabled,
            'schedule_enabled': schedule_enabled,
            'schedule': schedule or [],
        })
        if vlan_id is not None:
            data['networkconf_id'] = vlan_id
        if x_passphrase and security != 'open':
            data['x_passphrase'] = x_passphrase.strip()
        if ap_group_ids is not None:
            data['ap_group_ids'] = ap_group_ids

        # Perform the request and return True on HTTP 200
        self._request(
            f"/api/s/{self._site}/add/wlanconf",
            method='POST',
            payload=data
        )
        return self._last_response_code == 200

    def set_wlansettings_base(self, wlan_id: str, payload: dict) -> bool:
        """Base REST call to update WLAN settings."""
        self._curl_method = 'PUT'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/wlanconf/{wlan_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def set_wlansettings(self, wlan_id: str, x_passphrase: str, name: str = '') -> bool:
        """Update basic WLAN settings (passphrase and SSID)."""
        payload = {'x_passphrase': x_passphrase.strip()}
        if name:
            payload['name'] = name.strip()
        return self.set_wlansettings_base(wlan_id, payload)

    def disable_wlan(self, wlan_id: str, disable: bool) -> bool:
        """Disable or enable a WLAN network."""
        action = not disable
        payload = {'enabled': action}
        return self.set_wlansettings_base(wlan_id, payload)

    def set_wlan_mac_filter(self, wlan_id: str, policy: str, enable: bool, macs: list) -> bool:
        """Set MAC filter policy and list for a WLAN."""
        if policy not in ['allow', 'deny']:
            return False
        macs = [m.lower() for m in macs]
        payload = {'mac_filter_enabled': enable, 'mac_filter_policy': policy, 'mac_filter_list': macs}
        return self.set_wlansettings_base(wlan_id, payload)

    def set_wlan_passphrase(self, wlan_id: str, x_passphrase: str, name: str = None):
        """
        Update PSK/passphrase and optionally name (mirros set_wlansettings in PHP)
        """

        data = {}
        if x_passphrase:
            data['x_passphrase'] = x_passphrase.strip()
        if name is not None:
            data['name'] = name.strip()
        return self._request(
            f"/api/s/{self._site}/rest/wlanconf/{wlan_id}",
            method='PUT',
            payload=data
        )

    def delete_wlan(self, wlan_id: str):
        """
        Delete a WLAN configuration by ID
        """
        return self._request(
            f"/api/s/{self._site}/rest/wlanconf/{wlan_id.strip()}"
        )

    def cmd_stat(self, command: str) -> bool:
        """Execute specific stats commands, e.g., 'reset-dpi'."""
        if command != 'reset-dpi':
            return False
        payload = {'cmd': command}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/stat", payload=payload)

    def set_element_adoption(self, enable: bool) -> bool:
        """Toggle Element Adoption setting."""
        payload = {'enabled': enable}
        return self.fetch_results_boolean(f"/api/s/{self._site}/set/setting/element_adopt", payload=payload)

    def spectrum_scan(self, mac: str) -> bool:
        """Trigger RF spectrum scan on an AP."""
        payload = {'cmd': 'spectrum-scan', 'mac': mac.lower()}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr", payload=payload)

    def spectrum_scan_state(self, mac: str):
        """Fetch RF scan state/results for an AP."""
        return self.fetch_results(f"/api/s/{self._site}/stat/spectrum-scan/{mac.lower().strip()}")

    def set_device_settings_base(self, device_id: str, payload: dict) -> bool:
        """Base REST call to update device settings."""
        self._curl_method = 'PUT'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/device/{device_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def power_cycle_switch_port(self, mac: str, port_idx: int) -> bool:
        """Power-cycle a PoE switch port."""
        payload = {'mac': mac.lower(), 'port_idx': port_idx, 'cmd': 'power-cycle'}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr", payload=payload)



    def list_guests(self, within: int = 8760):
        """
        Retrieve all active guest sessions on the site within the last 'within' seconds
        """
        payload = {'within': within}
        return self.fetch_results(
            f"/api/s/{self._site}/stat/guest",
            payload=payload
        )

    ## same as list_guest but for mac
    def list_clients(self, mac: str = None):
        """Fetch online client devices, or single device if MAC provided."""
        path_mac = mac.lower().strip() if isinstance(mac, str) else ''
        return self.fetch_results(f"/api/s/{self._site}/stat/sta/{path_mac}")

    def list_active_clients(self, include_traffic_usage: bool = True, include_unifi_devices: bool = True):
        """Fetch active client devices, with optional traffic and UniFi device inclusion."""
        query = urlencode({
            'include_traffic_usage': include_traffic_usage,
            'include_unifi_devices': include_unifi_devices,
        })
        return self.fetch_results(f"/v2/api/site/{self._site}/clients/active?{query}")

    def list_clients_history(self, only_non_blocked: bool = True, include_unifi_devices: bool = True, within_hours: int = 0):
        """Fetch offline client device history."""
        query = urlencode({
            'only_non_blocked': only_non_blocked,
            'include_unifi_devices': include_unifi_devices,
            'within_hours': within_hours,
        })
        return self.fetch_results(f"/v2/api/site/{self._site}/clients/history?{query}")

    def expire_guest(self, mac: str):
        """
        Expire (unauthorize) a guest session immedietely
        """
        return self._request(
            f"/api/s/{self._site}/cmd/stamgr",
            method='POST',
            payload={'cmd': 'unauthorize-guest', 'mac': mac}
        )
    
    def list_vouchers(self):
        """
        List all hotspot vouchers on the site.
        """
        return self._request(f"/api/s/{self._site}/stat/voucher")

    def create_voucher(
        self,
        minutes: int,
        count: int = 1,
        quota: int = 0,
        note: str = '',
        up: int = None,
        down: int = None,
        megabytes: int = None
    ):

        """
        Create new hotspot vouchers with full options.
        :param minutes:     time-to-live in minutes
        :param count:       number of vouchers to generate
        :param quota:       total quota in bytes (0 for unlimited)
        :param note:        optional note for the vouchers
        :param up:          optional upload rate limit (kbps)
        :param down:        optional download rate limit (kbps)
        :param megabytes:   optional byte quota per voucher
        """
        payload = {
            'cmd': 'create-voucher',
            'expire': minutes,
            'n': count,
            'quota': quota
        }
        if note:
            payload['note'] = note.strip()
        if up is not None:
            payload['up'] = up
        if down is not None:
            payload['down'] = down
        if megabytes is not None:
            payload['bytes'] = megabytes

        return self._request(
            f"/api/s/{self._site}/cmd/hotspot",
            method='POST',
            payload=payload
            )



    def revoke_voucher(self, voucher_id: str):
        """
        Delete a specific voucher by its ID
        """
        payload = {'_id': voucher_id, 'cmd': 'delete-voucher'}

        return self._request(
            f"/api/s/{self._site}/cmd/hotspot",
            method='POST',
            payload=payload
        )

    def list_sessions(self):
        """
        List all client sessions (stat/session) for the site
        """
        return self._request(f"/api/s/{self._site}/stat/session")

    def stat_hourly_site(self, start: int = None, end: int = None, attribs: list = None):
        """
        Retrieve hourly site statistics report.
        :param start:   start timestamp in ms (defaults to 7 days ago)
        :param end:     end timestamp in ms (defaults to now)
        :param attribs: list of attributes to return (defaults to ['time'] + default_site_stats_attribs)
        """
        now_ms = int(time.time() * 1000)
        end = end if end is not None else now_ms
        start = start if start is not None else end - (7 * 24 * 3600 * 1000)
        default_attrs = getattr(self, 'default_site_stats_attribs', [])
        attribs = attribs if attribs is not None else ['time'] + default_attrs

        payload = {
            'attrs': attribs,
            'start': start,
            'end': end
        }

        return self._request(
            f"/api/s/{self._site}/stat/report/hourly.site",
            method='GET',
            payload=payload
        )

    def stat_5minutes_site(self, start: int = None, end: int = None, attribs: list = None):
        """Fetch 5-minute site stats (defaults to past 12 hours)."""
        end = end or int(time.time() * 1000)
        start = start or end - 12 * 3600 * 1000
        attrs = attribs or self.default_site_stats_attribs
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        return self.fetch_results(f"/api/s/{self._site}/stat/report/5minutes.site", payload=payload)

    def stat_5minutes_aps(self, start: int = None, end: int = None, mac: str = None, attribs: list = None):
        """Fetch 5-minute AP stats (defaults to past 12 hours)."""
        end = end or int(time.time() * 1000)
        start = start or end - 12 * 3600 * 1000
        attrs = attribs or self.default_ap_stats_attribs
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        if mac:
            payload['mac'] = mac.lower()
        return self.fetch_results(f"/api/s/{self._site}/stat/report/5minutes.ap", payload=payload)

    def stat_hourly_aps(self, start: int = None, end: int = None, mac: str = None, attribs: list = None):
        """Fetch hourly AP stats (defaults to past 7 days)."""
        end = end or int(time.time() * 1000)
        start = start or end - 7 * 24 * 3600 * 1000
        attrs = attribs or self.default_ap_stats_attribs
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        if mac:
            payload['mac'] = mac.lower()
        return self.fetch_results(f"/api/s/{self._site}/stat/report/hourly.ap", payload=payload)

    def stat_daily_aps(self, start: int = None, end: int = None, mac: str = None, attribs: list = None):
        """Fetch daily AP stats (defaults to past 7 days)."""
        now = int(time.time())
        end = end or (now - (now % 3600)) * 1000
        start = start or end - 7 * 24 * 3600 * 1000
        attrs = attribs or self.default_ap_stats_attribs
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        if mac:
            payload['mac'] = mac.lower()
        return self.fetch_results(f"/api/s/{self._site}/stat/report/daily.ap", payload=payload)

    def stat_monthly_aps(self, start: int = None, end: int = None, mac: str = None, attribs: list = None):
        """Fetch monthly AP stats (defaults to past 52 weeks)."""
        now = int(time.time())
        end = end or (now - (now % 3600)) * 1000
        start = start or end - 52 * 7 * 24 * 3600 * 1000
        attrs = attribs or self.default_ap_stats_attribs
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        if mac:
            payload['mac'] = mac.lower()
        return self.fetch_results(f"/api/s/{self._site}/stat/report/monthly.ap", payload=payload)

    def stat_5minutes_user(self, mac: str = None, start: int = None, end: int = None, attribs: list = None):
        """Fetch 5-minute user stats (defaults to past 12 hours)."""
        end = end or int(time.time() * 1000)
        start = start or end - 12 * 3600 * 1000
        attrs = attribs or ['time', 'rx_bytes', 'tx_bytes']
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        if mac:
            payload['mac'] = mac.lower()
        return self.fetch_results(f"/api/s/{self._site}/stat/report/5minutes.user", payload=payload)

    def stat_hourly_user(self, mac: str = None, start: int = None, end: int = None, attribs: list = None):
        """Fetch hourly user stats (defaults to past 7 days)."""
        end = end or int(time.time() * 1000)
        start = start or end - 7 * 24 * 3600 * 1000
        attrs = attribs or ['time', 'rx_bytes', 'tx_bytes']
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        if mac:
            payload['mac'] = mac.lower()
        return self.fetch_results(f"/api/s/{self._site}/stat/report/hourly.user", payload=payload)

    def stat_daily_user(self, mac: str = None, start: int = None, end: int = None, attribs: list = None):
        """Fetch daily user stats (defaults to past 7 days)."""
        end = end or int(time.time() * 1000)
        start = start or end - 7 * 24 * 3600 * 1000
        attrs = attribs or ['time', 'rx_bytes', 'tx_bytes']
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        if mac:
            payload['mac'] = mac.lower()
        return self.fetch_results(f"/api/s/{self._site}/stat/report/daily.user", payload=payload)

    def stat_monthly_user(self, mac: str = None, start: int = None, end: int = None, attribs: list = None):
        """Fetch monthly user stats (defaults to past 52 weeks)."""
        now = int(time.time())
        end = end or (now - (now % 3600)) * 1000
        start = start or end - 52 * 7 * 24 * 3600 * 1000
        attrs = attribs or ['time', 'rx_bytes', 'tx_bytes']
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        if mac:
            payload['mac'] = mac.lower()
        return self.fetch_results(f"/api/s/{self._site}/stat/report/monthly.user", payload=payload)

    def stat_5minutes_gateway(self, start: int = None, end: int = None, attribs: list = None):
        """Fetch 5-minute gateway stats (defaults to past 12 hours)."""
        end = end or int(time.time() * 1000)
        start = start or end - 12 * 3600 * 1000
        attrs = attribs or ['time', 'mem', 'cpu', 'loadavg_5']
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        return self.fetch_results(f"/api/s/{self._site}/stat/report/5minutes.gw", payload=payload)

    def stat_hourly_gateway(self, start: int = None, end: int = None, attribs: list = None):
        """Fetch hourly gateway stats (defaults to past 7 days)."""
        end = end or int(time.time() * 1000)
        start = start or end - 7 * 24 * 3600 * 1000
        attrs = attribs or ['time', 'mem', 'cpu', 'loadavg_5']
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        return self.fetch_results(f"/api/s/{self._site}/stat/report/hourly.gw", payload=payload)

    def stat_daily_gateway(self, start: int = None, end: int = None, attribs: list = None):
        """Fetch daily gateway stats (defaults to past 52 weeks)."""
        now = int(time.time())
        end = end or (now - (now % 3600)) * 1000
        start = start or end - 52 * 7 * 24 * 3600 * 1000
        attrs = attribs or ['time', 'mem', 'cpu', 'loadavg_5']
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        return self.fetch_results(f"/api/s/{self._site}/stat/report/daily.gw", payload=payload)

    def stat_monthly_gateway(self, start: int = None, end: int = None, attribs: list = None):
        """Fetch monthly gateway stats (defaults to past 52 weeks)."""
        now = int(time.time())
        end = end or (now - (now % 3600)) * 1000
        start = start or end - 52 * 7 * 24 * 3600 * 1000
        attrs = attribs or ['time', 'mem', 'cpu', 'loadavg_5']
        payload = {'attrs': ['time'] + attrs, 'start': start, 'end': end}
        return self.fetch_results(f"/api/s/{self._site}/stat/report/monthly.gw", payload=payload)

    def list_network(self, network_id: str = ''):
        return self._request(f"/api/s/{self._site}/rest/networkconf{network_id.strip()}")
    
    def list_networkconf(self, network_id: str = ''):
        return self._request(f"/api/s/{self._site}/rest/networkconf{network_id.strip()}")

    def list_backups(self):
        payload = {'cmd': 'list-backups'}

        return self.fetch_results(f"/api/s/{self._site}/cmd/backup", payload=payload, prefix_path=True)

    def get_network(self, network_id: str):
        """
        Get a specific network configuration by ID
        """
        return self._request(f"/api/s/{self._site}/rest/networkconf/{network_id}")

    def create_network(self, payload: dict):
        """
        Create a new network configuration
        """
        return self._request(
            f"/api/s/{self._site}/rest/networkconf",
            method='POST',
            payload=payload
        )

    def set_networksettings_base(self, network_id: str, update_fields: dict):
        """
        Update an existing network configuration
        """
        return self._request(
            f"/api/s/{self._site}/rest/networkconf/{network_id}",
            method='PUT',
            payload=update_fields
        )

    def delete_network(self, network_id: str): 
        """
        Delete a network configuration by ID
        """
        return self._request(
            f"/api/s/{self._site}/rest/networkconf{network_id.strip()}",
            method='DELETE'
        )

    def list_portconf(self):
        """
        List all port configurations on the site.
        """
        return self._request(f"/api/s/{self._site}/list/portconf")

    def get_portconf(self, portconf_id: str):
        """
        Retrieve port configuration by ID
        """
        return self._request(f"/api/s/{self._site}/rest/portconf/{portconf_id}")

    def create_portconf(self, config: dict):
        """
        Create a new port configuration.
        """
        return self._request(
            f"/api/s/{self._site}/rest/portconf",
            method='POST',
            payload=config
        )

    def set_portconf(self, portconf_id: str, config: dict):
        """
        Update an existing port configuration.
        """
        return self._request(
            f"/api/s/{self._site}/rest/portconf/{portconf_id}",
            method='PUT',
            payload=config
        )

    def delete_portconf(self, portconf_id: str):
        """
        Delete a port configuration by ID.
        """
        return self._request(
            f"/api/s/{self._site}/rest/portconf/{portconf_id}",
            method='DELETE'
        )

    def stat_ips_events(self, start: int = None, end: int = None, limit: int = None):
        """Fetch IPS/IDS events (defaults to past 24 hours)."""
        end = end or int(time.time() * 1000)
        start = start or end - (24 * 3600 * 1000)
        limit = limit or 10000
        payload = {'start': start, 'end': end, '_limit': limit}
        return self.fetch_results(f"/api/s/{self._site}/stat/ips/event", payload=payload)

    def stat_sta_sessions(self, mac: str, start: int = None, end: int = None):
        """
        Retrieve client sessions within a time window.
        """
        end = end if end is not None else int(time.time() * 1000)
        start = start if start is not None else end - (7 * 24 * 3600 * 1000)
        payload = {'mac': mac, 'start': start, 'end': end}
        return self._request(f"/api/s/{self._site}/stat/session", method='POST', payload=payload)

    def stat_sta_sessions_latest(self, mac: str, limit: int = None):
        """Fetch latest 'n' login sessions for a client (defaults to 5)."""
        limit = limit or 5
        payload = {'mac': mac.lower(), '_limit': limit, '_sort': '-assoc_time'}
        return self.fetch_results(f"/api/s/{self._site}/stat/session", payload=payload)

    def stat_sta(self, mac: str, start: int = None, end: int = None):
        """
        Retrieve stats for a specific client (STA).
        """
        end = end if end is not None else int(time.time() * 1000)
        start = start if start is not None else end - (7 * 24 * 3600 * 1000)
        payload = {'mac': mac, 'start': start, 'end': end}
        return self._request(f"/api/s/{self._site}/stat/user", method='POST', payload=payload)

    def stat_all_user(self, start: int = None, end: int = None):
        """
        Retrieve usage stats for all users within a time window.
        """
        end = end if end is not None else int(time.time() * 1000)
        start = start if start is not None else end - (7 * 24 * 3600 * 1000)
        payload = {'start': start, 'end': end}
        return self._request(f"/api/s/{self._site}/stat/alluser", method='POST', payload=payload)

    def stat_allusers(self, historyhours: int = 8760):
        """Fetch clients seen within the past N hours (all-time totals)."""
        payload = {'type': 'all', 'conn': 'all', 'within': historyhours}
        return self.fetch_results(f"/api/s/{self._site}/stat/alluser", payload=payload)

    def stat_daily_site(self, start: int = None, end: int = None, attribs: list = None):
        """
        Retrieve daily site statistics with selected attributes.
        """
        end = end if end is not None else int(time.time() * 1000)
        start = start if start is not None else end - (7 * 24 * 3600 * 1000)
        attribs = ['time'] + attribs if attribs else ['time'] + self.default_site_stats_attribs
        payload = {'attrs': attribs, 'start': start, 'end': end}
        return self._request(f"/api/s/{self._site}/stat/report/daily.site", method='POST', payload=payload)

    def stat_monthly_site(self, start: int = None, end: int = None, attribs: list = None):
        """
        Retrieve monthly site statistics with selected attributes.
        """
        end = end if end is not None else int(time.time() * 1000)
        start = start if start is not None else end - (30 * 24 * 3600 * 1000)
        attribs = ['time'] + attribs if attribs else ['time'] + self.default_site_stats_attribs
        payload = {'attrs': attribs, 'start': start, 'end': end}
        return self._request(f"/api/s/{self._site}/stat/report/monthly.site", method='POST', payload=payload)

    def stat_current_user(self):
        """
        Get stats for currently connected users.
        """
        return self._request(f"/api/s/{self._site}/stat/sta")

    def stat_all_users(self):
        """
        Get usage stats for all known users.
        """
        return self._request(f"/api/s/{self._site}/stat/alluser")

    def stat_voucher(self, create_time: int = None):
        """
        Fetch statistics about vouchers, optionally filtering by creation time
        """
        payload = {'create_time': create_time} if create_time is not None else {}
        return self._request(f"/api/s/{self._site}/stat/voucher", payload=payload)

    def stat_payment(self, within: int=None):
        """
        Fetch statistics about payments, optionally filtering by time window
        """
        path_suffix = f"?within={within}" if within is not None else ""
        return self._request(f"api/s/{self._site}/stat/payment{path_suffix}")

    def create_hotspotop(self, name: str, x_password: str, note: str = '') -> bool:
        """Create hotspot operator user"""
        payload = {'cmd': 'create-hotspotop', 'name': name, 'x_password': x_password}
        if note:
            payload['note'] = note.strip()
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/hotspot", payload=payload)

    def list_hotspotop(self):
        """List hotspot operators"""
        return self.fetch_results(f"/api/s/{self._site}/list/hotspotop")



    def stat_auths(self, start: int = None, end: int = None):
        """
        Fetch authorizatoin statistics within a time window
        """
        end = end if end is not None else int(time.time())
        start = start if start is not None else end - (7 * 24 * 3600)
        payload = {'start': start, 'end': end}
        return self._request(f"/api/s/{self._site}/stat/authorization", payload=payload)

    def stat_sessions(self, start: int = None, end: int = None, mac: str = None, type: str = 'all'):
        """
        Retrieve session statistics with optional filtering.
        """
        if type not in ['all', 'guest', 'user']:
            return False

        end = end if end is not None else int(time.time())
        start = start if start is not None else end - (7 * 24 * 3600)
        payload = {'type': type, 'start': start, 'end': end}

        if mac:
            payload['mac'] = mac.lower()

        return self._request(f"/api/s/{self._site}/stat/session", payload=payload)

    def stat_client(self, mac: str):
        """Fetch details for a single client device."""
        return self.fetch_results(f"/api/s/{self._site}/stat/user/{mac.lower().strip()}")

    def list_fingerprint_devices(self, fingerprint_source: int = 0):
        """Fetch client fingerprint devices (default source 0)."""
        return self.fetch_results(f"/v2/api/fingerprint_devices/{fingerprint_source}")

    def set_usergroup(self, client_id: str, group_id: str) -> bool:
        """Assign a client device to a user group."""
        payload = {'usergroup_id': group_id}
        return self.fetch_results_boolean(f"/api/s/{self._site}/upd/user/{client_id.strip()}", payload=payload)

    def list_usergroups(self):
        """Fetch all user groups."""
        return self.fetch_results(f"/api/s/{self._site}/rest/usergroup")

    def create_usergroup(self, group_name: str, qos_rate_max_down: int = -1, qos_rate_max_up: int = -1):
        """Create a new user group via REST."""
        payload = {'name': group_name, 'qos_rate_max_down': qos_rate_max_down, 'qos_rate_max_up': qos_rate_max_up}
        return self.fetch_results(f"/api/s/{self._site}/rest/usergroup", payload=payload)
    
    def edit_usergroup(self, group_id: str, group_name: str, qos_rate_max_down: int = None, qos_rate_max_up: int = None):
        """Modify an existing user group via REST."""
        self._curl_method = 'PUT'
        payload = {'_id': group_id, 'name': group_name}
        if qos_rate_max_down is not None:
            payload['qos_rate_max_down'] = qos_rate_max_down
        if qos_rate_max_up is not None:
            payload['qos_rate_max_up'] = qos_rate_max_up
        result = self.fetch_results(f"/api/s/{self._site}/rest/usergroup/{group_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def delete_usergroup(self, group_id: str) -> bool:
        """Delete a user group via REST."""
        self._curl_method = 'DELETE'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/usergroup/{group_id.strip()}")
        self._curl_method = 'GET'
        return result

    def edit_client_fixedip(self, client_id: str, use_fixedip: bool, network_id: str = None, fixed_ip: str = None):
        """Update a client device's fixed IP via REST."""
        self._curl_method = 'PUT'
        payload = {'_id': client_id, 'use_fixedip': use_fixedip}
        if use_fixedip:
            if network_id:
                payload['network_id'] = network_id
            if fixed_ip:
                payload['fixed_ip'] = fixed_ip
        result = self.fetch_results(f"/api/s/{self._site}/rest/user/{client_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def edit_client_name(self, client_id: str, name: str):
        """Update a client device's name via REST."""

        if not name:
            return False

        self._curl_method = 'PUT'
        payload = {'_id': client_id, 'name': name}
        result = self.fetch_results(f"/api/s/{self._site}/rest/user/{client_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def list_alarms(self, payload: dict = None):
        """
        Retrieve list of alarms with optional filtering payload
        """
        payload = payload or {}
        return self._request(f"/api/s/{self._site}/list/alarm", payload=payload)

    def list_events(self, historyhours: int = 720, start: int = 0, limit: int = 3000):
        payload = {
            '_sort': '-time',
            'within': historyhours,
            'type': null,
            '_start': start,
            '_limit': limit
        }
        return self._request(f"/api/s/{self._site}/stat/event", payload=payload)

    def list_tags(self):
        return self._request(f"/api/s/{self._site}/rest/tag")

    def list_dpi_stats(self):
        """
        List DPI stats.
        """
        return self._request(f"/api/s/{self._site}/stat/dpi")

    def list_dpi_stats_filtered(self, type: str = 'by_cat', cat_filter: list = None):
        """
        Retrieve DPI stats filtered by category or application
        """
        if type not in ['by_cat', 'by_app']:
            return False
        
        payload = {'type': type}

        if isinstance(cat_filter, list) and type == 'by_app':
            payload['cats'] = cat_filter

        return self._request(f"/api/s/{self._site}/stat/sitedpi", payload=payload)

    def list_dpi_app_categories(self):
        """Fetch DPI application categories."""
        return self.fetch_results(f"/api/s/{self._site}/list/dpi/application/categories")

    def list_dpi_app(self):
        """Fetch DPI applications."""
        return self.fetch_results(f"/api/s/{self._site}/list/dpi/application")

    def create_dpi_app(self, name: str, category: str, description: str = None) -> dict:
        """Create a new DPI application."""
        payload = {'name': name, 'category': category}
        if description:
            payload['description'] = description
        return self.fetch_results(f"/api/s/{self._site}/rest/dpi/application", payload=payload)

    def list_country_codes(self):
        return self.fetch_results(f"/api/s/{self._site}/stat/ccode")

    def list_radius_accounts(self):
        return self._request(f"/api/s/{self._site}/rest/account")

    def list_radius_profiles(self):
        """Fetch RADIUS profiles"""
        return self.fetch_results(f"/api/s/{self._site}/rest/radiusprofile")

    def create_radius_account(self, name: str, x_password: str, tunnel_type: int = None, tunnel_medium_type: int = None, vlan: str = None) -> dict:
        """Create a Radius user account with optional tunneling parameters and VLAN"""
        # Validate tunnel parameters
        valid_tunnel_types = {None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}
        valid_medium_types = {None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
        if tunnel_type not in valid_tunnel_types or tunnel_medium_type not in valid_medium_types or ((tunnel_type is None) ^ (tunnel_medium_type is None)):
            return False

        payload = {'name': name, 'x_password': x_password}
        if tunnel_type is not None:
            payload['tunnel_type'] = tunnel_type
        if tunnel_medium_type is not None:
            payload['tunnel_medium_type'] = tunnel_medium_type
        if vlan is not None:
            payload['vlan'] = vlan

        return self.fetch_results(f"/api/s/{self._site}/rest/account", payload=payload)

    def set_radius_account_base(self, account_id: str, payload) -> bool:
        self._curl_method = "PUT"

        return self.fetch_results_boolean(f'/api/s/{self._site}/rest/account/{account_id.strip()}', payload=payload)

    def get_system_log(
        self,
        class_: str = 'device-alert',
        start: int = None,
        end: int = None,
        page_number: int = 0,
        page_size: int = 100,
        custom_payload: dict = None
    ) -> list:
        """Fetch system logs filtered by class and time window with pagination"""
        # Determine time window
        now_ms = int(time.time() * 1000)
        end_ts = end if end is not None else now_ms
        start_ts = start if start is not None else end_ts - (7 * 24 * 3600 * 1000)

        # Base payload
        payload = {
            'pageNumber': page_number,
            'pageSize': page_size,
            'timestampFrom': start_ts,
            'timestampTo': end_ts,
        }

        # Class-specific filters
        if class_ == 'next-ai-alert':
            payload['nextAiCategory'] = ['CLIENT', 'DEVICE', 'INTERNET', 'VPN']
        elif class_ == 'admin-activity':
            payload['activity_keys'] = ['ACCESSED_NETWORK_WEB', 'ACCESSED_NETWORK_IOS', 'ACCESSED_NETWORK_ANDROID']
            payload['change_keys'] = ['CLIENT', 'DEVICE', 'HOTSPOT', 'INTERNET', 'NETWORK', 'PROFILE', 'ROUTING', 'SECURITY', 'SYSTEM', 'VPN', 'WIFI']
        elif class_ == 'update-alert':
            payload['systemLogDeviceTypes'] = ['GATEWAYS', 'SWITCHES', 'ACCESS_POINT', 'SMART_POWER', 'BUILDING_TO_BUILDING_BRIDGES', 'UNIFI_LTE']
        elif class_ == 'client-alert':
            payload['clientType'] = ['GUEST', 'TELEPORT', 'VPN', 'WIRELESS', 'RADIUS', 'WIRED']
            payload['guestAuthorizationMethod'] = ['FACEBOOK_SOCIAL_GATEWAY', 'FREE_TRIAL', 'GOOGLE_SOCIAL_GATEWAY', 'NONE', 'PASSWORD', 'PAYMENT', 'RADIUS', 'VOUCHER']
        elif class_ == 'threat-alert':
            payload['threatTypes'] = ['HONEYPOT', 'THREAT']
        elif class_ == 'triggers':
            payload['triggerTypes'] = ['TRAFFIC_RULE', 'TRAFFIC_ROUTE', 'FIREWALL_RULE']

        # Merge any custom payload overrides
        if custom_payload:
            payload.update(custom_payload)

        return self.fetch_results(f"/v2/api/site/{self._site}/system-log{class_}", payload=custom_payload)

    def delete_radius_account(self, account_id: str) -> bool:
        """Delete a Radius user account"""
        self._curl_method = 'DELETE'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/account/{account_id.strip()}")
        self._curl_method = 'GET'
        return result

    def list_readius_profiles(self):
        return self._request(f"/api/s/{self._site}/rest/radiusprofile")

    def list_hotspot_operators(self):
        return self._request(f"api/s/{self._site}/rest/hotspotop")

    def count_alarms(self, archived: bool = None):
        """
        Count alarms; if archived=False counts only non-archived
        """
        suffix = '?archived=false' if archived is False else ''
        return self._request(f"/api/s/{self._site}/cnt/alarm{suffix}")

    def archive_alarm(self, alarm_id: str = '') -> bool:
        """
        Archive alarms; specific alarm or all
        """
        if alarm_id:
            payload = {'_id': alarm_id, 'cmd': 'archive-alarm'}
        else:
            payload = {'cmd': 'archive-all-alarms'}
        self._request(f"/api/s/{self._site}/cmd/evtmgr", method="POST", payload=payload)
        return self._last_response_code == 200

    def stat_speedtest_results(self, start: int = None, end: int = None):
        """
        Retrieve speed test results with optional start and end times.
        """
        end = end if end is not None else int(time.time() * 1000)
        start = start if start is not None else end - (24 * 3600 * 1000)
        payload = {
            'attrs': ['xput_download', 'xput_upload', 'latency', 'time'],
            'start': start,
            'end': end
        }
        return self._request(f"/api/s/{self._site}/stat/report/archive.speedtest", payload=payload)

    def list_health(self):
        return self._request(f"/api/s/{self._site}/stat/heatlh")

    def stat_user_devices(self):
        """
        Retrieve statistics on user devices.
        """
        return self._request(f"/api/s/{self._site}/stat/user/devices")

    def stat_sites(self):
        """
        Retrieve statistics for all available sites.
        """
        return self._request("/api/stat/sites")

    def list_devices(self, macs: list[str] = []):
        """
        Fetch UniFi devices, optionally filtered by MAC addresses.
        """
        payload = {'macs': [mac.lower() for mac in macs]}
        return self.fetch_results(f"/api/s/{self._site}/stat/device", payload=payload)

    def list_devices_basic(self):
        return self.fetch_results(f"/api/s/{self._site}/stat/device-basic")

    def check_controller_update(self):
        """
        Fetch latest known controller version info
        """
        return self._request(f"/api/s/{self._site}/stat/fwupdate/latest-version")

    def get_update_os_console(self):
        """
        Get recent firmware update for UniFi OS console
        """
        if not self._unifi_os:
            raise NotAUnifiOsConsoleException()
        return self._request('/api/firmware/update')

    def update_os_console(self) -> bool:
        """
        Trigger UniFi OS update
        """
        if not self._unifi_os:
            raise NotAUnifiOsConsoleException()
        payload = {'persistFullData': True}
        self._request(f"/api/s/{self._site}/cmd/firmware/update", method='POST', payload=payload)
        return self._last_response_code == 200


    ## ---------- Deprecated Methods ---------
    def list_aps(self):
        raise MethodDeprecatedException('Function list_aps() has been deprecated, use list_devices() instead.')

    def set_locate_ap(self):
        raise MethodDeprecatedException('Function set_locate_ap() has been deprecated, use locate_ap() instead.') 

    def unset_locate_ap(self) -> bool:
        raise MethodDeprecatedException('Function unset_locate_ap() has been deprecated, use locate_ap() instead.')

    def site_ledson(self) -> bool:
        raise MethodDeprecatedException('Function site_ledson() has been deprecated, use site_leds() instead.')

    def site_ledsoff(self) -> bool:
        raise MethodDeprecatedException('Function site_ledsoff() has been deprecated, use site_leds() instead.')

    def restart_ap(self) -> bool:
        raise MethodDeprecatedException('Function restart_ap() has been deprecated, use restart_device() instead.')

    def get_class_version(self) -> str:
        return self.CLASS_VERSION

    def get_site(self) -> str:
        return self._site

    def set_debug(self) -> bool:
        return getattr(self, '_debug', False)

    def get_last_results_raw(self, return_json: bool = False):
        """Raw API response"""
        if self._last_results_raw is not None:
            if return_json:
                return json.dumps(self._last_results_raw, indent=4)
            return self._last_results_raw
        return False

    def get_last_error_message(self) -> str:
        """Error message of last operation"""
        return self._last_error_message

    def set_cookies(self, cookies_value: str) -> None:
        """
        Set the value for cookies and update timestamp
        """
        self._cookies = cookies_value
        self._cookies_created_at = int(time.time())

    def get_unificookie_name(self) -> str:
        """Get current UniFi cookie name"""
        return self._unificookie_nam

    def get_curl_method(self) -> str:
        """Get current HTTP request method"""
        return self._curl_method

    def set_curl_method(self, curl_method: str) -> str:
        if curl_method not in self.CURL_METHODS_ALLOWED:
            raise InvalidCurlMethodException()
        self._curl_method = curl_method
        return self._curl_method

    def get_curl_ssl_verify_peer(self) -> bool:
        """Get SSL verify peer setting"""
        return self._curl_ssl_verify_peer

    def set_curl_ssl_verify_peer(self, curl_ssl_verify_peer: bool) -> bool:
        """Enable or disable SSL peer verification"""
        self._curl_ssl_verify_peer = curl_ssl_verify_peer
        return True

    def get_curl_ssl_verify_host(self) -> int:
        """Get SSL verify host setting"""
        return self._curl_ssl_verify_host

    def set_curl_ssl_verify_host(self, curl_ssl_verify_host: int) -> bool:
        """Set SSL verify host level"""
        if curl_ssl_verify_host not in [0, 1, 2]:
            return False

        self._curl_ssl_verify_host = curl_ssl_verify_host
        return True

    def get_is_unifi_os(self) -> bool:
        """Check if connected controller is UniFi OS-based"""
        return self._unifi_os

    def set_is_unifi_os(self, is_unifi_os: bool) -> bool:
        """Flag controller as UniFi OS-based or not"""
        self._unifi_os = is_unifi_os
        return True

    def set_connection_timeout(self, timeout: int) -> bool:
        """Set connection timeout in seconds"""
        self._connection_timeout = timeout
        return True

    def get_connection_timeout(self) -> int:
        """Get current connection timeout"""
        return self._connect_timeout

    def set_curl_request_timeout(self, timeout: int) -> bool:
        """Set request timeout in seconds"""
        self._request_timeout = timeout
        return True

    def get_curl_request_timeout(self) -> int:
        """Get current request timeout"""
        return self._request_timeout

    def set_curl_http_version(self, http_version: int) -> bool:
        """Specify HTTP version for requests"""
        self._curl_http_version = http_version
        return True

    def get_curl_http_version(self) -> int:
        """Get HTTP version currently set"""
        return self._curl_http_version

    # ----- Protected Helper Methods -----

    def fetch_results_boolean(self, path: str, payload=None, login_required: bool = True, prefix_path: bool = True) -> bool:
     return self.fetch_results(path, payload, boolean=True, login_required=login_required, prefix_path=prefix_path)

    def _get_json_last_error(self) -> bool:
        try:
            json.loads(self._last_results_raw)
            return True
        except json.JSONDecodeError as e:
            # Try to match the error message like PHP's cases
            message = e.msg.lower()

            if "depth" in message:
                error = "The maximum stack depth has been exceeded"
            elif "expecting" in message or "syntax" in message:
                error = "Syntax error, malformed JSON"
            elif "control character" in message:
                error = "Control character error, possibly incorrectly encoded"
            elif "utf-8" in message:
                error = "Malformed UTF-8 characters, possibly incorrectly encoded"
            else:
                error = "Unknown JSON error occurred"

            raise JsonDecodeException(f"JSON decode error: {error}")

    def _check_base_url(self, baseurl: str) -> bool:
            """
            Validate base URL format and set it
            """
            if not re.match(r'^https?://', baseurl):
                raise InvalidBaseUrlException(f"Invalid base url {baseurl}")
            self._baseurl = baseurl
            return True

    def generate_backup(self, days: int = -1):
        """Generate a controller backup for the past N days."""
        payload = {'cmd': 'backup', 'days': days}
        result = self.fetch_results(f"/proxy/network/api/s/{self._site}/cmd/backup", payload=payload, prefix_path=False, boolean=False)
        print(f"RAW RESULT FROM FETCH_RESULTS(): {result}")
        return result

    def download_backup(self, filepath: str):
        """Download a generated backup file."""
        #with open(filepath, 'rb') as f:
           # return f.read()
        return self.exec_curl(filepath)

    def restore_backup(self, filename: str):
        """
        Restore a contorller backup (.unf) that already exists on the controller
        """
        payload = {
            'cmd': 'restore-backup',
            'file': filename
        }
        return self.fetch_results(f"/api/s/{self._site}/cmd/backup", payload=payload, prefix_path=True)

    def generate_backup_site(self):
        """Generate a site export backup."""
        payload = {'cmd': 'export-site'}
        return self.fetch_results(f"/api/s/{self._site}/cmd/backup", payload=payload)

    def list_portforwarding(self):
        """Fetch port forwarding settings"""
        return self.fetch_results(f"/api/s/{self._site}/list/portforward")

    def list_portforward_stats(self):
        """Fetch port forwarding stats"""
        return self.fetch_results(f"/api/s/{self._site}/stat/portforward")

    def list_extension(self):
        """Fetch VoIP extensions"""
        return self.fetch_results(f"/api/s/{self._site}/list/extension")

    def list_settings(self):
        """Fetch site settings"""
        return self.fetch_results(f"/api/s/{self._site}/get/setting")

    def adopt_device(self, macs):
        """Adopt one or more devices to the current site"""
        payload = {'cmd': 'adopt', 'macs': [m.lower() for m in (macs if isinstance(macs, list) else [macs])]}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr", payload=payload)

    def advanced_adopt_device(
        self,
        mac: str,
        ip: str,
        username: str,
        password: str,
        url: str,
        port: int = 22,
        ssh_key_verify: bool = True
    ) -> bool:
        """Advanced SSH-based device adoption"""
        payload = {
            'cmd': 'adv-adopt',
            'mac': mac.lower(),
            'ip': ip,
            'username': username,
            'password': password,
            'url': url,
            'port': port,
            'sshKeyVerify': ssh_key_verify,
        }
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/cmd/devmgr",
            payload=payload
        )

    def restart_device(self, macs, reboot_type: str = 'soft') -> bool:
        """Restart one or more devices with optional reboot type ('soft' or 'hard')"""
        mac_list = [m.lower() for m in (macs if isinstance(macs, list) else [macs])]
        payload = {'cmd': 'restart', 'macs': mac_list}
        if reboot_type and reboot_type.lower() in ['soft', 'hard']:
            payload['reboot_type'] = reboot_type.lower()
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr", payload=payload)

    def list_dynamicdns(self):
        """Fetch dynamic DNS settings"""
        return self.fetch_results(f"/api/s/{self._site}/rest/dynamicdns")

    def create_dynamicdns(self, payload: dict) -> bool:
        """Create dynamic DNS settings"""
        return self.fetch_results_boolean(f"/api/s/{self._site}/rest/dynamicdns", payload=payload)

    def set_dynamicdns(self, dynamicdns_id: str, payload: dict) -> bool:
        """Update site dynamic DNS settings"""
        self._curl_method = 'PUT'
        result = self.fetch_results_boolean(f"/api/s/{self._site}/rest/dynamicdns/{dynamicdns_id.strip()}", payload=payload)
        self._curl_method = 'GET'
        return result

    def list_dns_records(self) -> list:
        return self.fetch_results(f'/v2/api/site/{self._site}/static-dns')

    def create_dns_record(self, record_type: str, value: str, key: str, ttl: int = None, enabled: bool = True) -> dict:
        if record_type not in ['A', 'AAAA', 'MX', 'TXT', 'SRV', 'NS']:
            raise Exception(f'Invalid record type: {record_type}')

        payload = {
            'record_type': record_type,
            'value': value,
            'key': key,
            'enabled': enabled
        }

        if ttl is not None:
            payload['ttl'] = ttl

        return self.fetch_results(f'/v2/api/site/{self._site}/static-dns', payload=payload)

    def delete_dns_record(self, record_id: str) -> bool:
        self._curl_method = "DELETE"

        return self.fetch_results_boolean(f'/v2/api/site/{self._site}/static-dns/{record_id}')

    def list_device_states(self) -> list:
        return {
            0: 'offline',
            1: 'connected',
            2: 'pending adoption',
            4: 'updating',
            5: 'provisioning',
            6: 'unreachable',
            7: 'adopting',
            9: 'adoption error',
            10: 'adoption failed',
            11: 'isolated'
        }

    def list_rogueaps(self, within: int = 24):
        """Fetch rogue/neighboring access points"""
        payload = {'within': within}
        return self.fetch_results(f"/api/s/{self._site}/stat/rogueap", payload=payload)

    def extend_guest_validity(self, guest_id: str) -> bool:
        """Extend guest authorization"""
        payload = {'_id': guest_id, 'cmd': 'extend'}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/hotspot", payload=payload)

    def list_current_channels(self):
        """Fetch current channels"""
        return self.fetch_results(f"/api/s/{self._site}/stat/current-channel")

    def migrate_device(self, macs, inform_url: str) -> bool:
        """Migrate one or more devices to new inform URL."""
        payload = {'cmd': 'migrate', 'inform_url': inform_url, 'macs': [m.lower() for m in (macs if isinstance(macs, list) else [macs])]}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr", payload=payload)

    def cancel_migrate_device(self, macs) -> bool:
        """Cancel migration for one or more devices."""
        payload = {'cmd': 'cancel-migrate', 'macs': [m.lower() for m in (macs if isinstance(macs, list) else [macs])]}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr", payload=payload)

    def force_provision(self, mac) -> bool:
        """Force provision one or more devices."""
        payload = {'cmd': 'force-provision', 'macs': [m.lower() for m in (mac if isinstance(mac, list) else [mac])]}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr/", payload=payload)

    def reboot_cloudkey(self) -> bool:
        """Reboot a UniFi CloudKey."""
        payload = {'cmd': 'reboot'}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/system", payload=payload)

    def disable_ap(self, ap_id: str, disable: bool) -> bool:
        """Disable or enable an access point."""
        self._curl_method = 'PUT'
        payload = {'disabled': disable}
        return self.fetch_results_boolean(f"/api/s/{self._site}/rest/device/{ap_id.strip()}", payload=payload)

    def led_override(self, device_id: str, override_mode: str) -> bool:
        """Override LED mode for a device: 'off', 'on', or 'default'."""
        if override_mode not in ['off', 'on', 'default']:
            return False
        self._curl_method = 'PUT'
        payload = {'led_override': override_mode}
        return self.fetch_results_boolean(f"/api/s/{self._site}/rest/device/{device_id.strip()}", payload=payload)

    def locate_ap(self, mac: str, enable: bool) -> bool:
        """Toggle AP locate LED on or off."""
        cmd = 'set-locate' if enable else 'unset-locate'
        payload = {'cmd': cmd, 'mac': mac.lower()}
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr", payload=payload)

    def site_leds(self, enable: bool) -> bool:
        """Toggle LEDs of all access points on or off."""
        payload = {'led_enabled': enable}
        return self.fetch_results_boolean(f"/api/s/{self._site}/set/setting/mgmt", payload=payload)

    def custom_api_request(self, path: str, method: str = 'GET', payload=None, return_type: str = 'array', prefix_path: bool = False):
        """Execute custom API request with optional boolean or array return."""
        if method not in self.CURL_METHODS_ALLOWED:
            return False
        if not path.startswith('/'):
            return False
        self._curl_method = method
        if return_type == 'array':
            return self.fetch_results(path, payload, prefix_path)
        if return_type == 'boolean':
            return self.fetch_results_boolean(path, payload, prefix_path)
        return False 

    def get_cookie(self) -> str:
        return self._cookies

    def get_cookies(self) -> str:
        return self._cookies

    def get_cookies_created_at(self) -> int:
        return self._cookies_created_at
    
    def __construct(
        self,
        user: str,
        password: str,
        baseurl: str = 'https://127.0.0.1:8443',
        site: str = 'default',
        version: str = '8.0.28',
        ssl_verify: bool = False,
        unificookie_name: str = 'unificookie'
    ):
        """
        PHP constructor conversion: checks and initial assignments.
        """
        # Ensure HTTP client available
        self._check_curl()
        # Validate base URL and site
        self._check_base_url(baseurl)
        self._check_site(site)

        # Assign core properties
        self._baseurl = baseurl.strip()
        self._site = site.strip().lower()
        self._user = user.strip()
        self._password = password.strip()
        self._version = version.strip()
        self._unificookie_name = unificookie_name.strip()

        # SSL verification settings
        self._verify_ssl_cert = ssl_verify

    def __destruct(self):
        """
        PHP destructor: if the unificookie is set in session, skip logout; otherwise logout if logged in.
        """
        # If the unificookie is present in session cookies, skip logout
        if self._unificookie_name in self._session.cookies.get_dict():
            return

        # Logout if still logged in
        if getattr(self, '_is_loggedin', False):
            try:
                self.logout()
            except Exception:
                pass

    def list_firewallgroups(self, group_id: str = ''):
        return self.fetch_results(f"/api/s/{self._site}/rest/firewallgroup/{group_id.strip()}")

    def create_firewallgroup(self, group_name: str, group_type: str, group_members: list = []) -> bool:
        """Create a new firewall group"""
        # Only allow specific group types
        if group_type not in ['address-group', 'ipv6-address-group', 'port-group']:
            return False
        payload = {
            'name': group_name,
            'group_type': group_type,
            'group_members': group_members
        }
        return self._request(
            f"/api/s/{self._site}/rest/firewallgroup",
            method='POST',
            payload=payload
        )

    def edit_firewallgroup(self, group_id: str, site_id: str, group_name: str, group_type: str, group_members: list = []) -> bool:
        """Edit an existing firewall group"""
        # Only allow specific group types
        if group_type not in ['address-group', 'ipv6-address-group', 'port-group']:
            return False
        # Prepare payload
        payload = {
            '_id': group_id,
            'name': group_name,
            'group_type': group_type,
            'group_members': group_members,
            'site_id': site_id
        }
        return self._request(
            f"/api/s/{self._site}/rest/firewallgroup/{group_id.strip()}",
            method='PUT',
            payload=payload
        )

    def delete_firewallgroup(self, group_id: str) -> bool:
        self._curl_method = "DELETE"
        return self.fetch_results_boolean(f'/api/s/{self._site}/rest/firewallgroup/{group_id.strip()}')
        self._curl_method = "GET"

    def list_firewallrules(self):
        return self._request(f"/api/s/{self._site}/rest/firewallrule")

    def list_routing(self, route_id: str = ''):
        return self.fetch_results(f"/api/s/{self._site}/rest/routing/{route_id.strip()}")

    def set_tagged_devices(self, macs: list, tag_id: str) -> bool:
        self._curl_method = "PUT"
        payload = {'member_table': macs}
        return self.fetch_results_boolean(f"/api/s/{self._site}/rest/tag/{tag_id}", payload=payload)

    def set_ap_radiosettings(self, ap_id: str, radio: str, channel: int, ht: int, tx_power_mode: str, tx_power: int) -> bool:
        """Set AP radio settings"""
        payload = {
            'radio_table': {
                'radio': radio,
                'channel': channel,
                'ht': ht,
                'tx_power_mode': tx_power_mode,
                'tx_power': tx_power,
            }
        }
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/upd/device/{ap_id.strip()}",
            payload=payload
        )

    def set_ap_wlangroup(self, type_id: str, device_id: str, group_id: str) -> bool:
        """Assign AP to WLAN group based on radio type 'ng' or 'na'"""
        # Only allow specific radio types
        if type_id not in ['ng', 'na']:
            return False
        payload = {
            'wlan_overrides': [],
            f'wlangroup_id_{type_id}': group_id
        }
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/upd/device/{device_id.strip()}",
            payload=payload
        )

    def set_guestlogin_settings_base(self, payload: dict, section_id: str = '') -> bool:
        """Update guest login settings, base. Applies to a specific section if section_id provided."""
        # Append section_id to path if given
        suffix = f"/{section_id}" if section_id else ''
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/set/setting/guest_access{suffix}",
            payload=payload
        )

    def set_guestlogin_settings(
        self,
        portal_enabled: bool,
        portal_customized: bool,
        redirect_enabled: bool,
        redirect_url: str,
        x_password: str,
        expire_number: int,
        expire_unit: int,
        section_id: str
    ) -> bool:
        """Configure guest login settings with full options."""
        payload = {
            'portal_enabled': portal_enabled,
            'portal_customized': portal_customized,
            'redirect_enabled': redirect_enabled,
            'redirect_url': redirect_url,
            'x_password': x_password,
            'expire_number': expire_number,
            'expire_unit': expire_unit,
            '_id': section_id,
        }
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/set/setting/guest_access/{section_id}",
            payload=payload
        )

    def set_guestlogin_settings_base(self, payload: dict, section_id: str = '') -> bool:
        """Update guest login settings, base. Applies to a specific section if section_id provided."""
        suffix = f"/{section_id}" if section_id else ''
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/set/setting/guest_access{suffix}",
            payload=payload
        )

    def set_ips_settings_base(self, payload: dict) -> bool:
        """Update IPS/IDS settings, base."""
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/set/setting/ips",
            payload=payload
        )

    def set_super_mgmt_settings_base(self, settings_id: str, payload: dict) -> bool:
        """Update "Super Management" settings, base."""
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/set/setting/super_mgmt/{settings_id.strip()}",
            payload=payload
        )

    def set_super_smtp_settings_base(self, settings_id: str, payload: dict) -> bool:
        """Update "Super SMTP" settings, base."""
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/set/setting/super_smtp/{settings_id.strip()}",
            payload=payload
        )

    def set_super_identity_settings_base(self, settings_id: str, payload: dict) -> bool:
        """Update "Super Controller Identity" settings, base."""
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/set/setting/super_identity/{settings_id.strip()}",
            payload=payload
        )

    def rename_ap(self, ap_id: str, ap_name: str) -> bool:
        payload = {'name': ap_name}
        return self.fetch_results_boolean(f'/api/s/{self._site}/upd/device/{ap_id.strip()}', payload=payload)

    def move_device(self, mac: str, site_id: str) -> bool:
        """Move a device to another site"""
        payload = {'cmd': 'move-device', 'site': site_id, 'mac': mac.lower()}
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/cmd/sitemgr",
            payload=payload
        )

    def delete_device(self, mac: str) -> bool:
        payload = {'cmd': 'delete-device', 'mac': mac.lower()}

        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/sitemgr", payload=payload)

    def check_firmware_update(self) -> bool:
        payload = {'cmd': 'check-firmware-update'}

        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/productinfo", payload=payload)

    def upgrade_device(self, mac: str) -> bool:
        payload = {'mac': mac.lower()}

        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr/upgrade", payload=payload)

    def upgrade_all_devices(self, type: str = 'uap') -> bool:
        payload = {'type': type.lower()}

        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr/upgrade-all", payload=payload)

    def upgrade_device_external(self, firmware_url: str, macs: list) -> bool:
        """Upgrade devices using an external firmware URL and list of MAC addresses"""
        # Sanitize URL and normalize MACs
        sanitized_url = firmware_url.strip()
        macs_list = [m.lower() for m in macs]
        payload = {
            'url': sanitized_url,
            'macs': macs_list
        }
        return self.fetch_results_boolean(
            f"/api/s/{self._site}/cmd/devmgr/upgrade-external",
            payload=payload
        )

    def start_rolling_upgrade(self, payload: list = {'uap', 'usw', 'ugw', 'uxg'}) -> bool:
        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr/set-rollupgrade", payload=payload)

    def cancel_rolling_upgrade(self) -> bool:
        payload = {"cmd": "unset-rollupgrade"}

        return self.fetch_results_boolean(f"/api/s/{self._site}/cmd/devmgr", payload=payload)

    def list_firmware(self, type: str="available"):
        if type not in ['available', 'cached']:
            return False

        payload = {'cmd': f'list-{type}'}

        return self.fetch_results(f"/api/s/{self._site}/cmd/firmware", payload=payload)

    def get_debug(self) -> bool:
        return getattr(self, 'debug', False)

    def fetch_results(
        self,
        path: str,
        payload = None,
        boolean: bool = False,
        login_required: bool = False,
        prefix_path: bool = False
    ):
        if login_required and not self._is_loggedin:
            raise LoginRequiredException()

        self._last_results_raw = self.exec_curl(path, payload, prefix_path)
        self._last_results_raw = self._last_results_raw.decode()

        if isinstance(self._last_results_raw, str):
            try:
                response = json.loads(self._last_results_raw)
                print("Fetched response:", response)
            except:
                self._get_json_last_error()
                raise

            if isinstance(response, dict) and 'meta' in response:
                if response['meta'].get('rc') == 'ok':
                    self._last_error_message = ''
                    if 'data' in response:
                        if isinstance(response['data'], list):
                            print("Response inside fetch_results():", response)
                            print("Data:", response.get("data"))
                            return response['data'] if not boolean else True
                        return [response['data']] if not boolean else True
                    return True
                elif response['meta'].get('rc') == 'error':
                    self._last_error_message = 'An unknown error was returned by the controller'

                    raise Exception(f"Error message: {self._last_error_message}")

            if path.startswith('/v2/api/'):
                if 'errorCode' in response:
                    self._last_error_message = 'AN unkown error was returned by an API v2 endpoind'
                    raise Exception(f"Error code: {response['errorCode']}, message: {self.last_error_message}")
                return response

            # UniFi OS response
            if path.startswith('/api/'):
                if 'code' in response:
                    self._last_error_message = response.get('message', 'An unknown error was returned by a UniFi OS endpoint.')
                    raise Exception(f"Error code: {response['code']}, message: {self._last_error_message}")
                if not boolean:
                    return [response]
                return True
        return False

    def fetch_results_boolean(
        self,
        path: str,
        payload=None,
        login_required: bool = True,
        prefix_path: bool = True
    ) -> bool:
        """Call fetch_results and always return a boolean"""
        return self.fetch_results(path, payload, True, login_required, prefix_path)

    def get_json_last_error(self) -> bool:
        """Raise exception with message matching last JSON decoding error."""
        error_code = json.JSONDecodeError
        error_map = {
            0: 'No error',
            1: 'The maximum stack depth has been exceeded',
            2: 'Invalid or malformed JSON',
            3: 'Control character error, possibly incorrectly encoded',
            4: 'Syntax error, malformed JSON',
            5: 'Malformed UTF-8 characters, possibly incorrectly encoded',
            6: 'One or more recursive references in the value to be encoded',
            7: 'One or more NAN or INF values in the value to be encoded',
            8: 'A value of a type that cannot be encoded was given',
            9: 'A property name that cannot be encoded was given',
            10: 'Malformed UTF-16 characters, possibly incorrectly encoded',
        }

        # Attempt to find error from last decoding (simulate json_last_error from PHP)
        error = error_map.get(getattr(error_code, 'errno', None), 'Unknown JSON error occurred')
        raise Exception(f'JSON decode error: {error} JSON decode error: ' + error_map.get(json.JSONDecodeError, 'Unknown JSON error occurred'))

    def check_base_url(self, baseurl: str) -> bool:
        parsed = urlparse(baseurl)
        if not all([parsed.scheme, parsed.netloc]) or baseurl.endswith("/"):
            raise InvalidBaseUrlException()

        return True

    def exec_curl(self, path: str, payload=None, prefix_path: bool = True):
        # 1) method sanity check
        if self._curl_method not in self.CURL_METHODS_ALLOWED:
            raise InvalidCurlMethodException()

        # 2) build URL
        url = f"{self._baseurl}{path}"
        if self._unifi_os and prefix_path:
            url = f"{self._baseurl}/proxy/network{path}"

        # 3) build curl_options dict
        """
        curl_options = {
            'method': self._curl_method,
            'url': url,
            'headers': None,     # filled in below
            'timeout': 30,
            'verify': self._verify_ssl_cert,
        }
        """

        opts = self.get_curl_handle()

        opts.update({
            'method': self._curl_method,
            'url': url,
            'headers': { **opts['headers'], **self._curl_headers}
        })

        # 4) handle payload
        json_payload = ''
        if payload:
            json_payload = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
            opts['data'] = json_payload

            # force POST if GET or DELETE
            if self._curl_method in ('GET', 'DELETE'):
                self._curl_method = 'POST'
                opts['method'] = 'POST'

        # 5) set custom method flags
        if self._curl_method == 'POST':
            # nothing extra; requests uses method field
            pass
        elif self._curl_method in ('DELETE', 'PUT', 'PATCH'):
            opts['method'] = self._curl_method

        # 6) CSRF for UniFi OS non-GET
        if self._unifi_os and self._curl_method != 'GET':
            self.create_x_csrf_token_header()

        # 7) attach headers last
        opts['headers'] = self._curl_headers

        # 8) perform request
        try:
            opts['verify'] = False
            resp = self._session.request(**opts)
        except Timeout as e:
            raise CurlTimeoutException(str(e), None, None)
        except RequestException as e:
            raise CurlGeneralErrorException(f"Request error: {e}", None, None)

        http_code = resp.status_code

        # 9) handle expired auth
        if http_code == 401:
            if self.get_debug:
                print(f"exec_curl: 401 on {url}, need to re-login")
            if self._exec_retries == 0:
                # clear stored cookie/token
                self.cookies = ''
                self.cookies_created_at = 0
                self.is_logged_in = False
                self._exec_retries += 1

                if self._session:
                    self._session.close()
                # attempt re-login
                from time import sleep
                if self.login():
                    if self.get_debug:
                        print("exec_curl: re-login succeeded, retrying exec_curl")
                    return self.exec_curl(path, payload, prefix_path)
                raise LoginFailedException('Cookie/Token expired and re-login failed.')
            raise LoginFailedException('Login failed, check credentials.')

        # 10) debug dump
        if self.get_debug:
            print("\n---------cURL INFO-----------")
            print("Options:", opts)
            print("URL & PAYLOAD:", url)
            print("Payload:", json_payload or '<empty>')
            print("Response Code:", http_code)
            print("Response Body:", resp.text)
            print("-----------------------------\n")

        # 11) reset method and retry count
        self._curl_method = self.DEFAULT_CURL_METHOD
        self._exec_retries = 0

        return resp.content

    def get_curl_handle(self):
        """
        Mirror PHP's get_curl_handle():
        builds a curl_options dict for requests.Session.request()
        """
        # Determine SSL verification
        verify_ssl = bool(self.get_curl_ssl_verify_peer and self.get_curl_ssl_verify_host)

        # Map connect & overall timeouts
        curl_options = {
            'timeout': (self.get_connection_timeout(), self.get_curl_request_timeout()),
            'verify': verify_ssl,
            'headers': {},
        }

        # Verbose logging if debug
        if self.get_debug:
            # shows per-request wire logs
            logging.getLogger('urllib3').setLevel(logging.DEBUG)

        # Attach cookies if present
        if getattr(self, 'cookies', None):
            curl_options['headers']['Cookie'] = self._cookies

        return curl_options

    def response_header_callback(self, response: requests.Response):
        """
        Process Set-Cookie headers to extract UniFi session or TOKEN cookie.
        """
        cookies = []
        raw = getattr(response, 'raw', None)
        if raw and hasattr(raw, 'headers') and hasattr(raw.headers, 'get_all'):
            cookies = raw.headers.get_all('Set-Cookie') or []
        else:
            sc = response.headers.get('Set-Cookie')
            if sc:
                cookies = [sc]
        for header in cookies:
            for crumb in (c.strip() for c in header.split(';')):
                if 'unifises' in crumb:
                    self._cookies = crumb
                    self._cookies_created_at = int(time.time())
                    self._is_loggedin = True
                    self._unifi_os = False
                    return
                if 'TOKEN' in crumb:
                    self._cookies = crumb
                    self._cookies_created_at = int(time.time())
                    self._is_loggedin = True
                    self._unifi_os = True
                    return

    def create_x_csrf_token_header(self):
        # 1) Do we even have a TOKEN cookie?
        cookies = getattr(self, 'cookies', '')
        if not cookies or 'TOKEN' not in cookies:
            return

        # 2) Split on first '=', get the JWT
        parts = cookies.split('=', 1)
        if len(parts) < 2:
            return
        jwt = parts[1]

        # 3) Split JWT into its three '.' parts
        comps = jwt.split('.')
        if len(comps) < 2:
            return
        payload_b64 = comps[1]

        # 4) Pad base64 to correct length
        pad_len = (-len(payload_b64)) % 4
        if pad_len:
            payload_b64 = payload_b64 + ('=' * pad_len)

        # 5) Decode base64 -> bytes, then bytes -> str
        try:
            decoded_bytes = base64.b64decode(payload_b64)
            decoded_str   = decoded_bytes.decode('utf-8')
            payload_dict  = json.loads(decoded_str)
        except Exception:
            return

        # 6) Extract the token
        csrf_token = payload_dict.get('csrfToken')
        if not csrf_token:
            return

        # 7) Remove any existing x-csrf-token headers (case-insensitive)
        filtered = []
        for header in self.curl_headers:
            if header.lower().find('x-csrf-token:') == -1:
                filtered.append(header)
        self.curl_headers = filtered

        # 8) Append the new header, using only ASCII
        self.curl_headers.append('x-csrf-token: %s' % csrf_token)