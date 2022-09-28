import os

from app.utils.location import get_file_location

from ...db.models.File import File

async def get_file(file_id: int):
    
    '''
    The function to handle the retrieving of a file from the storage. 
    Has one argument, file_id: int 
    '''

    async def run_checks():

        async def file_does_not_exist():
            return (await File.objects.get_or_none(id=file_id) is None)

        def no_storage_read_permission():
            return not os.access("/storage", os.R_OK)

        if await file_does_not_exist():
            return 404 

        if no_storage_read_permission():
            return 403

        return 200

    async def get_file_obj():
        file_obj = await File.objects.get(id=file_id)
        return file_obj

    if (res := await run_checks()) == 200:
        file_obj = await get_file_obj()
        
        res = get_file_location(file_id), file_obj

    return res