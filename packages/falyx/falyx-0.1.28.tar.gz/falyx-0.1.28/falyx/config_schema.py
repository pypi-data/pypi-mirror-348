FALYX_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Falyx CLI Config",
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Title shown at top of menu"},
        "prompt": {
            "oneOf": [
                {"type": "string"},
                {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "prefixItems": [
                            {
                                "type": "string",
                                "description": "Style string (e.g., 'bold #ff0000 italic')",
                            },
                            {"type": "string", "description": "Text content"},
                        ],
                        "minItems": 2,
                        "maxItems": 2,
                    },
                },
            ]
        },
        "columns": {
            "type": "integer",
            "minimum": 1,
            "description": "Number of menu columns",
        },
        "welcome_message": {"type": "string"},
        "exit_message": {"type": "string"},
        "commands": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["key", "description", "action"],
                "properties": {
                    "key": {"type": "string", "minLength": 1},
                    "description": {"type": "string"},
                    "action": {
                        "type": "string",
                        "pattern": "^[a-zA-Z_][a-zA-Z0-9_]*(\\.[a-zA-Z_][a-zA-Z0-9_]*)+$",
                        "description": "Dotted import path (e.g., mymodule.task)",
                    },
                    "args": {"type": "array"},
                    "kwargs": {"type": "object"},
                    "aliases": {"type": "array", "items": {"type": "string"}},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "style": {"type": "string"},
                    "confirm": {"type": "boolean"},
                    "confirm_message": {"type": "string"},
                    "preview_before_confirm": {"type": "boolean"},
                    "spinner": {"type": "boolean"},
                    "spinner_message": {"type": "string"},
                    "spinner_type": {"type": "string"},
                    "spinner_style": {"type": "string"},
                    "logging_hooks": {"type": "boolean"},
                    "retry": {"type": "boolean"},
                    "retry_all": {"type": "boolean"},
                    "retry_policy": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "max_retries": {"type": "integer"},
                            "delay": {"type": "number"},
                            "backoff": {"type": "number"},
                        },
                    },
                },
            },
        },
    },
    "required": ["commands"],
}
