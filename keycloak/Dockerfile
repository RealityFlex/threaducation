FROM keycloak/keycloak:18.0

# Копируем провайдеры и файл экспорта реалма
COPY keycloak/providers/. /opt/keycloak/providers/
COPY keycloak/realm-export.json /opt/jboss/keycloak/imports/

# Устанавливаем фиксированный ключ шифрования (AES_KEY)
ENV KC_CACHE=AES
ENV KC_CACHE_AES_KEY=your-fixed-encryption-key-here

# Собираем Keycloak
RUN /opt/keycloak/bin/kc.sh build