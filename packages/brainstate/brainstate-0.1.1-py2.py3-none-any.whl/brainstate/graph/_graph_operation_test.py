# Copyright 2024 BDP Ecosystem Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import annotations

import unittest
from collections.abc import Callable
from threading import Thread

import jax
import jax.numpy as jnp
from absl.testing import absltest, parameterized

import brainstate as bst


class TestIter(unittest.TestCase):
    def test1(self):
        class Model(bst.nn.Module):
            def __init__(self):
                super().__init__()
                self.a = bst.nn.Linear(1, 2)
                self.b = bst.nn.Linear(2, 3)
                self.c = [bst.nn.Linear(3, 4), bst.nn.Linear(4, 5)]
                self.d = {'x': bst.nn.Linear(5, 6), 'y': bst.nn.Linear(6, 7)}
                self.b.a = bst.nn.LIF(2)

        for path, node in bst.graph.iter_leaf(Model()):
            print(path, node)
        for path, node in bst.graph.iter_node(Model()):
            print(path, node)
        for path, node in bst.graph.iter_node(Model(), allowed_hierarchy=(1, 1)):
            print(path, node)
        for path, node in bst.graph.iter_node(Model(), allowed_hierarchy=(2, 2)):
            print(path, node)

    def test_iter_leaf_v1(self):
        class Linear(bst.nn.Module):
            def __init__(self, din, dout):
                super().__init__()
                self.weight = bst.ParamState(bst.random.randn(din, dout))
                self.bias = bst.ParamState(bst.random.randn(dout))
                self.a = 1

        module = Linear(3, 4)
        graph = [module, module]

        num = 0
        for path, value in bst.graph.iter_leaf(graph):
            print(path, type(value).__name__)
            num += 1

        assert num == 3

    def test_iter_node_v1(self):
        class Model(bst.nn.Module):
            def __init__(self):
                super().__init__()
                self.a = bst.nn.Linear(1, 2)
                self.b = bst.nn.Linear(2, 3)
                self.c = [bst.nn.Linear(3, 4), bst.nn.Linear(4, 5)]
                self.d = {'x': bst.nn.Linear(5, 6), 'y': bst.nn.Linear(6, 7)}
                self.b.a = bst.nn.LIF(2)

        model = Model()

        num = 0
        for path, node in bst.graph.iter_node([model, model]):
            print(path, node.__class__.__name__)
            num += 1
        assert num == 8


class List(bst.nn.Module):
    def __init__(self, items):
        super().__init__()
        self.items = list(items)

    def __getitem__(self, idx):
        return self.items[idx]

    def __setitem__(self, idx, value):
        self.items[idx] = value


