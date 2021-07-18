from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty
from kivy.clock import Clock

from misc.browsers import BrowserMixin


class SettingsTab(TabbedPanelItem, BrowserMixin):
    tab_initialized = False

    def on_press(self, *args):
        Clock.create_trigger(self._initialize_tab)()  # Ensure action happens right after tab has been switched

    def _initialize_tab(self, *args):
        """
        If child implements tab_active_init, its contents will be run
        when the tab is pressed for the first time.
        """
        if not self.tab_initialized:
            for child in self.walk():
                if hasattr(child, "tab_active_init"):
                    child.tab_active_init()
            self.tab_initialized = True
