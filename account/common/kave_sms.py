from kavenegar import *
from urllib.error import HTTPError


def send_sms_with_template(receptor, tokens: dict, template):
    """
        sending sms that needs template
    """
    try:
        api = KavenegarAPI('2B43447356785348764F4B386363657A5A67325838654336594B686C35304F2F4D507A33313363363877773D')

        params = {
            'receptor': receptor,
            'template': template,
        }

        for key, value in tokens.items():
            params[key] = value

        response = api.verify_lookup(params)
        print(response)
        return True
    except APIException as e:
        print(e)
        return False
    except HTTPError as e:
        print(e)
        return False


# ---------------------------------------
def send_sms_normal(receptor, message):
    try:
        api = KavenegarAPI('2B43447356785348764F4B386363657A5A67325838654336594B686C35304F2F4D507A33313363363877773D')

        params_buyer = {
            'receptor': receptor,
            'message': message,
            'sender': '10005000505077'
        }

        response = api.sms_send(params_buyer)
        print(response)
    except APIException as e:
        print(e)
    except HTTPError as e:
        print(e)
