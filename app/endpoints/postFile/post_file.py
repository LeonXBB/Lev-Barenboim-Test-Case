import os

from app.db.db import File #please, don't look at the names
from app.utils.env import get_env
from app.utils.location import get_file_location

async def post_file(file):
    
    '''
    The function to handle the saving of the received file into the storage as well as the database. 
    Has one argument, file: FastAPI.UploadFile 
    '''

    config = get_env("app", False)               

    def get_max_filename_length():
        try:
            return int(config("MAX_FILENAME_LENGTH"))
        except:
            raise TypeError("config arg not declared or not an int")

    def run_checks():
        
        def file_corrupted():
            return not file
        
        def no_storage_write_permit():
            return not os.access("/storage", os.W_OK)

        def filename_too_long():
            return len(file.filename) > get_max_filename_length()

        if file_corrupted():
            return 422

        if no_storage_write_permit():
            return 403

        if filename_too_long():
            return 413

        return 201

    async def save_file_to_db():
        new_file = File(original_namestring=file.filename, headers=str(file.headers))
        await new_file.save()
        return new_file

    def save_file_to_storage():
        with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())            
       
    def get_file_id():
        return new_file.id
   
    if (res := run_checks()) == 201:
        
        new_file = await save_file_to_db()

        file_id = get_file_id()
        file_location = get_file_location(file_id, True)

        save_file_to_storage()

    return res
    