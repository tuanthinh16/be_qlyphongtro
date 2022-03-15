class ImagePost:
    def __init__(self, image_id=0, name_file='', post_id='', img=''):
        self.image_id = image_id
        self.name_file = name_file
        self.post_id = post_id
        self.img = img

    def visibale(self):
        return{
            'image_id': self.image_id,
            'name_file': self.name_file,
            'post_id': self.post_id,
            'img': self.img
        }
