# Set the base image to the base image
FROM hmlandregistry/dev_base_python_flask:3

ENV APP_NAME="mint-api" \
    SOR_URL="http://register:8080" \
    IDENTIFIER_KEY="local-land-charge" \
    PRIVATE_KEY="certs/test_private.pem" \
    PUBLIC_KEY="certs/test_public.pem" \
    PRIVATE_PASSPHRASE="thisisaprivatepassphrase" \
    PUBLIC_PASSPHRASE="thisisapublicpassphrase" \
    SECRET_KEY="thisisasecretkey" \
    SQL_HOST=postgres \
    SQL_DATABASE=mint_api_db \
    ALEMBIC_SQL_USERNAME=alembic_user \
    SQL_USE_ALEMBIC_USER=no \
    APP_SQL_USERNAME=mint_api_db_user \
    SQL_PASSWORD=password \
    MAX_HEALTH_CASCADE=6 \
    AUTHENTICATION_API_URL="http://authentication-api:8080/v2.0" \
    AUTHENTICATION_API_ROOT="http://authentication-api:8080" \
    SQLALCHEMY_POOL_RECYCLE="3300"

# The command to run the app is inherited from lr_base_python_flask
ADD requirements_test.txt requirements_test.txt
ADD requirements.txt requirements.txt
RUN yum install -y postgresql-devel
RUN pip3 install -q -r requirements.txt && \
  pip3 install -q -r requirements_test.txt
