# Claude Test - FastAPI Hello World

A simple REST API built with [FastAPI](https://fastapi.tiangolo.com/).

## What is FastAPI?

FastAPI is a modern, high-performance Python web framework for building APIs. It is built on top of Starlette (for the web layer) and Pydantic (for data validation). Key features include:

- Automatic interactive API documentation (Swagger UI at `/docs`)
- High performance, on par with Node.js and Go
- Type hints and automatic request/response validation
- Async support out of the box

## What This Project Does

This project exposes two endpoints:

- **`GET /hello`** — Returns `{"message": "Hello World"}`
- **`GET /{anything}`** — Echoes back whatever path you send, e.g. `GET /foo` returns `{"message": "foo"}`

## Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn main:app --reload
```

### Test it

```bash
curl http://localhost:8000/hello
# {"message":"Hello World"}

curl http://localhost:8000/goodbye
# {"message":"goodbye"}
```

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).
