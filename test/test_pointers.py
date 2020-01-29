import unittest

from link_cut_tree import build_link_cut_tree, Node


class PointerNode(Node):
	def __init__(self, value):
		self.lc_parent = None
		self.lc_children = set()
		super().__init__(value)

	def lc_link(self, v):
		super().lc_link(v)

		assert self.lc_parent == None
		assert self not in v.lc_children

		self.lc_parent = v
		v.lc_children.add(self)

	def lc_cut(self):
		prev_parent = super().lc_cut()

		assert self.lc_parent == prev_parent
		assert self in prev_parent.lc_children

		self.lc_parent = None
		prev_parent.lc_children.remove(self)

		return prev_parent


class TestPointers(unittest.TestCase):
	def test_pointers(self):
		nodes = {}
		for c in 'ABCDEFG':
			nodes[c] = PointerNode(c)

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

		assert nodes['A'].lc_parent == None

		assert nodes['A'].lc_children == {nodes['B'], nodes['C']}
		assert nodes['B'].lc_parent == nodes['A']
		assert nodes['C'].lc_parent == nodes['A']

		assert nodes['B'].lc_children == {nodes['D'], nodes['E']}
		assert nodes['D'].lc_parent == nodes['B']
		assert nodes['E'].lc_parent == nodes['B']

		assert nodes['C'].lc_children == {nodes['F'], nodes['G']}
		assert nodes['F'].lc_parent == nodes['C']
		assert nodes['G'].lc_parent == nodes['C']

		assert nodes['D'].lc_children == set()
		assert nodes['E'].lc_children == set()
		assert nodes['F'].lc_children == set()
		assert nodes['G'].lc_children == set()


if __name__ == '__main__':
	unittest.main()
