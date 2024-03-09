from db.base_repository import BaseRepository
from db.models import Request



class RequestRepository(BaseRepository[Request]):
    pass

#requests = RequestRepository(Request)