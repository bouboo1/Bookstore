import os
import sqlite3 as sqlite
import random
import base64
from pymongo import MongoClient
import simplejson as json


class Book:
    id: str
    title: str
    author: str
    publisher: str
    original_title: str
    translator: str
    pub_year: str
    pages: int
    price: int
    binding: str
    isbn: str
    author_intro: str
    book_intro: str
    content: str
    tags: [str]
    pictures: [bytes]

    def __init__(self):
        self.tags = []
        self.pictures = []


class BookDB:
    def __init__(self, large: bool = False):
        parent_path = os.path.dirname(os.path.dirname(__file__))
        #self.db_s = os.path.join(parent_path, "data/bookname.db")
        #self.db_l = os.path.join(parent_path, "data/book_lx.db")
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['bookstore']
        #self.book_db = self.db_l
        #if large:
            #self.book_db = self.db_l
        #else:
            #self.book_db = self.db_s

    def get_book_count(self):
        #conn = sqlite.connect(self.book_db)
        count = self.db.books.count_documents({})
        #cursor = conn.execute("SELECT count(id) FROM book")
        #row = cursor.fetchone()
        return count

    def get_book_info(self, start, size) -> [Book]:
        books = []
        #conn = sqlite.connect(self.book_db)
        result = self.db.books.find().sort([("id", 1)]).skip(size).limit(size)
        #cursor = conn.execute(
        #    "SELECT id, title, author, "
        #    "publisher, original_title, "
        #    "translator, pub_year, pages, "
        #    "price, currency_unit, binding, "
        #    "isbn, author_intro, book_intro, "
        #    "content, tags, picture FROM book ORDER BY id "
        #    "LIMIT ? OFFSET ?",
        #    (size, start),
        #)
        for row in result:
            book = Book()
            book.id = row['id']
            book.title = row['title']
            book.author = row['author']
            book.publisher = row['publisher']
            book.original_title = row['original_title']
            book.translator = row['translator']
            book.pub_year = row['pub_year']
            book.pages = row['pages']
            book.price = row['price']

            #book.currency_unit = row[9]
            book.binding = row['binding']
            book.isbn = row['isbn']
            book.author_intro = row['author_intro']
            book.book_intro = row['book_intro']
            book.content = row['content']
            tags = row['tags']

            picture = row['picture']

            for tag in tags:#for tag in tags.split("\n"):
                if tag.strip() != "":
                    book.tags.append(tag)
            for i in range(0, random.randint(0, 9)):
                if len(picture) > 0:
                    picture = picture[0].encode()
                    encode_str = base64.b64encode(picture).decode("utf-8")
                    book.pictures.append(encode_str)
            books.append(book)
            # print(tags.decode('utf-8'))

            # print(book.tags, len(book.picture))
            # print(book)
            # print(tags)

        return books

