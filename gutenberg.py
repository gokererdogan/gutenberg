"""A thin gutenberg catalog class that offers simple metadata retrieval and filtering.

You need the pickled Gutenberg catalog file (gutenberg.pkl) to use this class.
If you don't have this, you can create it from the official Gutenberg catalog using the script
parse_gutenberg_catalog.py.

Goker Erdogan
28 March 2021
"""
from typing import Dict, List

import pickle


class GutenbergCatalog:

    def __init__(self, path: str):
        with open(path, 'rb') as f:
            self._catalog = pickle.load(f)
        self._id_to_book = {}
        for book in self._catalog:
            self._id_to_book[book['id']] = book

    def get_metadata(self, book_id: int) -> Dict[str, List[str]]:
        assert str(book_id) in self._id_to_book, 'Cannot find book.'
        return self._id_to_book[str(book_id)]

    def filter_by(self, by: str, search_term: str) -> List[int]:
        cols = self._catalog[0].keys()
        assert by in cols, f'Unknown filter property, available ones are {cols}'
        return [int(b['id']) for b in self._catalog if search_term in b[by]]
