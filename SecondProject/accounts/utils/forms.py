def clean_passwords(
    form, field1: str, field2: str, error_message: str = "Пароли не совпадают"
):
    cleaned_data = form.cleaned_data

    if getattr(form, "_errors", None):
        for fld in (field1, field2):
            form._errors.pop(fld, None)

    pwd1 = cleaned_data.get(field1)
    pwd2 = cleaned_data.get(field2)

    if pwd1 and pwd2 and pwd1 != pwd2:
        form.add_error(field2, error_message)

    return cleaned_data
