from configs.db import Session
from models import Courier, Order
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import TSRANGE, ARRAY
from controllers.utils import process_str_list, intersect, process_dti


def validate_courier_id(data):
    session = Session()
    existing_ids = session.query(Courier.courier_id).all()
    existing_set = set([x[0] for x in existing_ids])
    new_ids = [c["courier_id"] for c in data]
    new_set = set(new_ids)
    intersection = new_set.intersection(existing_set)
    result = []
    if len(intersection) != 0:
        result = [{"id": x, "message": "id already exists"}
                  for x in intersection]
    session.close()
    return result


def create_couriers(data):
    session = Session()
    new_ids = [c["courier_id"] for c in data]
    couriers_list = [
        Courier(
            courier_id=c["courier_id"],
            courier_type=c["courier_type"],
            regions=c["regions"],
            working_hours=cast(process_str_list(c["working_hours"]),
                               ARRAY(TSRANGE)),
        )
        for c in data
    ]
    session.add_all(couriers_list)
    session.commit()
    result_list = [{"id": x} for x in new_ids]
    result = {"couriers": result_list}
    session.close()
    return result


def update_courier(data, courier_id):
    session = Session()
    c = session.query(Courier).filter(Courier.courier_id == courier_id).first()
    if c:
        courier_type = data.get("courier_type", c.courier_type)
        regions = data.get("regions", c.regions)
        if data.get("working_hours"):
            working_hours = process_str_list(data["working_hours"])
        else:
            working_hours = [str(x) for x in c.working_hours]
        session.query(Courier).filter(Courier.courier_id == courier_id).update(
            {
                Courier.courier_type: courier_type,
                Courier.regions: regions,
                Courier.working_hours: cast(working_hours, ARRAY(TSRANGE)),
            },
            synchronize_session=False,
        )
        session.commit()
        active_orders = (
            session.query(Order)
            .filter(Order.cour_id == courier_id, Order.status == "assigned")
            .all()
        )
        courier = session.query(Courier).filter(
            Courier.courier_id == courier_id).first()
        if len(active_orders) > 0:
            orders_to_update = []
            for act_ord in active_orders:
                if not (
                    (act_ord.weight <= courier.weight)
                    and (act_ord.region in courier.regions)
                    and intersect(act_ord.delivery_hours,
                                  courier.working_hours)
                ):
                    orders_to_update.append(act_ord.order_id)
            if len(orders_to_update) > 0:
                session.query(Order).filter(
                    Order.order_id.in_(orders_to_update)
                ).update(
                    {
                        Order.status: "created",
                        Order.cour_id: None,
                        Order.assign_time: None,
                    },
                    synchronize_session=False,
                )
                session.commit()
        status = 200
        result = {
            "courier_id": courier.courier_id,
            "courier_type": courier.courier_type,
            "regions": courier.regions,
            "working_hours": [process_dti(x) for x in courier.working_hours],
        }
    else:
        status = 404
        result = []
    session.close()
    return (status, result)


def is_courier_id_exists(courier_id):
    session = Session()
    c = session.query(Courier).filter(Courier.courier_id == courier_id).first()
    if c:
        return True
    session.close()
    return False
