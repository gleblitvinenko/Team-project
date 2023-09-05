def item_detail_info(*args, **kwargs) -> str:
    item_details = f"""
    ℹ️ Item Title: {kwargs.get("title")}

    🆔 ID: {kwargs.get("id")}

    💰 Price: {kwargs.get("price")}
    """
    return item_details
