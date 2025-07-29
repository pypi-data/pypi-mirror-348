from typing_extensions import TypedDict


class SlackProfile(TypedDict):
    real_name: str
    real_name_normalized: str
    display_name: str
    display_name_normalized: str
    status_text: str
    status_emoji: str
    email: str
    image_24: str
    image_32: str
    image_48: str
    image_72: str
    image_192: str
    image_512: str
    is_bot: bool
