# The MIT License (MIT)
#
# Copyright (c) 2023-2025 Ivo Steinbrecher
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""Camera functionality for pyvista."""


def get_camera_settings(camera):
    names = [
        "clipping_range",
        "distance",
        "elevation",
        "focal_point",
        "model_transform_matrix",
        "parallel_projection",
        "parallel_scale",
        "position",
        "roll",
        "thickness",
        "up",
        "view_angle",
    ]
    camera_settings = {}
    for name in names:
        camera_settings[name] = getattr(camera, name)
    return camera_settings


def set_camera_settings(camera, settings):
    for name, value in settings.items():
        setattr(camera, name, value)
