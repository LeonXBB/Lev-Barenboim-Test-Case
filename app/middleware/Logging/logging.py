import time

from ...db.db import Log
from ...utils.env import get_env

async def logging(request):

    '''
    The function to log any incoming request. Has one arg, request: FastAPI.Request.
    '''

    config = get_env("app", False)
               
    def logging_flag():
        try: # same as config("LOGGING_ON").isnumeric()
            return int(config("LOGGING_ON"))
        except:
            raise TypeError("config arg not declared or not an int")
        
    if logging_flag():

        def request_client_address():
            return f"{request.client.host}:{request.client.port}"

        def request_method():
            return str(request.method)

        def current_epoch():
            return int(time.time())

        #TODO write other params and add to the model

        async def make_new_log_entry():
            new_log_entry = Log(address=request_client_address(), method=request_method(), epoch=current_epoch())
            await new_log_entry.save()
        
        await make_new_log_entry()
        #TODO add funtionality to run logging after the request as well, to log the response
