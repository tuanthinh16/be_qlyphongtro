class DataModel:
    def __init__(self,id='',detail='',username='',count=''):
        self.id = id
        self.detail = detail
        self.username = username
        self.count = count
    def visibale(self):
        return{
            'id':self.id,
            'detail':self.detail,
            'username':self.username,
            'count':self.count
        }