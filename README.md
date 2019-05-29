# link_cut_tree

A link/cut tree implemented in python.

All link/cut tree operations on a node are prefixed with `lc_`.
Other methods are splay tree operations on the auxiliary tree.

Supports the following operations in `O(log n)` amortized time, where `v` and `w` are nodes:

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

## Advanced augmentation

Instead of just overriding `update_augmentation`, you can also override `_rotate_up`, `_lc_replace_right_subtree` and `lc_link` to support some more advanced forms of augmentation.

In `test/test_subtree_sum.py` is an example of a link/cut tree, where each node is augmented with the sum of its subtree's values in the represented tree. Note that this is vastly different from just a simple path aggregation.

The nodes supports the following operations in `O(log n)` amortized time:

- `v.get_sum()`: Returns the subtree sum for `v`.
- `v.set_value(value)`: Sets the value of `v` to `value`. (Subtree sums will be updated).
