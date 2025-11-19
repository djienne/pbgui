import json
import pprint

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except (ValueError,TypeError) as err:
        return False
    return True

def config_pretty_str(config: dict):
    pretty_str = pprint.pformat(config)
    for r in [("'", '"'), ("True", "true"), ("False", "false")]:
        pretty_str = pretty_str.replace(*r)
    return pretty_str
