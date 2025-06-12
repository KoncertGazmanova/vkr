from django.conf import settings


def get_client_ip(request_like):
    """Извлекает IP из request, учитывая X-Forwarded-For."""
    xff = getattr(request_like, "META", {}).get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return getattr(request_like, "META", {}).get("REMOTE_ADDR")
