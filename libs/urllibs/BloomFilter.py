# !/usr/bin/env python
# -*- coding:utf-8 -*-

import mmh3

from bitarray import bitarray
from random import randint


class BloomFilter(object):

    def __init__(self, size, hash_count=10):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        self.seed = randint(23, 97)

    def add(self, string):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(string, self.seed) % self.size
            self.bit_array[result] = 1

    def find(self, string):
        for seed in xrange(self.hash_count):
            result = mmh3.hash(string, self.seed) % self.size
            if self.bit_array[result] == 0:
                return False
        return True

