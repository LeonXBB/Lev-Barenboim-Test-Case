from decouple import Config, RepositoryEnv

def get_env(location: str, secret: bool) -> Config:
    '''
    Shortcut for getting correct .env files without the need to specify decouple framework each time.
    Takes two argument: 
    location: str, to specify folder name, and secret: whether to add the string "secret" before file extension 
    '''
    return Config(RepositoryEnv(f"{location}/{'secret' if secret else ''}.env"))