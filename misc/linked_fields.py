from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, \
    StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock

class LinkedFieldsGroup(Widget):
    fields = ListProperty([])
    linked = BooleanProperty(True)
    group_type = StringProperty("ratio")
    
    def __init__(self, **kwargs):
        super(LinkedFieldsGroup, self).__init__(**kwargs)

        self.update_rules = {'ratio': self.__ratio,
                             'difference': self.__difference} # TODO: allow custom update rule

    def __ratio(self,subject,source,target):
        ratio = target / source
        return subject * ratio

    def __difference(self,subject,source,target):
        diff = target - source
        return subject + diff

    def update_group(self,initiative_field):

        if self.linked:
            for field in self.fields:
                if field != initiative_field: # needs to support float type as well
                    field.value[0] = self.update_rules[self.group_type](field.value[0],
                                                                        initiative_field.value[0],
                                                                        int(initiative_field.text))
                    
                    field.value[0] = int(round(field.value[0]))
                    field.text = str(field.value[0])
        else:
            print("not linked bro")

        #print(initiative_field.input_filter) # Could use this to support float type
        initiative_field.value[0] = int(initiative_field.text)

class LinkedFieldsLock(ToggleButton):
    def toggle_lock(self):
        if self.state == 'down':
            self.group.linked = True
        else:
            self.group.linked = False

class LinkedNumericField(TextInput):
    previous_value = NumericProperty(None)

    def __init__(self, **kwargs):
        super(LinkedNumericField, self).__init__(**kwargs)
        
        Clock.schedule_once(lambda dt: self.group.fields.append(self),1)