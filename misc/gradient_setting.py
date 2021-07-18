from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty, ObjectProperty
from kivy.core.window import Window
from kivy.clock import Clock

import numpy as np
import random

from misc.browsers import BrowserMixin

import c_utils
config = c_utils.load_config()


class GradientStopMarker(Widget):
    boundary_img_path = "UI/menu/GradientStopMarkerBoundary.png"
    collision_bounds = None
    colliding = False

    def __init__(self, **kwargs):
        super(GradientStopMarker, self).__init__(**kwargs)
        self.marker_size = kwargs["size"]

        with self.canvas:
            Rectangle(source=self.boundary_img_path, **kwargs)

        self.collision_bounds = self._calculate_collision_bounds()

    def _calculate_collision_bounds(self):
        return [
            self.pos[0],
            self.pos[1],
            self.pos[0] + self.marker_size[0],
            self.pos[1] + self.marker_size[1]
        ]

    def collide_point(self, pos):
        if self.collision_bounds[0] < pos[0] < self.collision_bounds[2]\
            and self.collision_bounds[1] < pos[1] < self.collision_bounds[3]:
                return True
        return False

    def move_to_pos(self, pos):
        self.canvas.clear()
        with self.canvas:
            self.pos[0] = max(pos[0], self.parent.pos[0])
            self.pos[0] = min(
                self.pos[0],
                self.parent.pos[0] + self.parent.size[0]
            )
            self.pos[0] -= (self.marker_size[0] / 2) 
            Rectangle(
                source=self.boundary_img_path,
                pos=self.pos,
                size=self.marker_size
            )
        self.collision_bounds = self._calculate_collision_bounds()

    def on_mouse_pos(self, window, pos):
        if self.colliding:
            self.move_to_pos(pos)


class ColorGradientBar(BoxLayout, BrowserMixin):
    bar_texture = ObjectProperty(Texture)
    stop_markers = []
    buffer = None
    
    color_properties = c_utils.load_json(
        f"{config['project']['projects_location']}{config['project']['default']}"
    )["particles"]["style"]["color"]
    
    def __init__(self, **kwargs):
        super(ColorGradientBar, self).__init__(**kwargs)
        self.bar_texture = self.create_gradient_texture(
            self.color_properties
        )

    def tab_active_init(self):
        self.stop_markers = [ 
            GradientStopMarker(
                size=(15, self.height),
                pos = (
                    self.pos[0] + stop * self.size[0] - 15/2,
                    self.pos[1]
                ) 
            ) for stop in self.color_properties["stops"]
        ]
        for stop in self.stop_markers:
            stop.bind(pos=self.edit_stop_pos)  # Remember to unbind if delete
            self.add_widget(stop)

    def on_touch_down(self, touch):
        for stop in self.stop_markers:
            if stop.collide_point(touch.pos):
                stop.colliding = True
                Window.bind(mouse_pos = stop.on_mouse_pos)
                break  # Break to prevent case where multiple markers get stuck on top of each other

        return super().on_touch_down(touch)

    def on_touch_up(self, mouse_motion_event):
        no_collisions = True
        for stop in self.stop_markers:

            if stop.colliding:
                stop.colliding = False
                Window.unbind(mouse_pos = stop.on_mouse_pos)
                if mouse_motion_event.is_double_tap:
                    self.load_color_wheel(stop)
                    # Perhaps add delete option here as well
                no_collisions = False                
                break  # Break to handle case where multiple markers are on top of each other

        if mouse_motion_event.is_double_tap and no_collisions\
            and self.collide_point(*mouse_motion_event.pos):
            self.add_stop(mouse_motion_event.pos)

    def load_color_wheel(self, stop):
        self.show_color_chooser(lambda *args: self.edit_stop_rgba(stop, *args))

    def edit_stop_rgba(self, stop_marker, rgba):
        for i in range(len(self.stop_markers)):
            if self.stop_markers[i] == stop_marker:
                self.color_properties["RGBA"][i] = rgba
                break
                
        _, idx_map = c_utils.valid_color_gradient(
            self.color_properties
        )
        self.bar_texture = self.update_gradient_texture(
            self.bar_texture,
            self.color_properties
        )

    def edit_stop_pos(self, stop_marker, pos):
        for i in range(len(self.stop_markers)):
            if self.stop_markers[i] == stop_marker:
                t = (pos[0] - self.pos[0]) / (
                    (self.pos[0] + self.size[0]) - self.pos[0]
                )
                self.color_properties["stops"][i] = t
                break
        
        _, idx_map = c_utils.valid_color_gradient(
            self.color_properties
        )
        self.stop_markers = [self.stop_markers[idx] for idx in idx_map]
        self.bar_texture = self.update_gradient_texture(
            self.bar_texture,
            self.color_properties
        )

    def add_stop(self, pos):
        # TODO: fix odd behaviour when inserting new stop
        t = (pos[0] - self.pos[0]) / (
            (self.pos[0] + self.size[0]) - self.pos[0]
        )
        self.color_properties["stops"].append(t)
        self.color_properties["RGBA"].append([0.5, 0.5, 0.5, 1])

        new_marker = GradientStopMarker(
            size=(15, self.height),
            pos = (
                self.pos[0] + t * self.size[0] - 15/2,
                self.pos[1]
            ) 
        )

        new_marker.bind(pos=self.edit_stop_pos)
        insert_idx = len(self.stop_markers)
        for i, stop in enumerate(self.stop_markers):
            if stop.pos[0] > new_marker.pos[0]:
                insert_idx = i
                break

        self.stop_markers.insert(
            insert_idx, new_marker
        )
        self.add_widget(new_marker)

    def create_gradient_texture(self, color_properties, resolution=(64, 64)):
        texture = Texture.create(size=resolution, colorfmt="rgba")

        self.buffer = np.zeros((*resolution, 4), dtype=np.ubyte)
        texture = self.update_gradient_texture(texture, color_properties)
        
        return texture

    def update_gradient_texture(self, texture, color_properties):
        for i in range(self.buffer.shape[1]):
            RGBA_val = c_utils.interpolate_color(color_properties, i / 64)
            for j in range(4):
                self.buffer[:, i, j] = RGBA_val[j] * 255
        
        texture.blit_buffer(
            self.buffer.ravel(),
            colorfmt="rgba",
            bufferfmt="ubyte"
        )

        return texture

    def update(self):
        self.update_gradient_texture(self.bar_texture, self.color_properties)
        for i, stop_marker in enumerate(self.stop_markers):
            t = self.color_properties["stops"][i]
            stop_marker.move_to_pos(
                (self.pos[0] + t * self.size[0] + 15/2, None)
            )
