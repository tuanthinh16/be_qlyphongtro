class Posts:
    def __init__(self, post_ID=0, title='', type='', dientich='', address='', detail='', username='',timeposted='',cost=''):
        self.post_ID = post_ID
        self.title = title
        self.type = type
        self.dientich = dientich
        self.address = address
        self.detail = detail
        self.username = username
        self.timeposted = timeposted
        self.cost = cost

    def visibale(self):
        return{
            'post_ID': self.post_ID,
            'title': self.title,
            'type': self.type,
            'dientich': self.dientich,
            'address': self.address,
            'detail': self.detail,
            'username': self.username,
            'timeposted': self.timeposted,
            'cost': self.cost,
        }
