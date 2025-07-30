import json


class Serializer:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class TextSerializer(Serializer):
    def encode(self, data: str) -> bytes:
        return data.encode()


class JsonSerializer(Serializer):
    def encode(self, data) -> bytes:
        return json.dumps(data).encode()


class JsonlSerializer(Serializer):
    def encode(self, data) -> bytes:
        match data:
            case bytes():
                return data
            case str():
                return data.encode() + b"\n"
            case _:
                return json.dumps(data).encode() + b"\n"


class ParquetSerializer(Serializer):
    def encode(self, data) -> bytes:
        return json.dumps(data).encode() + b"\n"


def create_serializer(path, serializer):
    if isinstance(serializer, Serializer):
        return serializer

    serializer = serializer or {}
    suffixes = path.suffixes
    if ".json" in suffixes:
        return JsonSerializer(**serializer)
    elif ".jsonl" in suffixes:
        return JsonlSerializer(**serializer)
    elif ".parquet" in suffixes:
        return ParquetSerializer(**serializer)
    else:
        return TextSerializer()
