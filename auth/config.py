class Settings:
    # Database
    DATABASE_URL = "postgresql://threaducation_user:threads_t0_masses@postgres:5432/education_db"
    
    # Auth settings
    CLIENT_ID = "auth_client"  # Replace with your actual client ID
    CLIENT_SECRET = "vQkfDyPGu5nRhuOEgkUuvWHbqplfZND5"  # Replace with your actual client secret
    KEYCLOAK_URL = "http://keycloak:8080/realms/xd/protocol/openid-connect/token"  # Replace with your actual Keycloak URL

settings = Settings()