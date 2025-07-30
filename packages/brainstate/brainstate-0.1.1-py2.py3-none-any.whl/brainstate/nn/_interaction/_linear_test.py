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

import brainunit as u
from absl.testing import parameterized

import brainstate as bst


class TestDense(parameterized.TestCase):
    @parameterized.product(
        size=[(10,),
              (20, 10),
              (5, 8, 10)],
        num_out=[20, ]
    )
    def test_Dense1(self, size, num_out):
        f = bst.nn.Linear(10, num_out)
        x = bst.random.random(size)
        y = f(x)
        self.assertTrue(y.shape == size[:-1] + (num_out,))


class TestSparseMatrix(unittest.TestCase):
    def test_csr(self):
        data = bst.random.rand(10, 20)
        data = data * (data > 0.9)
        f = bst.nn.SparseLinear(u.sparse.CSR.fromdense(data))

        x = bst.random.rand(10)
        y = f(x)
        self.assertTrue(
            u.math.allclose(
                y,
                x @ data
            )
        )

        x = bst.random.rand(5, 10)
        y = f(x)
        self.assertTrue(
            u.math.allclose(
                y,
                x @ data
            )
        )

    def test_csc(self):
        data = bst.random.rand(10, 20)
        data = data * (data > 0.9)
        f = bst.nn.SparseLinear(u.sparse.CSC.fromdense(data))

        x = bst.random.rand(10)
        y = f(x)
        self.assertTrue(
            u.math.allclose(
                y,
                x @ data
            )
        )

        x = bst.random.rand(5, 10)
        y = f(x)
        self.assertTrue(
            u.math.allclose(
                y,
                x @ data
            )
        )

    def test_coo(self):
        data = bst.random.rand(10, 20)
        data = data * (data > 0.9)
        f = bst.nn.SparseLinear(u.sparse.COO.fromdense(data))

        x = bst.random.rand(10)
        y = f(x)
        self.assertTrue(
            u.math.allclose(
                y,
                x @ data
            )
        )

        x = bst.random.rand(5, 10)
        y = f(x)
        self.assertTrue(
            u.math.allclose(
                y,
                x @ data
            )
        )
