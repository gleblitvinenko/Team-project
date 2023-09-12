import datetime

from managers.user import User


def item_detail_info(*args, **kwargs) -> str:
    item_details = f"""
ℹ️ Item Title: {kwargs.get("title")}

🆔 ID: {kwargs.get("id")}

💰 Price: {kwargs.get("price")}
"""
    return item_details


def show_profile_info(telegram_id: int) -> str:
    user_manager = User()
    profile_info_dict = user_manager.get_info_for_profile(telegram_id=telegram_id)

    profile_info_message = f"""
🧬 Your profile:

{add_change_first_name_inline}: {profile_info_dict.get("first_name")}

{add_change_last_name_inline}: {profile_info_dict.get("last_name")}

{add_change_phone_number_inline}: {profile_info_dict.get("phone_number")}

{registration_date}: {datetime.datetime.strptime(profile_info_dict.get("reg_date"), "%Y-%m-%d").strftime("%d.%m.%Y")}
    """

    return profile_info_message


add_change_first_name_inline = "👤 First name"
add_change_last_name_inline = "📝 Last name"
add_change_phone_number_inline = "📱 Phone number"
registration_date = "📅 Registration date"
share_phone_number_button = "📱 Share phone number"

menu_names_dict = {
    "item_categories": "🏷️ Item categories",
    "profile": "📁 Profile",
    "cart": "🛒 Cart",
    "orders": "📦 Orders",
    "faq": "❓ FAQ",
}


def get_cart_text(items: list[dict]) -> str:
    cart_text = f"{menu_names_dict.get('cart')}\n\n"
    total_cart_price = 0
    for item_dict in items:
        item_cost = item_dict.get("price") * item_dict.get("quantity")
        cart_text += get_single_cart_item_text(item=item_dict)
        total_cart_price += item_cost

    cart_text += f"To pay {total_cart_price:.2f} UAH"
    return cart_text


def get_single_cart_item_text(item: dict) -> str:
    return f"📌 {item.get('title')} {item.get('price'):.2f} UAH ✖ {item.get('quantity')}  🟰 {(item.get('price') * item.get('quantity')):.2f} UAH \n\n"
