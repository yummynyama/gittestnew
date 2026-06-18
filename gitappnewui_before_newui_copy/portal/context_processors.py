"""Передаёт настройки из exam_config.py во все шаблоны."""
import exam_config


def exam_settings(request):
    # Не трогаем шаблоны Django Admin — меньше конфликтов
    if request.path.startswith("/django-admin/"):
        return {}
    return {
        "site_name": exam_config.SITE_NAME,
        "site_tagline": exam_config.SITE_TAGLINE,
        "btn_create_user": exam_config.BTN_CREATE_USER,
        "btn_register": exam_config.BTN_REGISTER,
        "btn_login": exam_config.BTN_LOGIN,
        "btn_send_application": exam_config.BTN_SEND_APPLICATION,
        "link_to_register": exam_config.LINK_TO_REGISTER,
        "link_to_login": exam_config.LINK_TO_LOGIN,
        "slider_interval": exam_config.SLIDER_INTERVAL_MS,
    }
