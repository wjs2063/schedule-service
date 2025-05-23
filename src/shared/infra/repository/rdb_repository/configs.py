

RDB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": "postgres",
                "host": "localhost",
                "port": 8080,
                "user": "postgres",
                "password": "postgres"
            }
        }
        # "token": {
        #     "engine": "tortoise.backends.asyncpg",
        #     "credentials": {
        #         "database": "token",
        #         "host": "localhost",
        #         "port": 5432,
        #         "user": "postgres",
        #         "password": "postgres"
        #     }
        # }
    },
    "apps": {
        "models": {
            "models": ["src.auth.domain.user.model"],
            "default_connection": "default"
        },
        # "token_models": {
        #     "models": ["app.models.audit_model"],
        #     "default_connection": "token"
        # }
    }
}
