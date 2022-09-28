import os
import platform

from app.utils.location import get_file_location

from ...db.models.File import File

async def get_file_headers(file_id: int):
    '''
    The function to handle the retrieving of a file attrs. 
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

    def get_file_size():
        return str(os.path.getsize(file_location))

    def get_file_create_date():
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
                
        if platform.system() == 'Windows':
            return str(int(os.path.getctime(file_location)))
        else:
            stat = os.stat(file_location)
            try:
                return str(int(stat.st_birthtime))
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return str(int(stat.st_mtime)) 

    if (res := await run_checks()) == 200:              
        file_location = get_file_location(file_id)
        
        res = (get_file_size(), get_file_create_date())

    return res