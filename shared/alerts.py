from django.urls import reverse_lazy

ALERT_CONFIGS = {
    "info": {
        "alert_type": "info",
        "icon": "fa-circle-info",
        "message": "This is an informational alert.",
        "hx_url": None,
        "button_text": None,
    },
    "checkpoint_fields": {
        "alert_type": "warning",
        "icon": "fa-triangle-exclamation",
        "message": "The checkpoint should contain at least one field. ",
        "hx_url": None,
        "button_text": "Add grade field",
    },
    "checkpoint_yeargroups": {
        "alert_type": "warning",
        "icon": "fa-triangle-exclamation",
        "message": "The checkpoint should target at least one year group.",
        "hx_url": None,
        "button_text": "Add year group",
    },
    "classes": {
        "alert_type": "warning",
        "icon": "fa-triangle-exclamation",
        "message": "There are no classes registered for this year group.",
        "hx_url": None,
        "button_text": None,
    },
    "student_programme": {
        "alert_type": "info",
        "icon": "fa-circle-info",
        "message": "This programme should comprise at least one qualification.",
        "button_text": "Add qualification",
    },
     "enrollment": {
        "alert_type": "info",
        "icon": "fa-triangle-exclamation",
        "message": "The student should be enrolled in at least one academic period.",
        "button_text": "Add enrollment",
    }
}


class Alert:
    def __init__(self, alert_key, custom_message=None, custom_hx_url=None, custom_button_text=None):
        config = ALERT_CONFIGS.get(alert_key, ALERT_CONFIGS["info"])  
        self.alert_type = config["alert_type"]
        self.icon = config["icon"]
        self.message = custom_message or config["message"]
        self.hx_url = custom_hx_url or config["hx_url"]
        self.button_text = custom_button_text or config["button_text"]

    def get_context(self):
        return {
            "type": self.alert_type,
            "icon": self.icon,
            "message": self.message,
            "hx_url": self.hx_url,
            "button_text": self.button_text,
        }


# def my_view(request):
#     alert = Alert("programme")  # Automatically loads config
#     alert.override(custom_message="Custom message for this alert")  # Override if needed
#     return render(request, "your_template.html", {"alert": alert.get_context()})

# {% include 'includes/alert.html' with type=alert.type icon=alert.icon message=alert.message hx_url=alert.hx_url button_text=alert.button_text %}
