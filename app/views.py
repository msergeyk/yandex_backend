from flask import Blueprint, request, Response
from werkzeug.exceptions import BadRequest
from controllers.couriers_controller import create_couriers, update_courier,\
                        validate_courier_id, is_courier_id_exists
from controllers.orders_controller import create_orders, assign_orders, complete_order,\
                        validate_order_id
from schemas.schema import CourierSchema, CourierPatchSchema, OrderSchema,\
                           OrdersAssignSchema, OrderCompleteSchema
from marshmallow import ValidationError

import json

views = Blueprint("api", __name__)


@views.route("/couriers", methods=["POST"])
def load_couriers_list():
    if not request.is_json:
        raise BadRequest('Content-Type must be application/json')
    request_json = request.get_json()
    request_data = request_json.get("data")
    if (request_data is None) or (len(request_data) == 0):
        raise BadRequest('json should contain not emtpy data field')

    error_messages = []
    not_validated_idx = []
    status = 201
    for i, data in enumerate(request_data):
        err_msg = {}
        try:
            CourierSchema().load(data)
        except ValidationError as err:
            err_msg = err.messages
        if len(err_msg) != 0:
            error_messages.append(err_msg)
            not_validated_idx.append(i)
            status = 400
    if status == 400:
        not_val_ids = [request_data[x]['courier_id'] for x in not_validated_idx]
        id_msg = [{"id": c_id, "message": error_messages[i]}
                  for i, c_id in enumerate(not_val_ids)]
        validated_data = [d for i, d in enumerate(request_data) if i not in not_validated_idx]
        existing_ids = validate_courier_id(validated_data)
        if len(existing_ids) > 0:
            id_msg.append(existing_ids)
        result = {"validation_error": {'couriers': id_msg}}
    else:
        existing_ids = validate_courier_id(request_data)
        if len(existing_ids) > 0:
            status = 400
            result = {"validation_error": {'couriers': existing_ids}}
        else:
            result = create_couriers(request_data)
    return Response(json.dumps(result), status, mimetype='application/json')


@views.route("/couriers/<courier_id>", methods=["PATCH"])
def update_courier_data(courier_id):
    if not request.is_json:
        raise BadRequest('Content-Type must be application/json')

    request_data = request.get_json()
    err_msg = {}
    try:
        CourierPatchSchema().load(request_data)
    except ValidationError as err:
        err_msg = err.messages
    if len(err_msg) != 0:
        return Response(status=400)
    status, result = update_courier(request_data, courier_id)
    if status == 200:
        return Response(json.dumps(result), status, mimetype='application/json')
    else:
        return Response(status=404)


@views.route("/orders", methods=["POST"])
def load_orders_list():
    if not request.is_json:
        raise BadRequest('Content-Type must be application/json')
    request_json = request.get_json()
    request_data = request_json.get("data")
    if (request_data is None) or (len(request_data) == 0):
        raise BadRequest('json should contain not emtpy data field')
    
    error_messages = []
    not_validated_idx = []
    status = 201
    for i, data in enumerate(request_data):
        err_msg = {}
        try:
            OrderSchema().load(data)
        except ValidationError as err:
            err_msg = err.messages
        if len(err_msg) != 0:
            error_messages.append(err_msg)
            not_validated_idx.append(i)
            status = 400
    if status == 400:
        not_val_ids = [request_data[x]['order_id'] for x in not_validated_idx]
        id_msg = [{"id": c_id, "message": error_messages[i]}
                for i, c_id in enumerate(not_val_ids)]
        validated_data = [d for i, d in enumerate(request_data) if i not in not_validated_idx]
        existing_ids = validate_order_id(validated_data)
        if len(existing_ids) > 0:
            id_msg.append(existing_ids)
        result = {"validation_error": {'orders': id_msg}}
    else:
        existing_ids = validate_order_id(request_data)
        if len(existing_ids) > 0:
            status = 400
            result = {"validation_error": {'orders': existing_ids}}
        else:
            result = create_orders(request_data)
    return Response(json.dumps(result), status, mimetype='application/json')


@views.route("/orders/assign", methods=["POST"])
def assign():
    if not request.is_json:
        raise BadRequest('Content-Type must be application/json')
    
    request_data = request.get_json()
    err_msg = {}
    try:
        OrdersAssignSchema().load(request_data)
    except ValidationError as err:
        err_msg = err.messages
    if len(err_msg) != 0:
        return Response(status=400)
    courier_id = request_data['courier_id']
    if is_courier_id_exists(courier_id):
        result = assign_orders(courier_id)
        return Response(json.dumps(result), status, mimetype='application/json')
    else:
        return Response(status=400)


@views.route("/orders/complete", methods=["POST"])
def complete():
    if not request.is_json:
        raise BadRequest('Content-Type must be application/json')
    
    request_data = request.get_json()
    err_msg = {}
    try:
        OrderCompleteSchema().load(request_data)
    except ValidationError as err:
        err_msg = err.messages
    if len(err_msg) != 0:
        return Response(status=400)
    courier_id = request_data['courier_id']
    order_id = request_data['order_id']
    complete_time = request_data['complete_time']
    status, result = complete_order(courier_id=courier_id,
                                 order_id=order_id,
                                 complete_time=complete_time)
    return Response(json.dumps(result), status, mimetype='application/json')