class Dict(bst.nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.items = dict(*args, **kwargs)

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        self.items[key] = value


class StatefulLinear(bst.nn.Module):
    def __init__(self, din, dout):
        super().__init__()
        self.w = bst.ParamState(bst.random.rand(din, dout))
        self.b = bst.ParamState(jnp.zeros((dout,)))
        self.count = bst.State(jnp.array(0, dtype=jnp.uint32))

    def increment(self):
        self.count.value += 1

    def __call__(self, x):
        self.count.value += 1
        return x @ self.w.value + self.b.value


class TestGraphUtils(absltest.TestCase):
    def test_flatten_treey_state(self):
        a = {'a': 1, 'b': bst.ParamState(2)}
        g = [a, 3, a, bst.ParamState(4)]

        refmap = bst.graph.RefMap()
        graphdef, states = bst.graph.flatten(g, ref_index=refmap, treefy_state=True)

        states[0]['b'].value = 2
        states[3].value = 4

        assert isinstance(states[0]['b'], bst.TreefyState)
        assert isinstance(states[3], bst.TreefyState)
        assert isinstance(states, bst.util.NestedDict)
        assert len(refmap) == 2
        assert a['b'] in refmap
        assert g[3] in refmap

    def test_flatten(self):
        a = {'a': 1, 'b': bst.ParamState(2)}
        g = [a, 3, a, bst.ParamState(4)]

        refmap = bst.graph.RefMap()
        graphdef, states = bst.graph.flatten(g, ref_index=refmap, treefy_state=False)

        states[0]['b'].value = 2
        states[3].value = 4

        assert isinstance(states[0]['b'], bst.State)
        assert isinstance(states[3], bst.State)
        assert len(refmap) == 2
        assert a['b'] in refmap
        assert g[3] in refmap

    def test_unflatten_treey_state(self):
        a = bst.graph.Dict(a=1, b=bst.ParamState(2))
        g1 = bst.graph.List([a, 3, a, bst.ParamState(4)])

        graphdef, references = bst.graph.flatten(g1, treefy_state=True)
        g = bst.graph.unflatten(graphdef, references)

        print(graphdef)
        print(references)
        assert g[0] is g[2]
        assert g1[3] is not g[3]
        assert g1[0]['b'] is not g[0]['b']

    def test_unflatten(self):
        a = bst.graph.Dict(a=1, b=bst.ParamState(2))
        g1 = bst.graph.List([a, 3, a, bst.ParamState(4)])

        graphdef, references = bst.graph.flatten(g1, treefy_state=False)
        g = bst.graph.unflatten(graphdef, references)

        print(graphdef)
        print(references)
        assert g[0] is g[2]
        assert g1[3] is g[3]
        assert g1[0]['b'] is g[0]['b']

    def test_unflatten_pytree(self):
        a = {'a': 1, 'b': bst.ParamState(2)}
        g = [a, 3, a, bst.ParamState(4)]

        graphdef, references = bst.graph.treefy_split(g)
        g = bst.graph.treefy_merge(graphdef, references)

        assert g[0] is not g[2]

    def test_unflatten_empty(self):
        a = Dict({'a': 1, 'b': bst.ParamState(2)})
        g = List([a, 3, a, bst.ParamState(4)])

        graphdef, references = bst.graph.treefy_split(g)

        with self.assertRaisesRegex(ValueError, 'Expected key'):
            bst.graph.unflatten(graphdef, bst.util.NestedDict({}))

    def test_module_list(self):
        ls = [
            bst.nn.Linear(2, 2),
            bst.nn.BatchNorm1d([10, 2]),
        ]
        graphdef, statetree = bst.graph.treefy_split(ls)

        assert statetree[0]['weight'].value['weight'].shape == (2, 2)
        assert statetree[0]['weight'].value['bias'].shape == (2,)
        assert statetree[1]['weight'].value['scale'].shape == (1, 2,)
        assert statetree[1]['weight'].value['bias'].shape == (1, 2,)
        assert statetree[1]['running_mean'].value.shape == (1, 2,)
        assert statetree[1]['running_var'].value.shape == (1, 2)

    def test_shared_variables(self):
        v = bst.ParamState(1)
        g = [v, v]

        graphdef, statetree = bst.graph.treefy_split(g)
        assert len(statetree.to_flat()) == 1

        g2 = bst.graph.treefy_merge(graphdef, statetree)
        assert g2[0] is g2[1]

    def test_tied_weights(self):
        class Foo(bst.nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.bar = bst.nn.Linear(2, 2)
                self.baz = bst.nn.Linear(2, 2)

                # tie the weights
                self.baz.weight = self.bar.weight

        node = Foo()
        graphdef, state = bst.graph.treefy_split(node)

        assert len(state.to_flat()) == 1

        node2 = bst.graph.treefy_merge(graphdef, state)

        assert node2.bar.weight is node2.baz.weight

    def test_tied_weights_example(self):
        class LinearTranspose(bst.nn.Module):
            def __init__(self, dout: int, din: int, ) -> None:
                super().__init__()
                self.kernel = bst.ParamState(bst.init.LecunNormal()((dout, din)))

            def __call__(self, x):
                return x @ self.kernel.value.T

        class Encoder(bst.nn.Module):
            def __init__(self, ) -> None:
                super().__init__()
                self.embed = bst.nn.Embedding(10, 2)
                self.linear_out = LinearTranspose(10, 2)

                # tie the weights
                self.linear_out.kernel = self.embed.weight

            def __call__(self, x):
                x = self.embed(x)
                return self.linear_out(x)

        model = Encoder()
        graphdef, state = bst.graph.treefy_split(model)

        assert len(state.to_flat()) == 1

        x = jax.random.randint(jax.random.key(0), (2,), 0, 10)
        y = model(x)

        assert y.shape == (2, 10)

    def test_state_variables_not_shared_with_graph(self):
        class Foo(bst.graph.Node):
            def __init__(self):
                self.a = bst.ParamState(1)

        m = Foo()
        graphdef, statetree = bst.graph.treefy_split(m)

        assert isinstance(m.a, bst.ParamState)
        assert issubclass(statetree.a.type, bst.ParamState)
        assert m.a is not statetree.a
        assert m.a.value == statetree.a.value

        m2 = bst.graph.treefy_merge(graphdef, statetree)

        assert isinstance(m2.a, bst.ParamState)
        assert issubclass(statetree.a.type, bst.ParamState)
        assert m2.a is not statetree.a
        assert m2.a.value == statetree.a.value

    def test_shared_state_variables_not_shared_with_graph(self):
        class Foo(bst.graph.Node):
            def __init__(self):
                p = bst.ParamState(1)
                self.a = p
                self.b = p

        m = Foo()
        graphdef, state = bst.graph.treefy_split(m)

        assert isinstance(m.a, bst.ParamState)
        assert isinstance(m.b, bst.ParamState)
        assert issubclass(state.a.type, bst.ParamState)
        assert 'b' not in state
        assert m.a is not state.a
        assert m.b is not state.a
        assert m.a.value == state.a.value
        assert m.b.value == state.a.value

        m2 = bst.graph.treefy_merge(graphdef, state)

        assert isinstance(m2.a, bst.ParamState)
        assert isinstance(m2.b, bst.ParamState)
        assert issubclass(state.a.type, bst.ParamState)
        assert m2.a is not state.a
        assert m2.b is not state.a
        assert m2.a.value == state.a.value
        assert m2.b.value == state.a.value
        assert m2.a is m2.b

    def test_pytree_node(self):
        @bst.util.dataclass
        class Tree:
            a: bst.ParamState
            b: str = bst.util.field(pytree_node=False)

        class Foo(bst.graph.Node):
            def __init__(self):
                self.tree = Tree(bst.ParamState(1), 'a')

        m = Foo()

        graphdef, state = bst.graph.treefy_split(m)

        assert 'tree' in state
        assert 'a' in state.tree
        assert graphdef.subgraphs['tree'].type.__name__ == 'PytreeType'

        m2 = bst.graph.treefy_merge(graphdef, state)

        assert isinstance(m2.tree, Tree)
        assert m2.tree.a.value == 1
        assert m2.tree.b == 'a'
        assert m2.tree.a is not m.tree.a
        assert m2.tree is not m.tree

    def test_call_jit_update(self):
        class Counter(bst.graph.Node):
            def __init__(self):
                self.count = bst.ParamState(jnp.zeros(()))

            def inc(self):
                self.count.value += 1
                return 1

        graph_state = bst.graph.treefy_split(Counter())

        @jax.jit
        def update(graph_state):
            out, graph_state = bst.graph.call(graph_state).inc()
            self.assertEqual(out, 1)
            return graph_state

        graph_state = update(graph_state)
        graph_state = update(graph_state)

        counter = bst.graph.treefy_merge(*graph_state)

        self.assertEqual(counter.count.value, 2)

    def test_stateful_linear(self):
        linear = StatefulLinear(3, 2)
        linear_state = bst.graph.treefy_split(linear)

        @jax.jit
        def forward(x, pure_linear):
            y, pure_linear = bst.graph.call(pure_linear)(x)
            return y, pure_linear

        x = jnp.ones((1, 3))
        y, linear_state = forward(x, linear_state)
        y, linear_state = forward(x, linear_state)

        self.assertEqual(linear.count.value, 0)
        new_linear = bst.graph.treefy_merge(*linear_state)
        self.assertEqual(new_linear.count.value, 2)

    def test_getitem(self):
        nodes = dict(
            a=StatefulLinear(3, 2),
            b=StatefulLinear(2, 1),
        )
        node_state = bst.graph.treefy_split(nodes)
        _, node_state = bst.graph.call(node_state)['b'].increment()

        nodes = bst.graph.treefy_merge(*node_state)

        self.assertEqual(nodes['a'].count.value, 0)
        self.assertEqual(nodes['b'].count.value, 1)


class SimpleModule(bst.nn.Module):
    pass


class SimplePyTreeModule(bst.nn.Module):
    pass


class TestThreading(parameterized.TestCase):

    @parameterized.parameters(
        (SimpleModule,),
        (SimplePyTreeModule,),
    )
    def test_threading(self, module_fn: Callable[[], bst.nn.Module]):
        x = module_fn()

        class MyThread(Thread):

            def run(self) -> None:
                bst.graph.treefy_split(x)

        thread = MyThread()
        thread.start()
        thread.join()


class TestGraphOperation(unittest.TestCase):
    def test1(self):
        class MyNode(bst.graph.Node):
            def __init__(self):
                self.a = bst.nn.Linear(2, 3)
                self.b = bst.nn.Linear(3, 2)
                self.c = [bst.nn.Linear(1, 2), bst.nn.Linear(1, 3)]
                self.d = {'x': bst.nn.Linear(1, 3), 'y': bst.nn.Linear(1, 4)}

        graphdef, statetree = bst.graph.flatten(MyNode())
        # print(graphdef)
        print(statetree)
        # print(bst.graph.unflatten(graphdef, statetree))

    def test_split(self):
        class Foo(bst.graph.Node):
            def __init__(self):
                self.a = bst.nn.Linear(2, 2)
                self.b = bst.nn.BatchNorm1d([10, 2])

        node = Foo()
        graphdef, params, others = bst.graph.treefy_split(node, bst.ParamState, ...)

        print(params)
        print(jax.tree.map(jnp.shape, params))

        print(jax.tree.map(jnp.shape, others))

    def test_merge(self):
        class Foo(bst.graph.Node):
            def __init__(self):
                self.a = bst.nn.Linear(2, 2)
                self.b = bst.nn.BatchNorm1d([10, 2])

        node = Foo()
        graphdef, params, others = bst.graph.treefy_split(node, bst.ParamState, ...)

        new_node = bst.graph.treefy_merge(graphdef, params, others)

        assert isinstance(new_node, Foo)
        assert isinstance(new_node.b, bst.nn.BatchNorm1d)
        assert isinstance(new_node.a, bst.nn.Linear)

    def test_update_states(self):
        x = jnp.ones((1, 2))
        y = jnp.ones((1, 3))
        model = bst.nn.Linear(2, 3)

        def loss_fn(x, y):
            return jnp.mean((y - model(x)) ** 2)

        def sgd(ps, gs):
            updates = jax.tree.map(lambda p, g: p - 0.1 * g, ps.value, gs)
            ps.value = updates

        prev_loss = loss_fn(x, y)
        weights = model.states()
        grads = bst.augment.grad(loss_fn, weights)(x, y)
        for key, val in grads.items():
            sgd(weights[key], val)
        assert loss_fn(x, y) < prev_loss

    def test_pop_states(self):
        class Model(bst.nn.Module):
            def __init__(self):
                super().__init__()
                self.a = bst.nn.Linear(2, 3)
                self.b = bst.nn.LIF([10, 2])

        model = Model()
        with bst.catch_new_states('new'):
            bst.nn.init_all_states(model)
        # print(model.states())
        self.assertTrue(len(model.states()) == 2)
        model_states = bst.graph.pop_states(model, 'new')
        print(model_states)
        self.assertTrue(len(model.states()) == 1)
        assert not hasattr(model.b, 'V')
        # print(model.states())

    def test_treefy_split(self):
        class MLP(bst.graph.Node):
            def __init__(self, din: int, dmid: int, dout: int, n_layer: int = 3):
                self.input = bst.nn.Linear(din, dmid)
                self.layers = [bst.nn.Linear(dmid, dmid) for _ in range(n_layer)]
                self.output = bst.nn.Linear(dmid, dout)

            def __call__(self, x):
                x = bst.functional.relu(self.input(x))
                for layer in self.layers:
                    x = bst.functional.relu(layer(x))
                return self.output(x)

        model = MLP(2, 1, 3)
        graph_def, treefy_states = bst.graph.treefy_split(model)

        print(graph_def)
        print(treefy_states)

        # states = bst.graph.states(model)
        # print(states)
        # nest_states = states.to_nest()
        # print(nest_states)

    def test_states(self):
        class MLP(bst.graph.Node):
            def __init__(self, din: int, dmid: int, dout: int, n_layer: int = 3):
                self.input = bst.nn.Linear(din, dmid)
                self.layers = [bst.nn.Linear(dmid, dmid) for _ in range(n_layer)]
                self.output = bst.nn.LIF(dout)

            def __call__(self, x):
                x = bst.functional.relu(self.input(x))
                for layer in self.layers:
                    x = bst.functional.relu(layer(x))
                return self.output(x)

        model = bst.nn.init_all_states(MLP(2, 1, 3))
        states = bst.graph.states(model)
        print(states)
        nest_states = states.to_nest()
        print(nest_states)

        params, others = bst.graph.states(model, bst.ParamState, bst.ShortTermState)
        print(params)
        print(others)


if __name__ == '__main__':
    absltest.main()
