# -*- coding: utf-8 -*-

class StoreSchema:

    order_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "petId": {"type": "integer"},
            "quantity": {"type": "integer"},
            "shipDate": {"type": "string"},
            "status": {"type": "string", "enum": ["placed", "approved", "delivered"]},
            "complete": {"type": "boolean"}
        }
    }

    inventory_schema = {
        "type": "object",
        "properties": {
            "approved": {"type": "integer"},
            "placed": {"type": "integer"},
            "delivered": {"type": "integer"}},
    }
