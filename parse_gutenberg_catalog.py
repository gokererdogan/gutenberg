"""Creates the python pickle and json catalogs from Gutenberg catalog XML files.

You need to download the Gutenberg catalog and unzip/untar it to the following location.
  rdf_path = '~/gutenberg/rdf-files/cache/epub'
Gutenberg catalog can be downloaded from www.gutenberg.org.
  - http://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2

Goker Erdogan
5 April 2021
"""
import json
from lxml import etree
import os
import pickle


NAMESPACES = NS = {
    'cc': "http://web.resource.org/cc/",
    'dcam': "http://purl.org/dc/dcam/",
    'dcterms': "http://purl.org/dc/terms/",
    'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'pgterms': "http://www.gutenberg.org/2009/pgterms/"
}

FIELD_XPATHS = dict(
    title=['//dcterms:title/text()', '//dcterms:alternative/text()'],
    subject=['//dcterms:subject/rdf:Description/rdf:value/text()'],
    type=['//dcterms:type/rdf:Description/rdf:value/text()'],
    language=['//dcterms:language/rdf:Description/rdf:value/text()'],
    author=['//dcterms:creator/pgterms:agent/pgterms:alias/text()',
            '//dcterms:creator/pgterms:agent/pgterms:name/text()'],
    author_birth=['//dcterms:creator/pgterms:agent/pgterms:birthdate/text()'],
    author_death=['//dcterms:creator/pgterms:agent/pgterms:deathdate/text()'],
    bookshelf=['//pgterms:bookshelf/rdf:Description/rdf:value/text()'],
    format=['//dcterms:hasFormat/pgterms:file/dcterms:format/rdf:Description/rdf:value/text()'],
    publisher=['//dcterms:publisher/text()'],
    rights=['//dcterms:rights/text()'],
    date_issued=['//dcterms:issued/text()'],
    num_downloads=['//pgterms:downloads/text()']
)


def _get_field(field_name, doc):
    results = []
    for xpath in FIELD_XPATHS[field_name]:
        results.extend(doc.xpath(xpath, namespaces=NAMESPACES))
    return results


def parse_doc(doc):
    return {f: _get_field(f, doc) for f in FIELD_XPATHS.keys()}


def main():
    rdf_path = '~/gutenberg/rdf-files/cache/epub'
    report_freq = 500
    books = []
    for i, book_dir in enumerate(os.listdir(rdf_path)):
        if i % report_freq == 0:
            print(i)
        doc = etree.parse(f'{rdf_path}/{book_dir}/pg{book_dir}.rdf', etree.ETCompatXMLParser())
        parsed = parse_doc(doc)
        parsed['id'] = book_dir
        books.append(parsed)

    with open('gutenberg.pkl', 'wb') as f:
        pickle.dump(books, f)
    print('Saved books pickle file.')

    with open(f'gutenberg.json', 'w') as f:
        json.dump(books, f)
    print('Saved books json file.')


if __name__ == "__main__":
    main()