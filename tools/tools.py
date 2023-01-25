import hashlib
import json
import os.path


def get_file_md5(fname: str) -> str:
    m = hashlib.md5()  # 创建md5对象
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象


def dict_to_json_bytes(vari: dict) -> bytes:
    jsonStr = json.dumps(vari)
    return jsonStr.encode()


def json_bytes_to_dict(vari: bytes) -> dict:
    jsonStr = vari.decode()
    return json.loads(jsonStr)


def have_file(path: str) -> bool:
    return os.path.exists(path)


def create_json_file(path: str, filename: str):
    voidJSON = json.dumps({})
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as fp:
        fp.write(voidJSON)


def clean_json_file(path: str):
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(json.dumps({}))


def write_json_file(path: str, data: dict):
    clean_json_file(path)
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(data, ensure_ascii=False, indent=4))


def read_json_file(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as fp:
        return json.load(fp)

