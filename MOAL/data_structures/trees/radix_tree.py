# -*- coding: utf-8 -*-

__author__ = """Chris Tabor (dxdstudio@gmail.com)"""

if __name__ == '__main__':
    from os import getcwd
    from os import sys
    sys.path.append(getcwd())

from MOAL.helpers.display import Section
from MOAL.data_structures.trees.trie import NaiveTrie


DEBUG = True if __name__ == '__main__' else False


class NaiveRadixTree(NaiveTrie):

    def _get_offset(self, string):
        """Calculate the offset of self value and a string.
        e.g. pot / potato = ato, position = 3 (used like [3:])"""
        if string == '':
            return 0
        chars = list(string)
        for k, char in enumerate(chars):
            if string[k] != chars[k]:
                return k
        return len(string)

    def add(self, string):
        """Add a node to this path, or augment it by updating the substring."""
        # Add initial starting node if empty.
        if len(self.path) == 0:
            self.path[string] = NaiveRadixTree()
            self.is_terminal = True
            return
        for substr, node in self.path.iteritems():
            if string.startswith(substr):
                offset = node._get_offset(substr)
                node.add(string[offset:])
                node.path[string[offset:]] = NaiveRadixTree()

    def view(self, indent=0, divider=None):
        if self.path is None:
            return
        for substr, node in self.path.iteritems():
            spacer = '{}'.format(indent * '') if indent > 0 else ''
            print('{}{}{} - *'.format(indent * '  ', spacer, substr))
            node.view(indent=indent + 1)
        if divider is not None:
            print(divider * 80)


if DEBUG:
    with Section('Naive Trie structure - basic'):
        ntrie = NaiveRadixTree()
        words = [
            'ad', 'add', 'addition', 'additional', 'additive', 'additives',
            'adder', 'address', 'addressee', 'addressing', 'addendum']
        for word in words:
            ntrie.add(word)
            ntrie.view(divider='-')
