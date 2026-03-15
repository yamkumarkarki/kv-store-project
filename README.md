# Persistent Key-Value Store

A simple append-only key-value store written in Python.

## Features
- `SET <key> <value>`
- `GET <key>`
- `EXIT`
- Persistent append-only storage in `data.db`
- In-memory index implemented with a custom linked list
- No built-in dictionary/map used for the key-value index
- Last write wins
- Replays the log on startup

## How to run
```bash
python3 main.py
```

## Example session
```text
SET name Yam
GET name
Yam
GET missing
NULL
EXIT
```

## Black-box testing behavior
- `SET` produces no output
- `GET <existing-key>` prints the value
- `GET <missing-key>` prints `NULL`
- `EXIT` cleanly terminates the program

## Notes
- Values may contain spaces because `SET` splits only the first two spaces.
- Each write is flushed and fsynced immediately.
- On startup, malformed partial log lines are ignored.

## Suggested Git steps
```bash
git init
git add .
git commit -m "Initial persistent KV store"
git tag project
```
