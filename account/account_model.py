class Account:
    def __init__(self, name='', username='', password='', email='', phone='', role=''):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.role = role

    def visibale(self):
        return{
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'phone': self.phone,
            'role': self.role
        }
