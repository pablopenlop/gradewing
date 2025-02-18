from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator

def limits_from_validators(model_field):
    min_value = max_value = None
    for validator in model_field.validators:
        if isinstance(validator, MinValueValidator):
            min_value = validator.limit_value
        elif isinstance(validator, MaxValueValidator):
            max_value = validator.limit_value
        elif isinstance(validator, MaxLengthValidator):
            max_value = validator.limit_value
    return min_value, max_value

def widget_limits_from_validators(form_instance, field_name):
    model_field = form_instance._meta.model._meta.get_field(field_name)
    min_value, max_value = limits_from_validators(model_field)
    if min_value is not None:
        form_instance.fields[field_name].widget.attrs.update({'min': min_value})
    if max_value is not None:
        form_instance.fields[field_name].widget.attrs.update({'max': max_value})

def helptext_from_validators(form_instance, field_name):
    model_field = form_instance._meta.model._meta.get_field(field_name)
    min_value, max_value = limits_from_validators(model_field)
    if min_value is not None and max_value is not None:
        form_instance.fields[field_name].help_text = f"{min_value} – {max_value}"
    elif min_value is not None:
        form_instance.fields[field_name].help_text =  f"Min. value: {min_value}"
    elif max_value is not None:
        form_instance.fields[field_name].help_text =  f"Max. value: {max_value}"
    else:
        form_instance.fields[field_name].help_text = None

