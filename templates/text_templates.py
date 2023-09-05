def item_detail_info(*args, **kwargs) -> str:
    item_details = f"""
    ℹ️ Item Title: {kwargs.get("title")}

    🆔 ID: {kwargs.get("id")}

    💰 Price: {kwargs.get("price")}
    """
    return item_details
 
 
profile_inline = "📁 Profile"
item_categories_inline = "🗄️ Item categories"
faq_inline = "❓ FAQ"
add_change_first_name_inline = "First name"
add_change_last_name_inline = "Last name"
add_change_phone_number_inline = "Phone number"
share_phone_number_inline = "Share phone number 📱"
