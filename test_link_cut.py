import unittest

from link_cut_tree import build_link_cut_tree, Node


class PathSumNode(Node):
	def __init__(self, name, value):
		super().__init__(value)
		self.name = name

	def display_str(self):
		return f'{self.name}: {self.value}'

	def update_augmentation(self):
		self.augmentation = self.value
		for c in self.children:
			if c:
				self.augmentation += c.augmentation


class TestPathSum(unittest.TestCase):
	def test_path_sum(self):
		root = PathSumNode('root', 1 << 0)
		c1 = PathSumNode('c1', 1 << 1)
		c2 = PathSumNode('c2', 1 << 2)
		c3 = PathSumNode('c3', 1 << 6)

		c1_1 = PathSumNode('c1_1', 1 << 3)

		c2_1 = PathSumNode('c2_1', 1 << 4)
		c2_2 = PathSumNode('c2_2', 1 << 5)

		c2_2_1 = PathSumNode('c2_2_1', 1 << 6)

		build_link_cut_tree(
			(root, [
				(c1, [
					(c1_1, []),
				]),
				(c2, [
					(c2_1, []),
					(c2_2, [
						(c2_2_1, []),
					]),
				]),
				(c3, []),
			]))


		self.assertEqual(root.lc_path_aggregate(), root.value)
		self.assertEqual(c1.lc_path_aggregate(), root.value + c1.value)
		self.assertEqual(c2.lc_path_aggregate(), root.value + c2.value)
		self.assertEqual(c3.lc_path_aggregate(), root.value + c3.value)

		self.assertEqual(c1_1.lc_path_aggregate(), root.value + c1.value + c1_1.value)
		self.assertEqual(c2_1.lc_path_aggregate(), root.value + c2.value + c2_1.value)
		self.assertEqual(c2_2.lc_path_aggregate(), root.value + c2.value + c2_2.value)
		self.assertEqual(c2_2_1.lc_path_aggregate(), root.value + c2.value + c2_2.value + c2_2_1.value)

		self.assertEqual(c2_2.lc_get_root(), root)

		c2_2.lc_cut()
		self.assertEqual(c2_2_1.lc_path_aggregate(), c2_2.value + c2_2_1.value)
		self.assertEqual(c2_2.lc_path_aggregate(), c2_2.value)
		self.assertEqual(c2_2_1.lc_get_root(), c2_2)

		root.lc_link(c2_2)
		self.assertEqual(root.lc_path_aggregate(), c2_2.value + root.value)
		self.assertEqual(c3.lc_path_aggregate(), c2_2.value + root.value + c3.value)
		self.assertEqual(c1_1.lc_path_aggregate(), c2_2.value + root.value + c1.value + c1_1.value)
		self.assertEqual(root.lc_get_root(), c2_2)
		self.assertEqual(c1_1.lc_get_root(), c2_2)


class TestEvert(unittest.TestCase):
	def test_evert(self):
		nodes = {}
		for c in map(chr, range(ord('a'), ord('l') + 1)):
			nodes[c] = PathSumNode(c, 1)

		build_link_cut_tree(
			(nodes['a'], [
				(nodes['b'], [
					(nodes['e'], [
						(nodes['h'], []),
					]),
					(nodes['f'], []),
				]),
				(nodes['c'], []),
				(nodes['d'], [
					(nodes['g'], [
						(nodes['i'], []),
						(nodes['j'], [
							(nodes['l'], []),
						]),
						(nodes['k'], []),
					]),
				]),
			]))

		nodes['j'].lc_evert()

		self.assertEqual(nodes['l'].lc_path_aggregate(), 2)
		self.assertEqual(nodes['h'].lc_path_aggregate(), 7)


if __name__ == '__main__':
	unittest.main()
