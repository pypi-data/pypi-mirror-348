class Bencode:
    @staticmethod
    def encode(data):
        if isinstance(data, int):
            return Bencode.encode_int(data)
        elif isinstance(data, str):
            return Bencode.encode_str(data)
        elif isinstance(data, list):
            return Bencode.encode_list(data)
        elif isinstance(data, dict):
            return Bencode.encode_dict(data)
        else:
            raise TypeError(f"Unsupported type: {type(data)}")

    @staticmethod
    def encode_int(data):
        return f"i{data}e".encode('utf-8')

    @staticmethod
    def encode_str(data):
        return f"{len(data.encode('utf-8'))}:{data}".encode('utf-8')

    @staticmethod
    def encode_list(data):
        return b'l' + b''.join(Bencode.encode(item) for item in data) + b'e'

    @staticmethod
    def encode_dict(data):
        encoded_items = []
        for key, value in sorted(data.items()):
            encoded_items.append(Bencode.encode(key))
            encoded_items.append(Bencode.encode(value))
        return b'd' + b''.join(encoded_items) + b'e'

    @staticmethod
    def decode(data):
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return Bencode._decode_next(data, 0)
        # return value

    @staticmethod
    def _decode_next(data, index):
        if data[index] == 'i':
            return Bencode._decode_int(data, index)
        elif data[index].isdigit():
            return Bencode._decode_str(data, index)
        elif data[index] == 'l':
            return Bencode._decode_list(data, index)
        elif data[index] == 'd':
            return Bencode._decode_dict(data, index)
        else:
            raise ValueError(f"Invalid bencode data at index {index}")

    @staticmethod
    def _decode_int(data, index):
        end_index = data.index('e', index)
        number = int(data[index + 1:end_index])
        return end_index + 1, number

    @staticmethod
    def _decode_str(data, index):
        colon_index = data.index(':', index)
        length = int(data[index:colon_index])
        start = colon_index + 1
        end = start + length
        string = data[start:end]
        if(len(string) > length): return None, None
        return end, string

    @staticmethod
    def _decode_list(data, index):
        index += 1
        items = []
        while data[index] != 'e':
            index, item = Bencode._decode_next(data, index)
            items.append(item)
        return index + 1, items

    @staticmethod
    def _decode_dict(data, index):
        index += 1
        items = {}
        while data[index] != 'e':
            index, key = Bencode._decode_next(data, index)
            index, value = Bencode._decode_next(data, index)
            items[key] = value
            if index >= len(data): return None, None
        return index + 1, items
