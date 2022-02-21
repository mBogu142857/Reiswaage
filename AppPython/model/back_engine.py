# import all internal and external libraries
from csv import reader
import numpy as np
from marshmallow import Schema, fields, post_load, post_dump, pprint
from model.settings import SettingsSchema, Settings
import copy

from model.settings import Settings
from model.measure import Measure

class BackEngine:
    def __init__(self, measure=Measure(), settings=Settings()):
        self.measure = measure
        self.settings = settings

    def __repr__(self):
        return "<BackEngine data={self.data}, settings={self.settings}>".format(self=self)

    def clear(self):
        """
        Clear
        :return: None
        """
        self.measure.clear()
        self.settings.clear()

    def set_settings_param(self, n_el, b_offs, est_prec):
        """
        Set the settings parameters
        :param n_el:
        :param b_offs:
        :param est_prec:
        :return: None
        """
        self.settings.set_settings_param(n_el, b_offs, est_prec)

    def compute_measure(self):
        """
        Compute the measures
        :return: None
        """
        self.measure.perform_measurement()

    def toolchain(self):
        """This function calls all the steps of the processing and computing functions and populated the corresponding
         fields in the App data structure
        :return: None
        """
        self.clear()
        self.compute_measure()


        """ Example on how to plot something while in debug mode (right click, evaluate selected)
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        x = np.linspace(0, 100, 100)
        y = np.linspace(0, 100, 100)
        ax.plot(x, y, 'b', linewidth=0.8, 'r', linewidth=0.8, label='Example Plot')
        ax.plot(x, y, 'b', linewidth=0.8, 'r*', label='Example Plot')
        """

        return None

class BackEngineSchema(Schema):
    class Meta:
        ordered = True

    settings = fields.Nested(SettingsSchema, required=True)

@post_load
def load_back_engine(self, data, **kwargs):
    return BackEngine(**data)


if __name__ == "__main__":
    daObject = BackEngine()
    schema = BackEngineSchema()

    result = BackEngineSchema().dumps(daObject)
    pprint(result)

    newObject = schema.loads(result)
    print(str(newObject))
