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

from vathos.gpu.context import OffscreenContextManager

class TestOffscreenContextManager(unittest.TestCase):

  def test_enter(self):
    with OffscreenContextManager():
      gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
      fbos = gl.glGenFramebuffers(2)
      self.assertEqual(len(fbos), 2)
      self.assertEqual(fbos[0], 1)
      self.assertEqual(fbos[1], 2)
