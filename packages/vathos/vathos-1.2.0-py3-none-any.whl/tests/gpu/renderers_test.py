# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020-2021, Vathos GmbH
#
# All rights reserved.
#
###############################################################################
import unittest
import os

os.environ['PYOPENGL_PLATFORM'] = 'osmesa'

import OpenGL.GL as gl
import numpy as np
import trimesh

from vathos.gpu.context import OffscreenContextManager
from vathos.gpu.renderers import SimpleDepthRenderer
from vathos.geometry.vantage_point import SampledPinholeProjection


class TestSimpleDepthRenderer(unittest.TestCase):

  def setUp(self):

    K = np.array([[400, 0, 256], [0, 400, 212], [0, 0, 1]], dtype='f')
    size = (512, 424)
    self.projection = SampledPinholeProjection(K, size, znear=0.01, zfar=10.0)
    # fronto parallel cube with local frame in the barycenter, side length 1
    self.mesh = trimesh.load('./res/cube.obj')

    # compute expected corners
    corners = np.array([[-1, -1, 7], [-1, 1, 7], [1, -1, 7], [1, 1, 7]],
                       dtype='f')
    corners_hom = np.vstack((corners[:, 0] / corners[:, 2],
                             corners[:, 1] / corners[:, 2])).transpose()
    corners_projected = corners_hom @ K[:2, :2].transpose() + np.ones(
        corners_hom.shape) @ np.diag(K[:2, 2])

    self.corners_expected = np.rint(corners_projected).astype('uint16')

  def test_add_node(self):
    with OffscreenContextManager():
      renderer = SimpleDepthRenderer(self.projection)
      renderer.add_node('test', self.mesh, np.eye(4, dtype='f'))
      self.assertIn('test', renderer.generators)
      self.assertIn('test', renderer.transforms)
      self.assertRaises(RuntimeError, renderer.add_node, 'test', self.mesh,
                        np.eye(4, dtype='f'))

  def test_render(self):
    with OffscreenContextManager():
      renderer = SimpleDepthRenderer(self.projection)

      transform = np.eye(4, dtype='f')
      transform[2, 3] = 8.0
      renderer.add_node('test', self.mesh, transform)

      image = renderer.render()
      self.assertGreater(image[:, :, 3].sum(), 0)
      # test depth
      np.testing.assert_almost_equal(image[:, :, 2].max(), 7.0, decimal=3)
      # test projection
      patch_size = 1
      for i in range(0, self.corners_expected.shape[0]):
        patch = image[self.corners_expected[i, 1] -
                      patch_size:self.corners_expected[i, 1] +
                      patch_size, self.corners_expected[i, 0] -
                      patch_size:self.corners_expected[i, 0] + patch_size, 3]
        # for a corner, we should have 3 black and 1 white pixel
        self.assertEqual((patch==0.0).sum(), 3)
        self.assertEqual((patch==1.0).sum(), 1)