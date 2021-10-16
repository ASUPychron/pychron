# ===============================================================================
# Copyright 2015 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================
# ============= standard library imports ========================
# ============= local library imports  ==========================
from __future__ import absolute_import

import math

from pychron.canvas.canvas2D.scene.primitives.base import Connectable
from pychron.canvas.canvas2D.scene.primitives.connections import Tee, Fork, Elbow
from pychron.canvas.canvas2D.scene.primitives.primitives import (
    Rectangle,
    Bordered,
    BorderLine,
)


def rounded_rect(gc, x, y, width, height, corner_radius):
    with gc:
        gc.translate_ctm(x, y)  # draw a rounded rectangle
        x = y = 0
        gc.begin_path()

        hw = width * 0.5
        hh = height * 0.5
        if hw < corner_radius:
            corner_radius = hw * 0.5
        elif hh < corner_radius:
            corner_radius = hh * 0.5

        gc.move_to(x + corner_radius, y)
        gc.arc_to(x + width, y, x + width, y + corner_radius, corner_radius)
        gc.arc_to(
            x + width, y + height, x + width - corner_radius, y + height, corner_radius
        )
        gc.arc_to(x, y + height, x, y, corner_radius)
        gc.arc_to(x, y, x + width + corner_radius, y, corner_radius)
        gc.draw_path()


class RoundedRectangle(Rectangle, Connectable, Bordered):
    corner_radius = 8.0
    display_name = None
    fill = True
    use_border_gaps = True

    def get_tooltip_text(self):
        return "Stage={}\nVolume={}".format(self.name, self.volume)

    def _render(self, gc):
        corner_radius = self.corner_radius
        with gc:
            width, height = self.get_wh()
            x, y = self.get_xy()
            if self.fill:
                rounded_rect(gc, x, y, width, height, corner_radius)

            self._render_border(gc, x, y, width, height)

            gc.set_fill_color(self._convert_color(self.name_color))
            if self.display_name:
                self._render_textbox(gc, x, y, width, height, self.display_name)
            elif not self.display_name == "":
                self._render_name(gc, x, y, width, height)

    def _render_border(self, gc, x, y, width, height):
        if self.use_border:

            corner_radius = self.corner_radius
            with gc:
                gc.set_line_width(self.border_width)
                if self.fill:
                    c = self._get_border_color()
                else:
                    c = self.default_color
                    c = self._convert_color(c)
                    gc.set_fill_color((0, 0, 0, 0))

                gc.set_stroke_color(c)
                rounded_rect(gc, x, y, width, height, corner_radius)

            if self.use_border_gaps:
                # from pychron.canvas.canvas2D.scene.primitives.connections import Fork, Tee

                with gc:
                    for t, c in self.connections:
                        with gc:
                            gc.set_line_width(self.border_width + 1)
                            if isinstance(c, Elbow):
                                p1, p2 = c.start_point, c.end_point

                                if p1.y < p2.y:
                                    p1x, p1y = p1.get_xy()
                                    gc.move_to(p1x - 5, y + height)
                                    gc.line_to(p1x + 5, y + height)

                                else:
                                    if c.corner == "ll":
                                        p1x, p1y = p1.get_xy()
                                        gc.move_to(p1x - 5, p1y)
                                        gc.line_to(p1x + 5, p1y)

                                    else:
                                        p2x, p2y = p2.get_xy()
                                        xx = x

                                        if p1.x >= self.x:
                                            xx = x + width
                                        gc.move_to(xx, p2y - 5)
                                        gc.line_to(xx, p2y + 5)

                            elif isinstance(c, BorderLine):
                                p1, p2 = c.start_point, c.end_point
                                p2x, p2y = p2.get_xy()
                                if p1.x == p2.x:
                                    yy = y
                                    if p1.y >= self.y:
                                        if p1.y - self.y != 1:
                                            yy = y + height

                                    p1x, p1y = p1.get_xy()
                                    gc.move_to(p1x - 5, yy)
                                    gc.line_to(p1x + 5, yy)
                                else:
                                    xx = x

                                    if p1.x >= self.x:
                                        xx = x + width
                                    gc.move_to(xx, p2y - 5)
                                    gc.line_to(xx, p2y + 5)

                            elif isinstance(c, Tee):
                                if t == "mid":
                                    yy = y if c.left.y < self.y else y + height
                                    mx = c.get_midx()
                                    gc.move_to(mx - 5, yy)
                                    gc.line_to(mx + 5, yy)
                                else:
                                    gc.set_line_width(self.border_width + 2)
                                    # gc.set_stroke_color((1,0,0))
                                    if t == "left":
                                        xx, yy = c.left.get_xy()
                                        xx += 2.5
                                    else:
                                        xx, yy = c.right.get_xy()

                                    gc.move_to(xx, yy - 5)
                                    gc.line_to(xx, yy + 5)
                            elif isinstance(c, Fork):
                                yy = y if c.left.y < self.y else y + height
                                mx = c.get_midx()
                                gc.move_to(mx - 5, yy)
                                gc.line_to(mx + 5, yy)

                            gc.draw_path()


