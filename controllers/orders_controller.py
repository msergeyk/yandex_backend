from configs.db import Session
from models import Order, Courier
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import TSRANGE, ARRAY
from controllers.utils import process_str_list, intersect
from datetime import datetime
import dateutil.parser


def validate_order_id(data):
    session = Session()
    existing_ids = session.query(Order.order_id).all()
    existing_set = set([x[0] for x in existing_ids])
    new_ids = [c["order_id"] for c in data]
    new_set = set(new_ids)
    intersection = new_set.intersection(existing_set)
    result = []
    if len(intersection) != 0:
        result = [{"id": x, "message": "id already exists"}
                  for x in intersection]
    session.close()
    return result


def create_orders(data):
    session = Session()
    new_ids = [c["order_id"] for c in data]
    orders_list = [
        Order(
            order_id=o["order_id"],
            weight=o["weight"],
            region=o["region"],
            delivery_hours=cast(process_str_list(o["delivery_hours"]),
                                ARRAY(TSRANGE)),
        )
        for o in data
    ]
    session.add_all(orders_list)
    session.commit()
    result_list = [{"id": x} for x in new_ids]
    result = {"orders": result_list}
    session.close()
    return result


def assign_orders(courier_id):
    session = Session()
    current_orders = (
        session.query(Order.order_id, Order.assign_time)
        .filter(Order.cour_id == courier_id, Order.status == "assigned")
        .all()
    )
    if len(current_orders) > 0:
        orders_list = [{"id": x.order_id} for x in current_orders]
        assign_time = current_orders[0].assign_time.isoformat()[:-4] + "Z"
        result = {"orders": orders_list, "assign_time": assign_time}
    else:
        courier = session.query(Courier).filter(
            Courier.courier_id == courier_id).first()
        available_orders = session.query(Order).filter(
            Order.status == "created").all()
        assign_list = []
        for av_ord in available_orders:
            if (
                (av_ord.weight <= courier.weight)
                and (av_ord.region in courier.regions)
                and intersect(av_ord.delivery_hours, courier.working_hours)
            ):
                assign_list.append(av_ord.order_id)
        if len(assign_list) > 0:
            session.query(Order).filter(
                Order.order_id.in_(assign_list)).update(
                {
                    Order.status: "assigned",
                    Order.cour_id: courier_id,
                    Order.assign_time: datetime.utcnow(),
                },
                synchronize_session=False,
            )
            session.commit()
            current_orders = (
                session.query(Order.order_id, Order.assign_time)
                .filter(Order.cour_id == courier_id,
                        Order.status == "assigned")
                .all()
            )
            orders_list = [{"id": x.order_id} for x in current_orders]
            assign_time = current_orders[0].assign_time.isoformat()[:-4] + "Z"
            result = {"orders": orders_list, "assign_time": assign_time}
        else:
            result = {"orders": []}
    session.close()
    return result


def complete_order(courier_id, order_id, complete_time):
    session = Session()
    order = (
        session.query(Order)
        .filter(Order.order_id == order_id, Order.cour_id == courier_id)
        .first()
    )
    if order:
        status = 200
        result = {"order_id": order.order_id}
        if order.status != "completed":
            complete_time = dateutil.parser.isoparse(
                complete_time).astimezone()
            session.query(Order).filter(Order.order_id == order_id).update(
                {Order.status: "completed",
                 Order.complete_time: complete_time},
                synchronize_session=False,
            )
    else:
        status = 400
        result = []
    session.commit()
    session.close()
    return (status, result)
