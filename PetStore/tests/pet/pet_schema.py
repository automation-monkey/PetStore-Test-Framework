# -*- coding: utf-8 -*-

pet_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "category": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}},
        "photoUrls": {"type": "array", "items": {"type": "string"}},
        "tags": {"type": "array", "items": {"type": "object"}, "properties": {"id": {"type": "integer"},
                                                                              "name": {"type": "string"}}},
        "status": {"type": "string", "enum": ["available", "pending", "sold"]}
    }
}
