import unittest
import generator
from io import StringIO


class TestFunctions(unittest.TestCase):
    def test_number_generator(self):
        self.assertEqual(
            668,
            generator.number_generator("sydney")
        )


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.tree = generator.Trie()

    def test_insert(self):
        bike = self.tree.insert(
            "bike",
            generator.number_generator("bike"),
        )

        self.assertIsInstance(bike, generator.Leaf)
        self.assertEqual(True, bike.is_end)

        # b = 98
        # i = 105
        # k = 107
        # e = 101
        # bike = 411
        self.assertEqual(411, bike.value)

        self.assertEqual("k", bike.parent.key)
        self.assertDictEqual({"e": bike}, bike.parent.leafs)

    def test_get(self):
        sydney = self.tree.insert(
            "sydney",
            generator.number_generator("sydney"),
        )

        singapore = self.tree.insert(
            "singapore",
            generator.number_generator("singapore"),
        )

        self.assertEqual(singapore, self.tree.get("singapore"))
        self.assertRaises(IndexError, self.tree.get, "unknown")

    def test_contains(self):
        sydney = self.tree.insert(
            "sydney",
            generator.number_generator("sydney"),
        )

        self.assertEqual(True, self.tree.contains("sydney"))
        self.assertEqual(False, self.tree.contains("unknown"))

    def test_remove(self):
        sydney = self.tree.insert(
            "sydney",
            generator.number_generator("sydney"),
        )

        singapore = self.tree.insert(
            "singapore",
            generator.number_generator("singapore"),
        )

        self.assertEqual(True, self.tree.contains("singapore"))
        self.tree.remove("singapore")
        self.assertEqual(False, self.tree.contains("singapore"))
        self.assertRaises(IndexError, self.tree.remove, "unknown")


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inv = generator.Inventory()

    def test_add(self):
        self.inv.add("sydney")
        self.inv.add("singapore")
        self.assertEqual(True, self.inv.contains("sydney"))
        self.assertEqual(True, self.inv.contains("singapore"))
        self.assertEqual(False, self.inv.contains("unknown"))

    def test_remove(self):
        self.inv.add("sydney")
        self.inv.add("singapore")

        self.inv.remove("sydney")

        self.assertEqual(False, self.inv.contains("sydney"))
        self.assertEqual(True, self.inv.contains("singapore"))

    def test_find(self):
        self.inv.add("sydney")
        self.inv.add("singapore")

        data = self.inv.find("singapore")
        self.assertEqual(("singapore", 968), data)

    def test_next(self):
        self.inv.add("sydney")
        self.inv.add("singapore")

        self.assertEqual(sorted(["i", "y"]), sorted(self.inv.next("s")))

    def test_load(self):
        cities = [
            "adelaide",
            "beijing",
            "chicago",
            "cork",
            "dubai",
            "guangzhou",
            "jerusalem",
            "lisbon",
            "madrid",
            "mecca",
            "paris",
            "seoul",
            "shanghai",
            "shenzhen",
            "sydney",
            "tokyo",
            "york",
            "kualalumpur",
            "london",
            "naypyidaw",
            "ouaga",
        ]

        fh = StringIO()
        
        for each in cities:
            fh.write("{}\n".format(each))
        
        fh.seek(0)
        self.inv.load(fh)
        self.assertEqual(("cork", 431), self.inv.find("cork"))
