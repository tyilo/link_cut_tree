import enum


class Traversal(enum.Enum):
	in_order = enum.auto()
	pre_order = enum.auto()
	post_order = enum.auto()


class Node:
	def __init__(self, value=None, left=None, right=None):
		self.parent = None
		self.children = [None, None]
		self.value = value
		self.path_parent = None

		self.reversed = False

		self.left = left
		self.right = right

		self.augmentation = None
		self.update_augmentation()

	def _push_reversed(self):
		if self.parent:
			self.parent._push_reversed()

		if self.reversed:
			self.children = self.children[::-1]
			for c in self.children:
				if c:
					c.reversed = not c.reversed

			self.reversed = False


	def __str__(self):
		return f'<{type(self).__name__}: {self.value}>'


	def update_augmentation(self):
		pass


	def set_child(self, i, o):
		self.children[i] = o
		if o:
			o.parent = self

		self.update_augmentation()


	def child_index(self):
		return self.parent.children.index(self)


	@property
	def left(self):
		return self.children[0]


	@left.setter
	def left(self, o):
		self.set_child(0, o)


	@property
	def right(self):
		return self.children[1]


	@right.setter
	def right(self, o):
		self.set_child(1, o)


	def traverse_subtree(self, order=Traversal.in_order, reverse=False):
		if order == Traversal.pre_order:
			yield self

		for i in range(2):
			if i == 1 and order == Traversal.in_order:
				yield self

			c = self.children[i ^ self.reversed ^ reverse]
			if c:
				yield from c.traverse_subtree(order, reverse ^ self.reversed)

		if order == Traversal.post_order:
			yield self


	def display_str(self):
		return str(self.value)


	def _node_style(self):
		color = 'red' if self.reversed else 'white'
		return f'  {id(self)} [label="{self.display_str()}",style=filled,fillcolor="{color}"];'


	def print_subtree(self, file=None):
		empty = 0

		print('digraph splay {', file=file)
		for node in self.traverse_subtree():
			print(node._node_style(), file=file)

			for c in node.children:
				if c:
					print(f'  {id(node)} -> {id(c)};', file=file)
				else:
					print(f'  {id(node)} -> empty{empty};', file=file)
					print(f'  empty{empty} [shape=point];', file=file)
					empty += 1

		print('}', file=file)


	def get_splay_root(self):
		r = self
		while r.parent:
			r = r.parent

		return r


	def print_tree(self, file=None):
		self.get_splay_root().print_subtree(file)


	def _rotate_up(self):
		i = self.child_index()
		p = self.parent
		g = p.parent

		self.parent = g
		if g:
			j = p.child_index()
			g.children[j] = self
		else:
			self.path_parent = p.path_parent
			p.path_parent = None

		p.set_child(i, self.children[1 - i])
		self.set_child(1 - i, p)


	def splay(self):
		self._push_reversed()
		while self.parent:
			i = self.child_index()
			p = self.parent

			if not p.parent:
				# zig
				self._rotate_up()
			else:
				j = p.child_index()
				if i == j:
					# zig-zig
					p._rotate_up()
					self._rotate_up()
				else:
					# zig-zag
					self._rotate_up()
					self._rotate_up()


	def get_extreme(self, largest):
		r = self.get_splay_root()
		while r.children[largest]:
			r = r.children[largest]

		return r


	def get_smallest(self):
		return self.get_extreme(False)


	def get_largest(self):
		return self.get_extreme(True)


	def _lc_cut_off_right_subtree(self):
		'''
		Cuts off the right subtree of `self` in the auxiliary tree
		and puts it into its own auxiliary tree.
		'''

		if self.right:
			self.right.path_parent = self
			self.right.parent = None
			self.right = None

			self.update_augmentation()


	def lc_access(self):
		'''
		Makes `self` root of its auxiliary tree `T` and `T` the root of the tree of augmented trees.
		`T` will be a binary search tree
		containining the nodes on the path from `self` to the root of the represented tree.
		The (implicit) key is the depth of the nodes in the represented tree.
		This implies that `self` will have no right child in `T`.
		'''

		self.splay()
		self._lc_cut_off_right_subtree()

		while self.path_parent:
			w = self.path_parent
			w.splay()
			w._lc_cut_off_right_subtree()

			w.right = self
			self.parent = w
			self.path_parent = None

			w.update_augmentation()

			self.splay()


	def lc_get_root(self):
		'''
		Returns the root of the represented tree.
		'''

		self.lc_access()
		r = self.get_smallest()
		r.splay()
		return r


	def lc_cut(self):
		'''
		Cuts the a node away from its parent in the represented tree.

		Preconditions:
			`self` is not the root of the represented tree.

		Returns:
			`self`, which is the root of one of the new represented trees.
			`left`, which is a node in the other represented tree.
		'''

		self.lc_access()

		l = self.left
		assert l != None, "Can't cut the root of the represented tree"

		l.parent = None
		self.left = None

		self.update_augmentation()

		return (self, l)


	def lc_link(self, v):
		'''
		Links the two represented trees `self` and `v`, by making `v` a child of `self`.

		Preconditions:
			`self` and `v` are not in the same represented tree.
			`self` is the root of its represented tree.
		'''

		self.lc_access()
		assert self.left == None, "self is not the root of the represented tree"

		v.lc_access()

		assert self.parent == None and self.path_parent == None, "Can't link two nodes in the same represented tree"

		self.left = v

		v.update_augmentation()


	def lc_path_aggregate(self):
		self.lc_access()
		return self.augmentation


	def lc_evert(self):
		'''
		Reverse the edges from `self` to the root of the represented tree.
		This makes `self` the new root of the represented tree.
		'''

		self.lc_access()
		self.reversed = True


class LinkCutForest:
	def __init__(self, nodes):
		self.nodes = nodes


	def print_represented_forest(self, file=None):
		print('digraph link_cut {', file=file)
		for node in self.nodes:
			print(node._node_style(), file=file)

			if node.parent:
				continue

			prev = None
			for p in node.traverse_subtree(Traversal.in_order):
				if prev:
					print(f'  {id(prev)} -> {id(p)};', file=file)

				prev = p

			if node.path_parent:
				print(f'  {id(node.path_parent)} -> {id(node)};', file=file)

		print('}', file=file)


	def print_aux_trees(self, file=None):
		empty = 0

		print('digraph link_cut {', file=file)
		for node in self.nodes:
			print(node._node_style(), file=file)

			for c in node.children:
				if c:
					print(f'  {id(node)} -> {id(c)};', file=file)
				else:
					print(f'  {id(node)} -> empty{empty};', file=file)
					print(f'  empty{empty} [shape=point];', file=file)
					empty += 1

			if node.path_parent:
				print(f'  {id(node.path_parent)} -> {id(node)} [style=dashed, dir=back];', file=file)

		print('}', file=file)


def build_link_cut_tree(structure, forest=None):
	if not forest:
		forest = LinkCutForest([])

	node, children = structure
	forest.nodes.append(node)

	for c, c_children in children:
		c.lc_link(node)
		build_link_cut_tree((c, c_children), forest)

	return forest
