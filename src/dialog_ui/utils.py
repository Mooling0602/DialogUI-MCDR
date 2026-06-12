import json

from mcdreforged.api.all import PluginServerInterface, RTextMCDRTranslation


def extract_file(server: PluginServerInterface, file_path: str, target_path: str):
    """Extract a file from the plugin's bundled resources to a target location.

    :param server: The plugin server interface.
    :param file_path: The path to the file in the bundled resources.
    :param target_path: The path to the target location.
    """
    with (
        server.open_bundled_file(file_path) as file_handler,
        open(target_path, "wb") as target_file,
    ):
        target_file.write(file_handler.read())


def tr(
    server: PluginServerInterface, tr_key: str, return_str: bool = False, *args
) -> str | RTextMCDRTranslation:
    """Optimized method for using `PluginServerInterface.rtr()` provided by MCDR.

    :param server: A `PluginServerInterface()` instance, will be used to use MCDR interfaces and get the plugin id.
    :param tr_key: Translation key string.
    :param return_str: If returns a `str` object as result.
    :param *args: Used for template strings.

    :return: A `str` object or a `RTextMCDRTranslation` instance.
    """
    plg_id = server.get_self_metadata().id
    if tr_key.startswith(f"{plg_id}"):
        translation = server.rtr(f"{tr_key}")
    else:
        if tr_key.startswith("#"):
            translation = server.rtr(tr_key.replace("#", ""), *args)
        else:
            translation = server.rtr(f"{plg_id}.{tr_key}", *args)
    if return_str:
        tr_to_str: str = str(translation)
        return tr_to_str
    else:
        return translation


def tr_to_str(server: PluginServerInterface, tr_key: str, *args) -> str:
    """Call `tr()` and require a :class:`str` output."""
    return str(tr(server, tr_key, True, *args))


def tr_to_rtr(
    server: PluginServerInterface, tr_key: str, *args
) -> RTextMCDRTranslation:
    """Call `tr()` and require a :class:`RTextMCDRTranslation` instance."""
    rtr = tr(server, tr_key, False, *args)
    assert isinstance(rtr, RTextMCDRTranslation)
    return rtr


def dict_to_json_str(data: dict, **kwargs) -> str:
    """Serialize a dict to a JSON string.

    :param data: The dict to serialize.
    :param kwargs: Extra arguments passed to :func:`json.dumps`.
    :return: The JSON string.
    """
    return json.dumps(data, **kwargs)


def json_str_to_dict(json_str: str, **kwargs) -> dict:
    """Deserialize a JSON string to a dict.

    :param json_str: The JSON string to parse.
    :param kwargs: Extra arguments passed to :func:`json.loads`.
    :return: The parsed dict.
    """
    return json.loads(json_str, **kwargs)


def _detect_encoding(
    file_path: str, encodings: tuple[str, ...] = ("utf-8", "gbk")
) -> str:
    """Try to detect the encoding of a text file.

    :param file_path: Path to the file.
    :param encodings: Encodings to try, in order.
    :return: The first working encoding.
    :raises ValueError: If no encoding works.
    """
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                f.read()
            return enc
        except (UnicodeDecodeError, LookupError):
            continue
    raise ValueError(f"Cannot detect encoding for {file_path}, tried: {encodings}")


def dict_to_json_file(
    data: dict, file_path: str, encoding: str = "utf-8", **kwargs
) -> None:
    """Write a dict to a JSON file.

    :param data: The dict to serialize.
    :param file_path: Path to the output JSON file.
    :param encoding: Encoding for the output file, default utf-8.
    :param kwargs: Extra arguments passed to :func:`json.dump`.
    """
    with open(file_path, "w", encoding=encoding) as f:
        json.dump(data, f, **kwargs)


def json_file_to_dict(file_path: str, encoding: str | None = None, **kwargs) -> dict:
    """Read a JSON file and deserialize it to a dict.

    :param file_path: Path to the JSON file.
    :param encoding: File encoding. If None, auto-detect (utf-8 then gbk).
    :param kwargs: Extra arguments passed to :func:`json.load`.
    :return: The parsed dict.
    """
    if encoding is None:
        encoding = _detect_encoding(file_path)
    with open(file_path, "r", encoding=encoding) as f:
        return json.load(f, **kwargs)
