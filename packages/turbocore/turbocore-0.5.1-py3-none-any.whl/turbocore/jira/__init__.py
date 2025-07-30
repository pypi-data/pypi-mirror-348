import urllib.parse
import turbocore
import os
import requests
from rich.pretty import pprint as PP
import sys



def get_base_url():
    host = get_base_host()
    return "https://%s" % host

def get_base_host():
    host = os.environ.get("TJI_HOST")
    return host


def get_token():
    token = os.environ.get("TJI_TOKEN")
    return token


def get_user():
    token = os.environ.get("TJI_USER")
    return token


def direct_get(full_url):
    res = req(verb="GET", route=full_url)
    return res.json()


def req(verb, route, data=None, stream=False) -> requests.Response:
    
    if not route.startswith("/") and not route.startswith("http://") and not route.startswith("https://"):
        raise Exception("parameter 'route' must start with a '/'")

    f_ = {
        "GET": requests.get,
        "POST": requests.post,
    }

    if not verb.upper() in f_.keys():
        raise Exception("Unsupported http verb '%s'" % verb)

    hdr = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    #    "Authorization": "Bearer %s" % get_token()

    auth=(get_user(), get_token())
    url = get_base_url() + route
    
    # special case we have a full url
    if not route.startswith("/"):
        url = route

    url_host_actual = url.split("//")[1].split("/")[0].split(":")[0]
    if url_host_actual is None or url_host_actual == "" or url_host_actual != get_base_host():
        raise Exception("Unsafe host in API call detected, %s" % str(url_host_actual))
    
    #res = f_[verb](url=url, headers=hdr, data=data)
    res = f_[verb](url=url, headers=hdr, data=data, auth=auth)
    return res


def ji_test():
    """test function.
    """
    print("test it is")

    res = req(verb="GET", route="/rest/api/3/myself")
    x = res.json()
    PP(x)
    sys.exit(0)


def project_key():
    if os.path.isfile(".key"):
        with open(".key", "r") as f:
            return f.read().split("\n")[0].strip()
    return os.getcwd().split(os.sep)[-1]

def ji_dev():
    """test dev function.
    """
    proj = project_key()
    last_int_hours = 48
    res = req(verb="GET", route="/rest/api/3/search?maxResults=250&jql=" + urllib.parse.quote('created >= -%dh and project = %s' % (last_int_hours, proj)))
    x = res.json()
    PP(x)

    sys.exit(0)


def main():
    turbocore.cli_this(__name__, 'ji_')
    return
