import unittest

from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_cache(self):
        cache = LRUCache()
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        cache.set('d', 4)

        cache.set('a', 'a')
        x = cache.get('c')
        list_ = []
        for k, v in cache:
            list_.append(f'{k}{v}')

        self.assertListEqual(['c3', 'aa', 'd4', 'b2'], list_)

    def test_case_2(self):
        cache = LRUCache()
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)
        cache.set('d', 4)

        cache.delete('d')
        list_ = []
        for k, v in cache:
            list_.append(f'{k}{v}')

        self.assertListEqual(['c3', 'b2', 'a1'], list_)

    def test_case_3(self):
        cache = LRUCache()
        cache.delete('a')


if __name__ == '__main__':
    unittest.main()