class Spectrometer(RoundedRectangle):
    tag = "spectrometer"

    def __init__(self, *args, **kw):
        super(Spectrometer, self).__init__(*args, **kw)
        self.width = 10
        self.height = 10


class Stage(RoundedRectangle):
    tag = "stage"

    def __init__(self, *args, **kw):
        super(Spectrometer, self).__init__(*args, **kw)
        self.width = 10
        self.height = 5


class CircleStage(Connectable, Bordered):
    tag = "cirle_stage"

    def get_tooltip_text(self):
        return "Circle Stage={}\nVolume={}".format(self.name, self.volume)

    def _render(self, gc):
        with gc:
            width, height = self.get_wh()
            x, y = self.get_xy()
            gc.arc(x, y, width, 0, 360)
            gc.draw_path()

            self._render_border(gc, x, y, width)

            gc.set_fill_color(self._convert_color(self.name_color))
            if self.display_name:
                self._render_textbox(gc, x, y, width, height, self.display_name)
            elif not self.display_name == "":
                self._render_name(gc, x, y, width, height)

    def _render_textbox(self, gc, x, y, w, h, txt):

        tw, th, _, _ = gc.get_full_text_extent(txt)
        x = x - tw / 2.0
        y = y - th / 2.0

        self._render_text(gc, txt, x, y)

    def _render_border(self, gc, x, y, width):
        gc.set_line_width(self.border_width)
        with gc:
            c = self._get_border_color()
            gc.set_stroke_color(c)
            gc.arc(x, y, width, 0, 2 * math.pi)
            gc.stroke_path()

        self._render_gaps(gc, x, y, width)

    def _render_gaps(self, gc, cx, cy, r):
        gc.set_line_width(self.border_width + 2)

        def sgn(x):
            return -1 if x < 0 else 1

        def angle(x, y):
            return math.pi / 2 - math.atan2(x, y)

        with gc:
            gc.set_stroke_color(self._convert_color(self.default_color))
            for t, c in self.connections:
                if isinstance(c, BorderLine):
                    dw = math.atan((c.width - c.border_width / 2) / r)

                    p1, p2 = c.start_point, c.end_point
                    p2x, p2y = p2.get_xy()
                    p1x, p1y = p1.get_xy()

                    if p1x == p2x and p1y == p2y:
                        continue

                    p2x = p2x - cx
                    p2y = p2y - cy

                    p1x = p1x - cx
                    p1y = p1y - cy

                    dx = p2x - p1x
                    dy = p2y - p1y
                    dr = (dx ** 2 + dy ** 2) ** 0.5
                    D = p1x * p2y - p2x * p1y

                    ss = (r ** 2 * dr ** 2 - D ** 2) ** 0.5
                    plus_x = D * dy + sgn(dy) * dx * ss
                    minus_x = D * dy - sgn(dy) * dx * ss

                    plus_y = -D * dx + abs(dy) * ss
                    minus_y = -D * dx - abs(dy) * ss
                    plus_x /= dr ** 2
                    plus_y /= dr ** 2
                    minus_x /= dr ** 2
                    minus_y /= dr ** 2

                    if p2y > p1y:
                        if p2x > p1x:
                            theta = angle(plus_x, plus_y)
                        else:
                            theta = angle(minus_x, minus_y)
                    else:
                        if p2x > p1x:
                            theta = angle(minus_x, minus_y)
                        else:
                            theta = angle(plus_x, plus_y)

                    gc.arc(cx, cy, r, theta - dw, theta + dw)
                    gc.stroke_path()


# ============= EOF =============================================
