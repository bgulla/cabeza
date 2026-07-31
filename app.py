import html
import json
import os
from typing import Any

from flask import Flask, Response, request

app = Flask(__name__)


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, indent=2, sort_keys=True)
    return str(value)


def _render_dump() -> str:
    headers = sorted(request.headers, key=lambda h: h[0])
    query_params = {key: request.args.getlist(key) for key in sorted(request.args)}
    form_data = {key: request.form.getlist(key) for key in sorted(request.form)}
    cookies = {key: request.cookies.get(key) for key in sorted(request.cookies)}

    environ_keys = [
        key
        for key in sorted(request.environ)
        if key.startswith(("HTTP_", "CONTENT_", "REQUEST_", "QUERY_STRING", "REMOTE_ADDR", "PATH_INFO", "SCRIPT_NAME", "SERVER_", "RAW_URI", "wsgi.url_scheme"))
        and key not in {"wsgi.input", "wsgi.errors"}
    ]
    environ_values = [(key, request.environ.get(key)) for key in environ_keys]

    lines = [
        "CABEZA REQUEST DUMP",
        "===================",
        f"METHOD: {request.method}",
        f"PATH: {request.path}",
        f"FULL_PATH: {request.full_path}",
        f"BASE_URL: {request.base_url}",
        f"URL: {request.url}",
        f"REMOTE_ADDR: {request.remote_addr}",
        f"SCHEME: {request.scheme}",
        f"HOST: {request.host}",
        f"USER_AGENT: {request.headers.get('User-Agent', '')}",
        "",
        "HEADERS:",
        "-------",
    ]

    for name, value in headers:
        lines.append(f"{name}: {value}")

    lines.extend(["", "QUERY_PARAMS:", "------------"])
    for name, values in query_params.items():
        lines.append(f"{name}: {values}")

    lines.extend(["", "FORM_DATA:", "---------"])
    for name, values in form_data.items():
        lines.append(f"{name}: {values}")

    lines.extend(["", "COOKIES:", "-------"])
    for name, value in cookies.items():
        lines.append(f"{name}: {value}")

    lines.extend(["", "OTHER ENV:", "----------"])
    for name, value in environ_values:
        lines.append(f"{name}: {_safe_text(value)}")

    body = "\n".join(lines)
    escaped = html.escape(body)

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Request Dump</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{
      margin: 0;
      padding: 1.2rem;
      background: #000000;
      color: #00ff41;
      font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
      line-height: 1.45;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .banner {{
      margin-bottom: 1rem;
      color: #00ff41;
      font-weight: bold;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
  </style>
</head>
<body>
  <div class=\"banner\">CABEZA REQUEST DUMP</div>
  <pre>{escaped}</pre>
</body>
</html>
"""


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
def dump(path: str) -> Response:
    return Response(_render_dump(), mimetype="text/html; charset=utf-8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=False)
