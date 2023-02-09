def format_rich_text(value):
    if not value or not value["ops"]:
        return None

    return "".join([item["insert"] for item in value["ops"]]).strip()
