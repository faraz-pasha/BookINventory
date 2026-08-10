class Book:

    def __init__(
        self,
        title,
        author,
        genre,
        rating,
        is_read,
        cover,
        notes
    ):

        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.is_read = is_read
        self.cover = cover
        self.notes = notes


    def to_dict(self):

        return {

            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "rating": self.rating,
            "is_read": self.is_read,
            "cover": self.cover,
            "notes": self.notes

        }