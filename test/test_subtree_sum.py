import unittest

from link_cut_tree import build_link_cut_tree, Node


class SubtreeSumNode(Node):
	def __init__(self, name, value):
		self.name = name
		self.delta_sum = value
		super().__init__(value)


	def display_str(self):
		return f'{self.name}: {self.delta_sum}'


	def _rotate_up(self):
		p = self.parent
		c = self.children[1 - self.child_index()]

		if c:
			c.delta_sum += self.delta_sum

		self.delta_sum, p.delta_sum = self.delta_sum + p.delta_sum, -self.delta_sum

		super()._rotate_up()


	def _lc_replace_right_subtree(self, new_right_child):
		if self.right:
			self.right.delta_sum += self.delta_sum

		if new_right_child:
			new_right_child.delta_sum -= self.delta_sum

		super()._lc_replace_right_subtree(new_right_child)


	def lc_link(self, v):
		super().lc_link(v)

		v.delta_sum += self.delta_sum


	def get_sum(self):
		self.lc_expose()
		return self.delta_sum


	def set_value(self, value):
		self.lc_expose()
		delta = value - self.value
		self.delta_sum += delta
		self.value = value


class TestSubtreeSum(unittest.TestCase):
	def test_subtree_sum(self):
		nodes = {}
		for i, c in enumerate('ABCDEFG'):
			nodes[c] = SubtreeSumNode(c, 1 << i)

		build_link_cut_tree(\
			(nodes['A'], [
				(nodes['B'], [
					(nodes['D'], []),
					(nodes['E'], []),
				]),
				(nodes['C'], [
					(nodes['F'], []),
					(nodes['G'], []),
				]),
			]))

		sums = {
			'A': (1 << 7) - 1,
			'B': 0b11010,
			'C': 0b1100100,
			'D': 1 << 3,
			'E': 1 << 4,
			'F': 1 << 5,
			'G': 1 << 6,
		}

		for name, node in nodes.items():
			self.assertEqual(node.get_sum(), sums[name])

		nodes['C'].lc_cut()
		diffs = {
			'A': -sums['C'],
		}
		for name, node in nodes.items():
			self.assertEqual(node.get_sum(), sums[name] + diffs.get(name, 0), f'{name}')

		nodes['C'].lc_link(nodes['E'])
		diffs = {
			'B': sums['C'],
			'E': sums['C'],
		}
		for name, node in nodes.items():
			self.assertEqual(node.get_sum(), sums[name] + diffs.get(name, 0), f'{name}')

		nodes['C'].set_value(nodes['C'].value + (1 << 8))
		diffs = {
			'A': 1 << 8,
			'B': sums['C'] + (1 << 8),
			'E': sums['C'] + (1 << 8),
			'C': 1 << 8,
		}
		for name, node in nodes.items():
			self.assertEqual(node.get_sum(), sums[name] + diffs.get(name, 0), f'{name}')


if __name__ == '__main__':
	unittest.main()
