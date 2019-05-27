import unittest
from itertools import zip_longest

from link_cut_tree import Node


'''
All of the following tests are from the paper introducing splay trees:1985
Self-Adjusting Binary Search Trees by Sleator & Tarjan, 1985
'''


def assert_same_node(unittest, n1, n2):
	if n1 and n2:
		unittest.assertEqual(n1.value, n2.value)
	else:
		unittest.assertEqual(n1, n2)


def assert_same_tree(unittest, t1, t2):
	r1 = t1.get_splay_root()
	r2 = t2.get_splay_root()
	for n1, n2 in zip_longest(r1.traverse_subtree(), r2.traverse_subtree()):
		assert_same_node(unittest, n1, n2)
		assert_same_node(unittest, n1.parent, n2.parent)
		assert_same_node(unittest, n1.left, n2.left)
		assert_same_node(unittest, n1.right, n2.right)


class TestSplayZig(unittest.TestCase):
	def setUp(self):
		self.zig1 = \
			Node('y',
				Node('x',
					Node('A'),
					Node('B'),
				),
				Node('C'),
			)

		self.zig2 = \
			Node('x',
				Node('A'),
				Node('y',
					Node('B'),
					Node('C'),
				),
			)


	def test_zig1(self):
		self.zig1.left.splay()
		assert_same_tree(self, self.zig1, self.zig2)


	def test_zig2(self):
		self.zig2.right.splay()
		assert_same_tree(self, self.zig1, self.zig2)


class TestSplayZigZig(unittest.TestCase):
	def setUp(self):
		self.zig_zig1 = \
			Node('z',
				Node('y',
					Node('x',
						Node('A'),
						Node('B'),
					),
					Node('C'),
				),
				Node('D'),
			)

		self.zig_zig2 = \
			Node('x',
				Node('A'),
				Node('y',
					Node('B'),
					Node('z',
						Node('C'),
						Node('D'),
					),
				),
			)


	def test_zig_zig1(self):
		self.zig_zig1.left.left.splay()
		assert_same_tree(self, self.zig_zig1, self.zig_zig2)


	def test_zig_zig2(self):
		self.zig_zig2.right.right.splay()
		assert_same_tree(self, self.zig_zig1, self.zig_zig2)


class TestSplayZigZag(unittest.TestCase):
	def test_zig_zag_left(self):
		zig_zag1 = \
			Node('z',
				Node('y',
					Node('A'),
					Node('x',
						Node('B'),
						Node('C'),
					),
				),
				Node('D'),
			)

		zig_zag2 = \
			Node('x',
				Node('y',
					Node('A'),
					Node('B'),
				),
				Node('z',
					Node('C'),
					Node('D'),
				)
			)

		zig_zag1.left.right.splay()
		assert_same_tree(self, zig_zag1, zig_zag2)


	def test_zig_zag_right(self):
		zig_zag1 = \
			Node('g',
				Node('A'),
				Node('p',
					Node('x',
						Node('B'),
						Node('C'),
					),
					Node('D')
				),
			)

		zig_zag2 = \
			Node('x',
				Node('g',
					Node('A'),
					Node('B'),
				),
				Node('p',
					Node('C'),
					Node('D'),
				)
			)

		zig_zag1.right.left.splay()
		assert_same_tree(self, zig_zag1, zig_zag2)


class TestSplayGeneral(unittest.TestCase):
	@staticmethod
	def find_node(t, val):
		for n in t.traverse_subtree():
			if n.value == val:
				return n


	def test_fig4(self):
		before = \
			Node('i',
				Node('h',
					Node('g',
						Node('f',
							Node('A'),
							Node('e',
								Node('d',
									Node('B'),
									Node('c',
										Node('C'),
										Node('b',
											Node('D'),
											Node('a',
												Node('E'),
												Node('F'),
											),
										),
									),
								),
								Node('G'),
							),
						),
						Node('H'),
					),
					Node('I'),
				),
			Node('J'),
		)

		after = \
			Node('a',
				Node('f',
					Node('A'),
					Node('d',
						Node('B'),
						Node('b',
							Node('c',
								Node('C'),
								Node('D'),
							),
							Node('E'),
						),
					),
				),
				Node('h',
					Node('g',
						Node('e',
							Node('F'),
							Node('G'),
						),
						Node('H'),
					),
					Node('i',
						Node('I'),
						Node('J'),
					),
				),
			)

		self.find_node(before, 'a').splay()
		assert_same_tree(self, before, after)


	def test_fig5a(self):
		before = \
			Node('g',
				Node('f',
					Node('e',
						Node('d',
							Node('c',
								Node('b',
									Node('a',
										Node('A'),
										Node('B'),
									),
									Node('C'),
								),
								Node('D'),
							),
							Node('E'),
						),
						Node('F'),
					),
					Node('G'),
				),
				Node('H'),
			)

		after = \
			Node('a',
				Node('A'),
				Node('f',
					Node('d',
						Node('b',
							Node('B'),
							Node('c',
								Node('C'),
								Node('D'),
							),
						),
						Node('e',
							Node('E'),
							Node('F'),
						),
					),
					Node('g',
						Node('G'),
						Node('H'),
					),
				),
			)

		self.find_node(before, 'a').splay()
		assert_same_tree(self, before, after)


	def test_fig5b(self):
		before = \
			Node('g',
				Node('f',
					Node('A'),
					Node('e',
						Node('d',
							Node('B'),
							Node('c',
								Node('b',
									Node('C'),
									Node('a',
										Node('D'),
										Node('E'),
									),
								),
								Node('F'),
							),
						),
						Node('G'),
					),
				),
				Node('H'),
			)

		after = \
			Node('a',
				Node('f',
					Node('A'),
					Node('d',
						Node('B'),
						Node('b',
							Node('C'),
							Node('D'),
						),
					),
				),
				Node('g',
					Node('e',
						Node('c',
							Node('E'),
							Node('F'),
						),
						Node('G'),
					),
					Node('H'),
				),
			)

		self.find_node(before, 'a').splay()
		assert_same_tree(self, before, after)


if __name__ == '__main__':
	unittest.main()
