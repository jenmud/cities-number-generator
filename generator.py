"""
This is a very simple city name generator. It will load a file
of city names, generate a number for it, and allow your to find the city
and the number.
"""

def number_generator(name):
    """
    Number generator used for generating a unique number for a string.

    :param name: String that you are generating the number for.
    :type name: :class:`str`
    :returns: The gererated number for the provided name.
    :rtype: :class:`int`
    """
    num = 0
    for each in name:
        num += ord(each)
    return num


class Leaf(object):
    """
    Leaf is a leaf node in the Trie tree.

    :param parent: Parent leaf of for the this leaf.
    :type parent: :class:`~.Leaf`
    :param key: Is the index key for the leaf.
    :type key: :class:`str`
    :param value: Value assigned to the key.
    :type value: value
    """
    def __init__(self, parent=None, key=None, value=None):
        self.parent = parent
        self.key = key
        self.value = value
        self.is_end = False
        self.leafs = {}

    def __str__(self):  # pragma: no cover
        return "<{}> IsEnd: {}, Key: {}, Value: {}".format(
            self.__class__.__name__,
            self.is_end,
            self.key,
            self.value,
        )

    def __repr__(self):  # pragma: no cover
        return self.__str__()


class Trie(object):
    """
    Trie/prefix tree used for efficient storing and
    prefix string searching.
    """
    def __init__(self):
        self.root = Leaf(key=None)

    @staticmethod
    def _insert(leaf, key, value):
        if not key:
            leaf.is_end = True
            leaf.value = value
            return leaf

        head = key[0]
        tail = key[1:]

        _leaf = leaf.leafs.get(head)
        if _leaf is None:
            _leaf = Leaf(key=head, parent=leaf)
            leaf.leafs[head] = _leaf

        return Trie._insert(_leaf, tail, value)

    def insert(self, key, value):
        """
        Insert the key and value into the tree.

        :param key: Index key
        :type key: :class:`str`
        :param value: Value mapped to the index key
        :type value: value
        :returns: The end leaf.
        :rtype: :class:`~.Leaf`
        """
        return self._insert(self.root, key, value)

    @staticmethod
    def _remove(leaf, key):
        if not key and leaf.is_end:
            leaf.is_end = False
            leaf.value = None
            if len(leaf.leafs) != 0:
                del leaf.parent.leafs[key]
            return

        head = key[0]
        tail = key[1:]
        _leaf = leaf.leafs[head]

        return Trie._remove(_leaf, tail)

    def remove(self, key):
        """
        Remove the key from the tree.

        :param key: Index key to remove from the tree
        :type key: :class:`str`
        :raises IndexError: If the key does not exist in the tree.
        """
        if self.contains(key) is False:
            raise IndexError("key {!r} not found".format(key))
        self._remove(self.root, key)
        
    @staticmethod
    def _get(leaf, key):
        if not key:
            if leaf.is_end is True:
                return leaf
            raise IndexError("key {!r} not found".format(key))

        head = key[0]
        tail = key[1:]
        _leaf = leaf.leafs.get(head)

        if _leaf is None:
            raise IndexError("key {!r} not found".format(key))

        return Trie._get(_leaf, tail)
            
    def get(self, key):
        """
        Get the key's value from the tree.

        :param key: Key that you would like the value for.
        :type key: :class:`str` 
        :raises IndexError: If the key does not exist in the tree.
        :return: The value assigned to the key.
        :rtype: value 
        """
        return self._get(self.root, key)

    @staticmethod
    def _find(leaf, key):

        if not key:
            return leaf

        head = key[0]
        tail = key[1:]

        _leaf = leaf.leafs.get(head) 
        if leaf is None:
            raise IndexError("leaf {!r} not found".format(each))

        return Trie._find(_leaf, tail)

    def leafs(self, key):
        """
        Return all the known leafs hanging off of this leaf.

        :param key: Key that you would like leafs for.
        :type key: :class:`str`
        :returns: Iterable of key indexes.
        :rtype: :class:`str`
        """
        leaf = self._find(self.root, key)
        return [each.key for each in leaf.leafs.values()]

    def contains(self, key):
        """
        Checks if the key exists in the tree.

        :param key: Key that you are checking for.
        :type key: :class:`str`
        :returns: True if the key is found in the tree.
        :rtype: :class:`bool`
        """
        try:
            _ = self.get(key)
            return True
        except IndexError:
            return False


class Inventory(object):
    """
    Inventory for tracking city names and quering for cities.
    """
    def __init__(self):
        self.store = Trie()

    def load(self, fh):
        """
        Load a given file into the inventory.

        ..note::

            File should contains a city name on each line.

        :param fh: File handle that you are loading into the inventory.
        :type fh: :class:`file`
        """
        for each in fh:
            self.add(each.strip())

    def add(self, name):
        """
        Add a new name to the inventory.

        :param name: Name that you are added in to the inventory.
        :type name: :class:`str`
        """
        self.store.insert(name, number_generator(name))

    def remove(self, name):
        """
        Remove a name from the inventory.

        :param name: Name that you are removing.
        :type name: :class:`str`
        """
        try:
            self.store.remove(name)
        except IndexError:
            pass

    def contains(self, name):
        """
        Check if the name exists in the inventory.

        :param name: Name that you are check for.
        :type name: :class:`str`
        :returns: True is the name exists in the inventory.
        :rtype: :class:`bool`
        """
        return self.store.contains(name)

    def find(self, name):
        """
        Find the item in the inventory with the given name.

        :param name: Search the inventory for the name.
        :type name: :class:`str`
        :returns: Name and number.
        :rtype: :class:`tuple` of (:class:`str`, :class:`int`) or :obj:`None`.
        """
        try:
            num = self.store.get(name).value
            return (name, num)
        except IndexError:
            return

    def next(self, key):
        """
        Find the next available letters available.

        :param key: Key that you are searching.
        :type key: :class:`str`
        :returns: Iterable of abvailable options.
        :rtype: iterable of :class:`str`
        """
        return self.store.leafs(key)


if __name__ == "__main__":  # pragma: no cover
    import argparse
    import sys

    args = argparse.ArgumentParser(
        description="Return a generated number for a city name.",
    )

    args.add_argument(
        "-f",
        "--file",
        required=True,
        type=argparse.FileType(),
        metavar="FILENAME",
        help="Filename containing city names.",
    )

    args.add_argument(
        "city",
        metavar="CITY",
        help="City name.",
    )

    ns = args.parse_args()

    inv = Inventory()
    inv.load(ns.file)

    result = inv.find(ns.city)
    if result is None:
        print("Count not find {!r}".format(ns.city))
        sys.exit(2)
    print("City {!r} has a number {}".format(result[0], result[1]))
