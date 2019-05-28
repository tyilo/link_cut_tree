# link_cut_tree

A link/cut tree implemented in python.

All link/cut tree operations on a node are prefixed with `lc_`.
Other methods are splay tree operations on the auxiliary tree.

Supports the following operations in `O(log n)`, where `v` and `w` are nodes:

- `v.lc_get_root()`
- `v.lc_cut()`
- `v.lc_link(w)`
- `v.lc_path_aggregate()`
- `v.lc_evert()`
- `v.lc_lca(w)`

## Path aggregation

To support path aggregation extra information must be stored on the nodes.
This can be done by making a subclass of `Node` and overriding `update_augmentation`.

### Min example

To support querying the minimum value in a path, the following class can be used:

```python
class PathMinNode(Node):
	def update_augmentation(self):
		self.augmentation = self.value
		for c in self.children:
			if c:
				self.augmentation = min(self.augmentation, c)
```

Now `v.lc_path_aggregate()` can be used to query the minimum value on the path from `v` to the root in the represented tree.
