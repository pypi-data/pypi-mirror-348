# Maji Package
Library for client side passport functionality.
Adding new auth backend behaviour.
Working with passport tokens.
Adding new endpoints.

# Update library
https://pypi.org/project/maji-passport/

* Login to pypi via techoutlaw account.
* https://pypi.org/manage/account/ - API tokens. Generate new API to update library.
* Update the version of the library in 2 files (setup.py and pyproject.toml)
* Generate new binary files: ```python setup.py sdist bdist_wheel```
* Publish new binaries from dist folder: ```twine upload --repository pypi dist/*```
* Update requirements on Brandon\Argo\etc

# Installation
    1. Instal thru pip
    2. Add package maji_passport at LOCAL_APPS (django) https://pypi.org/project/maji-passport/
    3. Add settings for your apllication
        a. "maji_passport.apps.PassportConfig" into INSTALLED_APPS
        b. "maji_passport.authentication.backend.PassportAuthBackend" add into DEFAULT_AUTHENTICATION_CLASSES
        c. new envoronment variables ( Look it below )
        d. develop your own tasks or move existed to argo/passport/tasks.py
        e. overwrite 2 functions 
            * maji_passport.services.kafka.KafkaService = KafkaService
            * maji_passport.KafkaUpdateUserSerializer = KafkaUpdateUserSerializer

        f. add new routes:
            path("api/auth/", include("maji_passport.urls")),
        g. Put logic for auth backend env variable APPLICATION_AUTHENTICATION if it needs
        h. Put logic for user serializer env variable USER_DETAIL_SERIALIZER if it needs


# Env veriables
### PASSPORT SETTINGS
```
PASSPORT_ENABLE = env("PASSPORT_ENABLE", default=True)
PASSPORT_SERVICE_KEY = env("PASSPORT_SERVICE_KEY", default="")
PASSPORT_UPDATE_TOKEN_URL = env(
    "PASSPORT_UPDATE_TOKEN_URL",
    default="https://test.com/api/v1/internal_auth/auth/update_token/",
)

PASSPORT_START_MIGRATE = env("PASSPORT_START_MIGRATE", default="")
PASSPORT_SET_PASSWORD = env("PASSPORT_SET_PASSWORD", default="")
PASSPORT_LOGIN_URL = env(
    "PASSPORT_LOGIN_URL", default="https://test.com/auth/login"
)
PASSPORT_KAFKA_INTERNAL_SERVER_TOPIC = env(
    "PASSPORT_KAFKA_INTERNAL_SERVER_TOPIC", default="internalServerTopic"
)
PASSPORT_EXCHANGE_KEY = env("PASSPORT_EXCHANGE_KEY", default="")
PASSPORT_PUBLIC_KEY_PATH = env(
    "PASSPORT_PUBLIC_KEY_PATH", default="secrets/rsa_keys/public.pem"
)
APPLICATION_AUTHENTICATION = None
USER_DETAIL_SERIALIZER = None
```

### KAFKA
```
KAFKA_SASL_PASSWORD = env("KAFKA_SASL_PASSWORD", default="")
KAFKA_SASL_USERNAME = env("KAFKA_SASL_USERNAME", default="")
KAFKA_BOOTSTRAP_SERVER = env("KAFKA_BOOTSTRAP_SERVER", default="")
KAFKA_SECURITY_PROTOCOL = env("KAFKA_SECURITY_PROTOCOL", default="SASL_SSL")
KAFKA_SASL_MECHANISM = env("KAFKA_SASL_MECHANISM", default="PLAIN")
KAFKA_SESSION_TIMEOUT_MS = env("KAFKA_SESSION_TIMEOUT_MS", default=45000)
KAFKA_GROUP_ID = env("KAFKA_GROUP_ID", default="argo_test_passport_group")
```
            

    

