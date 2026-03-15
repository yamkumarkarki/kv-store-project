import os
from typing import Optional

DB_FILE = "data.db"
NOT_FOUND = "NULL"


def escape_field(text: str) -> str:
    """Escape tabs, newlines, and backslashes for safe log storage."""
    return (
        text.replace("\\", "\\\\")
        .replace("\t", "\\t")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )


def unescape_field(text: str) -> str:
    """Reverse the escaping applied before values were written to disk."""
    result = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and i + 1 < len(text):
            nxt = text[i + 1]
            if nxt == "t":
                result.append("\t")
            elif nxt == "n":
                result.append("\n")
            elif nxt == "r":
                result.append("\r")
            elif nxt == "\\":
                result.append("\\")
            else:
                result.append(nxt)
            i += 2
        else:
            result.append(ch)
            i += 1
    return "".join(result)


class Node:
    """A single node in a linked-list index."""

    def __init__(self, key: str, value: str, next_node: Optional["Node"] = None) -> None:
        self.key = key
        self.value = value
        self.next = next_node


class LinkedListIndex:
    """A simple in-memory index without using dict/map types."""

    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def set(self, key: str, value: str) -> None:
        current = self.head
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next

        self.head = Node(key, value, self.head)

    def get(self, key: str) -> Optional[str]:
        current = self.head
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None


class KVStore:
    def __init__(self, db_path: str = DB_FILE) -> None:
        self.db_path = db_path
        self.index = LinkedListIndex()
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Replay the append-only log to rebuild the in-memory index."""
        if not os.path.exists(self.db_path):
            return

        with open(self.db_path, "r", encoding="utf-8") as db_file:
            for raw_line in db_file:
                line = raw_line.rstrip("\n")
                if not line:
                    continue

                parts = line.split("\t", 2)
                if len(parts) != 3:
                    # Ignore partial/corrupt trailing lines from interrupted writes.
                    continue

                command, key, value = parts
                if command != "SET":
                    continue

                self.index.set(unescape_field(key), unescape_field(value))

    def set(self, key: str, value: str) -> None:
        """Append the write to disk, flush immediately, then update memory."""
        record = f"SET\t{escape_field(key)}\t{escape_field(value)}\n"
        with open(self.db_path, "a", encoding="utf-8") as db_file:
            db_file.write(record)
            db_file.flush()
            os.fsync(db_file.fileno())

        self.index.set(key, value)

    def get(self, key: str) -> Optional[str]:
        return self.index.get(key)
