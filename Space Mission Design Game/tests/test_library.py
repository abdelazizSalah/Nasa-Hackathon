"""Library-only content, navigation data, persistence and reference safety checks."""
import json
from pathlib import Path
import tempfile
import unittest
from game.library.content import (DATA, load_library, paginate, table_pages, search,
                                  safe_url, ReferenceOpener, ReadingPosition)

class LibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.books,cls.refs=load_library()

    def test_complete_substantial_collection(self):
        self.assertEqual(len(self.books),12)
        self.assertEqual(len({b['id'] for b in self.books}),12)
        for book in self.books:
            self.assertGreaterEqual(len(book['chapters']),3)
            self.assertEqual(len(book['questions']),3)
            self.assertTrue((DATA/'assets'/f'cover-{book["id"]}.png').is_file())
            for c in book['chapters']:
                words=' '.join(p for s in c['sections'] for p in s['paragraphs']).split()
                self.assertGreaterEqual(len(words),200,c['title'])
                self.assertTrue(c['refs'])
                self.assertTrue(all(safe_url(self.refs[r]['url']) for r in c['refs']))
                self.assertTrue((DATA/'assets'/f'{c["diagram"]}.png').is_file())

    def test_all_text_fits_bounded_pages(self):
        for b in self.books:
            for c in b['chapters']:
                for p in paginate(c)+table_pages(c):
                    self.assertLessEqual(len(p.splitlines()),20)
                    self.assertTrue(all(len(line)<=53 for line in p.splitlines()),c['title'])

    def test_search_and_comparison_coverage(self):
        for term in ('vegetation','aluminum','electric propulsion','thermal expansion','hydrazine'):
            self.assertTrue(search(self.books,term),term)
        self.assertFalse(search(self.books,''))
        for b in self.books:
            for c in b['chapters']:
                table=' '.join(table_pages(c)).replace('\n',' ')
                for row in c['table'][1:]:
                    self.assertIn(row[0],table)

    def test_reading_position_is_separate_and_robust(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'reading.json';p.write_text('broken')
            position=ReadingPosition(p);self.assertEqual(position.get('power'),(0,0))
            self.assertTrue(position.save('power',2,3))
            self.assertEqual(ReadingPosition(p).get('power'),(2,3))
            p.write_text(json.dumps({'schema_version':1,'positions':{'power':[-1,'bad']}}))
            self.assertEqual(ReadingPosition(p).get('power'),(0,0))

    def test_explicit_reference_actions_only(self):
        called=[];opener=ReferenceOpener(self.refs,lambda url,**kw:called.append(url))
        self.assertEqual(called,[])
        with self.assertRaises(ValueError):opener.open('not-a-source')
        opener.open('basics');opener.future.result(timeout=2)
        self.assertEqual(called,[self.refs['basics']['url']]);opener.close()
        for url in ('file:///x','javascript:alert(1)','https://nasa.gov.evil.com','http://nasa.gov','https://user@nasa.gov','https://nasa.gov:80','https://nasa.gov/\n'):
            self.assertFalse(safe_url(url),url)

if __name__=='__main__':unittest.main()
