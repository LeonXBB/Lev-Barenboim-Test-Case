from app.utils.env import get_env
from app.utils.hash import get_hash

async def authorization_check(request):

    '''
    The function to check whether the user has the authorization to send a request to the server. 
    Has one argument, request: FastAPI.Request
    '''

    config = get_env("app", False)
    secret_config = get_env("app", True)

    def ignore_urls():
        try:
            return eval(secret_config("IGNORE_URLS"))
        except:
            raise TypeError("config arg not declared or not a tuple")

    def authorization_check_flag():
        try: # same as config("AUTHORIZATION_CHECK_ON").isnumeric()
            return int(config("AUTHORIZATION_CHECK_ON"))
        except:
            raise TypeError("config arg not declared or not an int")

    if not authorization_check_flag() or any(request.url._url.count(string) for string in ignore_urls()):
        return True
    
    else:        
        form_data = await request.form()
        return "auth_token" in form_data and form_data["auth_token"] == get_hash(secret_config("REQUESTS_TOKEN"))