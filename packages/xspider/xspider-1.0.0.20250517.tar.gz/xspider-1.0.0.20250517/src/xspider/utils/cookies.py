def list_dict_to_str(cookies_list_dict: list[dict[str, str]]) -> str:
    """将 cookies 的列表字典格式转换为字符串格式"""
    return "; ".join([c["name"] + "=" + c["value"] for c in cookies_list_dict])


def str_to_dict(cookies_str: str) -> dict[str, str]:
    """将 cookies 的字符串格式转换为字典格式"""
    return {c.split("=", maxsplit=1)[0].strip(): c.split("=", maxsplit=1)[-1].strip() for c in cookies_str.split(";")}


def dict_to_str(cookies_dict: dict[str, str]) -> str:
    """将 cookies 的字典格式转换为字符串格式"""
    return "; ".join([k + "=" + v for k, v in cookies_dict.items()])
