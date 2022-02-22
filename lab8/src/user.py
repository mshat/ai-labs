from typing import List


class User:
    likes: List[str]
    dislikes: List[str]

    def __init__(self, name: str = None):
        self.name = name
        self.likes = []
        self.dislikes = []

    def add_like(self, artist_name: str):
        if artist_name in self.dislikes:
            self.dislikes.remove(artist_name)
        else:
            if artist_name not in self.likes:
                self.likes.append(artist_name)

    def add_dislike(self, artist_name: str):
        if artist_name in self.likes:
            self.likes.remove(artist_name)
        else:
            if artist_name not in self.dislikes:
                self.dislikes.append(artist_name)

    def __str__(self):
        return f'User {self.name} likes: {self.likes}, dislikes: {self.dislikes}'