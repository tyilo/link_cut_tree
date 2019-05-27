import unittest

from link_cut_tree import build_link_cut_tree, Node


class PathSumNode(Node):
	def update_augmentation(self):
		self.augmentation = self.value
		for c in self.children:
			if c:
				self.augmentation += c.augmentation


class TestPathSum(unittest.TestCase):
	def test_path_sum(self):
		root = PathSumNode(1 << 0)
		c1 = PathSumNode(1 << 1)
		c2 = PathSumNode(1 << 2)
		c3 = PathSumNode(1 << 6)

		c1_1 = PathSumNode(1 << 3)

		c2_1 = PathSumNode(1 << 4)
		c2_2 = PathSumNode(1 << 5)

		c2_2_1 = PathSumNode(1 << 6)

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


if __name__ == '__main__':
	unittest.main()
