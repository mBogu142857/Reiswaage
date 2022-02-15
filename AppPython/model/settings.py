from marshmallow import Schema, fields, post_load, post_dump, pprint


class Settings:
    """This class contains the settings

    """
    def __init__(self, n_el: int = 0, b_offs: int = 0, est_prec: int = 0):

        self.n_el = n_el
        self.b_offs = b_offs
        self.est_prec = est_prec

    def __repr__(self):
        return "<Settings n_el={self.n_el}, b_offs={self.b_offs}, " \
               "est_prec={self.est_prec}>".format(self=self)

    def clear(self):
        """Clear/reset method
        """
        self.n_el: int = 0
        self.b_offs: int = 0
        self.est_prec: int = 0

    def set_settings_param(self,  n_el, b_offs, est_prec):
        """Set parameters
        :param n_el:
        :param b_offs:
        :param est_prec:
        :return: None
        """
        self.n_el = n_el
        self.b_offs = b_offs
        self.est_prec = est_prec


class SettingsSchema(Schema):
    class Meta:
        ordered = True

    n_el = fields.Int(required=True)
    b_offs = fields.Int(required=True)
    est_prec = fields.Int(required=True)

    @post_load
    def load_settings(self, data, **kwargs):
        return Settings(**data)


if __name__ == "__main__":
    daObject = Settings()
    schema = SettingsSchema()

    result = SettingsSchema().dumps(daObject)
    pprint(result)

    newObject = schema.loads(result)
    print(str(newObject))
