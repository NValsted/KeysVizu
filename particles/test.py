from base import fluids_base_ext

class Bonk:
    def __init__(self):
        self.FluidField = fluids_base_ext.pyFluidField(32,0.2,0.1,0.001)
        self.FluidField.iterate()

    def update(self):
        self.FluidField.add_velocity(15,15,20,20)
        self.FluidField.add_density(15,15,2)
        self.FluidField.iterate()

bonk_FF = Bonk()
for i in range(10):
    bonk_FF.update()