import sys
from kv_store import KVStore


def handle_set(store: KVStore, line: str) -> None:
    parts = line.split(maxsplit=2)
    if len(parts) < 3:
        return

    _, key, value = parts
    store.set(key, value)


def handle_get(store: KVStore, line: str) -> None:
    parts = line.split(maxsplit=1)
    if len(parts) < 2:
        return

    _, key = parts
    value = store.get(key)

    if value is None:
        return

    print(value, flush=True)


def main() -> int:
    store = KVStore()

    while True:
        try:
            line = input().strip()
        except EOFError:
            break

        if not line:
            continue

        upper = line.upper()

        if upper == "EXIT":
            return 0

        if upper.startswith("SET "):
            handle_set(store, line)
            continue

        if upper.startswith("GET ") or upper == "GET":
            handle_get(store, line)
            continue

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
