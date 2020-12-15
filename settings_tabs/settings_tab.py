from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

import os

from misc.browsers import *

class SettingsTab(TabbedPanelItem):

    def dismiss_popup(self):
        self.popup_window.dismiss()

    def show_file_chooser(self, dialog_type = "load", filter_strings = ['*'], initial_directory = "/", callback = None):
        
        if dialog_type == "load":
            content = LoadDialog(load = self.load_file, cancel = self.dismiss_popup)
        else:
            content = SaveDialog(save = self.save_file, cancel = self.dismiss_popup)

        content.filter_strings = filter_strings
        content.initial_directory = initial_directory

        if callback is not None:
            content.callback = callback
        
        self.popup_window = Popup(title = "File browser",
                                  content = content,
                                  size_hint = (0.5,0.5) )
        self.popup_window.open()

    def load_file(self,path,filename):
        if 'callback' in self.popup_window.content.__dir__():
            self.popup_window.content.callback(os.path.join(path, filename[0]))
        else:
            print(os.path.join(path, filename[0]))

        self.popup_window.dismiss()

    def save_file(self,path,filename):
        if 'callback' in self.popup_window.content.__dir__():
            self.popup_window.content.callback(os.path.join(path, filename))
        else:
            print(os.path.join(path, filename))

        self.popup_window.dismiss()

    def show_color_chooser(self, callback = None):
        content = ColorBrowser(apply = self.apply_color, cancel = self.dismiss_popup)

        if callback is not None:
            content.callback = callback

        self.popup_window = Popup(title = "Color browser",
                                  content = content,
                                  size_hint = (0.5,0.5) )

        self.popup_window.open()

    def apply_color(self,color):
        if 'callback' in self.popup_window.content.__dir__():
            self.popup_window.content.callback(color)
        else:
            print(color)

        self.popup_window.dismiss()