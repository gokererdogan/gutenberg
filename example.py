"""An example script showcasing filtering and text retrieval.

11 April 2021
"""
from gutenberg import GutenbergCatalog
from gutenberg_text import get_text, strip_headers


def main():
    catalog = GutenbergCatalog('gutenberg.pkl')
    book_ids = catalog.filter_by('author', 'Russell, Bertrand')
    print(f'Found {len(book_ids)} books')

    book_id = 2529
    book_metadata = catalog.get_metadata(book_id)
    print('Title: ', book_metadata['title'])

    text = strip_headers(get_text(book_id))
    print('Part of text: ')
    print(text[1000:1100])


if __name__ == '__main__':
    main()
