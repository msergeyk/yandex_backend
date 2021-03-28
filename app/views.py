from flask import Blueprint, request, Response
from controllers.couriers_controller import create_couriers, update_courier
from controllers.orders_controller import create_orders, assign_orders, complete_order

views = Blueprint("api", __name__)

@views.route("/couriers", methods=["POST"])
def load_couriers_list():
    request_data = request.get_json()['data']
    status, result_json = create_couriers(request_data)
    if status == 'err':
        result_json = {"validation_error": result_json}
    return result_json

@views.route("/couriers/<courier_id>", methods=["PATCH"])
def update_courier_data(courier_id):
    request_data = request.get_json()
    status, result_json = update_courier(request_data, courier_id)
    return result_json


@views.route("/orders", methods=["POST"])
def load_orders_list():
    request_data = request.get_json()['data']
    status, result_json = create_orders(request_data)
    if status == 'err':
        result_json = {"validation_error": result_json}
    return result_json


@views.route("/orders/assign", methods=["POST"])
def assign():
    request_data = request.get_json()
    courier_id = request_data['courier_id']
    result_json = assign_orders(courier_id)
    return result_json


@views.route("/orders/complete", methods=["POST"])
def complete():
    request_data = request.get_json()
    courier_id = request_data['courier_id']
    order_id = request_data['order_id']
    complete_time = request_data['complete_time']
    result_json = complete_order(courier_id=courier_id,
                                 order_id=order_id,
                                 complete_time=complete_time)
    return result_json


