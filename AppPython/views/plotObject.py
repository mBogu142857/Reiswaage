from marshmallow import Schema, fields, post_load, post_dump, pprint

class AxesObject:
    def __init__(self, XData=[], YData=[], CData=[], XLim=[], YLim=[], Color=[]):
        self.XData = XData
        self.YData = YData
        self.CData = CData
        self.XLim = XLim
        self.YLim = YLim
        self.Color = Color

    def __repr__(self):
        return "<AxesObject  XData = {self.XData}, YData = {self.YData}, CData = {self.CData}, " \
               "XLim = {self.XLim}, YLim = {self.YLim}, Color = {self.Color}>".format(self=self)

    def clear(self):
        self.XData = []
        self.YData = []
        self.CData = []
        self.XLim = []
        self.YLim = []
        self.Color = []

class AxesObjectSchema(Schema):
    class Meta:
        ordered = True

    XData = fields.List(fields.Float(required=True))
    YData = fields.List(fields.Float(required=True))
    CData = fields.List(fields.Float(required=True))
    XLim = fields.List(fields.Float(required=True))
    YLim = fields.List(fields.Float(required=True))
    Color = fields.List(fields.Float(required=True))

@post_load
def load_axes(self, data, **kwargs):
    return AxesObject(**data)


if __name__ == "__main__":
    daObject = AxesObject()
    schema = AxesObjectSchema()

    result = AxesObjectSchema().dumps(daObject)
    pprint(result)

    newObject = schema.loads(result)
    print(str(newObject))
