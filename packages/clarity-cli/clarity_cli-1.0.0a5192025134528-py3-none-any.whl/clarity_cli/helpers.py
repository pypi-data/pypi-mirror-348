import json
import jwt
import datetime
import base64
import requests
from clarity_cli.outputs import CliOutput
from clarity_cli.defs import CONFIG_DIR, TOKEN_FILE, CONFIG_FILE, ProfileConfig, EXECUTION_VIEW_PATH, TEST_LIST, DEVICES_LIST
from clarity_cli.exceptions import StopCommand, UnAuthenticated
out = CliOutput()


def ensure_config_dir():
    """Ensure the config directory exists"""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
        out.ok("Created configuration directory at ~/.clarity")


def is_logged_in(profile):
    """Check if the user is logged in by verifying the token"""
    if not TOKEN_FILE.exists():
        raise UnAuthenticated()
    out.vprint("Token file found")
    try:
        with open(TOKEN_FILE, 'r') as f:
            token_data = json.load(f)

        # Verify token hasn't expired
        token = token_data.get(profile)
        if not token:
            raise UnAuthenticated()
        out.vprint("Token was loaded successfully")
        # Decode the token without verification to check expiration
        decoded = jwt.decode(token, options={"verify_signature": False})
        out.vprint("Token was parsed successfully")
        exp_timestamp = decoded.get('exp', datetime.datetime.now(datetime.timezone.utc))

        # Check if token has expired
        if datetime.datetime.fromtimestamp(exp_timestamp, tz=datetime.timezone.utc) < datetime.datetime.now(datetime.timezone.utc):
            out.warning(
                "Your session has expired. Please login again.")
            raise UnAuthenticated()

        return token

    except Exception as e:
        out.error(f"Error checking login status: {str(e)}")
        raise UnAuthenticated()


def format_device_state(device):
    if device['state'] == 'connected':
        device['state'] = f"[green]{device['state']}[/green]"
    if device['state'] == 'disconnected':
        device['state'] = f"[red]{device['state']}[/red]"
    else:
        device['state'] = f"[yellow]{device['state']}[/yellow]"


def get_devices(token, workspace_id, domain):
    headers = {"Authorization": f"Bearer {token}", "workspace": workspace_id}
    url = f"{domain}/{DEVICES_LIST}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        res = response.json()
        devices = res['device_list']
        return devices
    else:
        out.vprint("Error getting devices list")
        out.vprint(response.text)
        raise StopCommand("Couldn't get devices list")


def get_tests(token, workspace_id, domain):
    headers = {"Authorization": f"Bearer {token}", "workspace": workspace_id}
    url = f"{domain}/{TEST_LIST}"
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    param_res = {}
    if response.status_code == 200:
        res = response.json()
        for test in res:
            param_res[test['test_id']] = test['params_schema']
        return res, param_res
    else:
        out.vprint("Error getting tests list")
        out.vprint(response.text)
        raise StopCommand("Couldn't get Test list")


def trigger_test_execution(domain, token, workspace, project_id, agent_id, test_id, params):
    headers = {"Authorization": f"Bearer {token}", "workspace": workspace}
    url = f"{domain}/inv-api/testing/executions/handler"
    data = {
        "project_id": project_id,
        "agent_id": agent_id,
        "test_plan_config": [{
            "params_config": {},
            "test_id": test_id,
            "test_config": {'variables_config':  params}
        }
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    # Check if the request was successful
    if response.status_code == 202:
        res = response.json()
        out.ok("Execution started")
        out.vprint(f"execution id: {res['execution_id']}, project id: {res['project_id']}")
        # return URL to track the execution
        return f"{domain}/{EXECUTION_VIEW_PATH.format(execution_id=res['execution_id'], project_id=res['project_id'])}"
    else:
        out.vprint("Status code:", response.status_code)
        raise StopCommand(f"Failed to start execution, {response.text}")


def get_clarity_access_token(profile, client_id, client_secret, token_endpoint, scope):
    # The client credentials grant requires HTTP Basic Authentication,
    # where the username is the client ID and the password is the client secret
    try:
        client_auth = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {client_auth}",
        }

        # The grant_type must be client_credentials
        data = {
            "grant_type": "client_credentials",
            "scope": scope,
        }
        response = requests.post(token_endpoint, headers=headers, data=data)

        if response.status_code != 200:
            out.verbose(response.text)
            raise StopCommand("Failed to get access token")

        response_data = response.json()
        out.vprint(f"Got token: {response_data['access_token']}")
        write_token(response_data["access_token"], profile)
    except Exception as e:
        out.vprint(f"Login error - {e}")
        raise StopCommand("Unable to login")


def read_config(config_override=None):
    config_to_use = config_override or CONFIG_FILE
    try:
        out.vprint(f"Reading config file: {config_to_use}")
        with open(config_to_use, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def read_token():
    try:
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def get_params(params_file):
    try:
        with open(params_file, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def write_new_profile_to_config(profile_name: str, default: bool, config: ProfileConfig):
    try:
        cur_config = read_config()
        new_profile = {
            profile_name: config.model_dump()
        }
        full_config = {**cur_config, **new_profile}
        full_config['default'] = profile_name if default else full_config.get('default', "")
        with open(CONFIG_FILE, "w") as f:
            json.dump(full_config, f)
    except Exception as e:
        StopCommand(f"An error occurred while writing new profile to config file - {e}")


def write_token(token, profile):
    tokens = read_token()
    tokens[profile] = token
    try:
        out.vprint(f"writing token to {TOKEN_FILE}, for profile: {profile}")
        with open(TOKEN_FILE, 'w') as f:
            json.dump(tokens, f)
    except Exception as e:
        StopCommand(f"Unable to write tmp token to: {TOKEN_FILE} - {e}")


def get_profile_configuration(profile=None, override_config_path=None):
    current_configuration = read_config(override_config_path)
    if not profile:
        out.warning("Profile was not provided, using default profile")
        profile = current_configuration.get('default')
        if profile:
            out.ok(f"Default profile found, using {profile} profile")
        else:
            raise StopCommand("Default profile wasn't configured, please specify a profile")
    try:
        profile_config = ProfileConfig(**current_configuration.get(profile, {}))
        if not profile_config:
            out.error(f"profile {CliOutput.bold(profile)} was not found")
            out.warning("use "+{CliOutput.bold('\'clarity profile-setup\'')} + "command to set it up")
    except Exception as e:
        # is_valid_config = all([True if key in profile_config else False for key in ['client_id', 'client_secret', 'token_endpoint', 'scope']])
        # if not is_valid_config:
        out.vprint(f"Error parsing config - {e}")
        out.warning("use "+{CliOutput.bold('\'clarity profile-setup\'')} + "command to set it up")
        raise StopCommand("Profile configuration is not valid, please reconfigure or use another profile")
    return profile_config, profile
