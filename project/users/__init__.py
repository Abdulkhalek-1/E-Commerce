from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        import project.users.signals  # noqa: F401
