from marshmallow import Schema, fields
from marshmallow import Schema, ValidationError, validates, validates_schema
from marshmallow.fields import Date, Dict, Float, Int, List, Nested, Str
from marshmallow.validate import Length, OneOf, Range
from datetime import datetime
import dateutil.parser


class CourierSchema(Schema):
    courier_id = Int(validate=Range(min=1), strict=True, required=True)
    courier_type = Str(validate=OneOf(['foot', 'bike', 'car']), strict=True, required=True)
    regions = List(Int(validate=Range(min=1), strict=True), validate=Length(min=1), required=True)
    working_hours = List(Str(validate=validate_hours, strict=True),
                         validate=Length(min=1), required=True)


class CourierPatchSchema(Schema):
    courier_type = Str(validate=OneOf(['foot', 'bike', 'car']), strict=True)
    regions = List(Int(validate=Range(min=1), strict=True), validate=Length(min=1))
    working_hours = List(Str(validate=validate_hours, strict=True),
                         validate=Length(min=1))


class OrderSchema(Schema):
    order_id = Int(validate=Range(min=1), strict=True, required=True)
    weight = Float(validate=Range(min=0.01, max=50), strict=True, required=True)
    region = Int(validate=Range(min=1), strict=True, required=True)
    delivery_hours = List(Str(validate=validate_hours, strict=True),
                         validate=Length(min=1), required=True)


class OrdersAssignSchema(Schema):
    courier_id = Int(validate=Range(min=1), strict=True, required=True)


class OrderCompleteSchema(Schema):
    courier_id = Int(validate=Range(min=1), strict=True, required=True)
    order_id = Int(validate=Range(min=1), strict=True, required=True)
    complete_time = Str(strict=True, required=True)

    @validates('complete_time')
    def validate_dt(self, dt):
        try:
            t = dateutil.parser.isoparse(dt).astimezone()
            if t > datetime.utcnow().astimezone():
                raise ValidationError("Incorrect timestamp")
        except:
            raise ValidationError("Incorrect timestampt")


def validate_hours(s):
    if len(s) != 11:
        raise ValidationError("Incorrect time segment format")
    if s[5] != '-':
        raise ValidationError("Incorrect time segment format")
    try:
        t1 = datetime.strptime(s[:5], '%H:%M')
        t2 = datetime.strptime(s[6:], '%H:%M')
        if t1 >= t2:
            raise ValidationError("Incorrect time segment format")
    except:
        raise ValidationError("Incorrect time segment format")











try:
    result = CourierSchema().load({"courier_id": 1,
                                   "courier_type": 'foot',
                                   "regions": [1], 
                                   "working_hours": ['12:00-14:00']})
    print(result)
except ValidationError as err:
    print(err.messages)
    print(err.valid_data)
