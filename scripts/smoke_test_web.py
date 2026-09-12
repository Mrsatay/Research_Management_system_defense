from __future__ import annotations

import http.cookiejar
import io
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def request(
    opener: urllib.request.OpenerDirector,
    path: str,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, str, dict[str, str]]:
    request_object = urllib.request.Request(
        BASE_URL + path,
        data=data,
        headers=headers or {},
        method=method,
    )
    with opener.open(request_object) as response:
        return response.status, response.read().decode("utf-8"), dict(response.headers)


def form_data(values: dict[str, str]) -> bytes:
    return urllib.parse.urlencode(values).encode("utf-8")


def multipart_data(
    field_name: str,
    filename: str,
    content: bytes,
) -> tuple[bytes, str]:
    boundary = "----ResearchPaperManagerSmokeBoundary"
    body = io.BytesIO()
    body.write(f"--{boundary}\r\n".encode())
    body.write(
        (
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{filename}"\r\n'
        ).encode()
    )
    body.write(b"Content-Type: text/csv\r\n\r\n")
    body.write(content)
    body.write(f"\r\n--{boundary}--\r\n".encode())
    return body.getvalue(), f"multipart/form-data; boundary={boundary}"


def main() -> None:
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar)
    )

    status, login_html, _ = request(opener, "/login")
    assert status == 200 and "Sign in to continue" in login_html

    status, _, headers = request(
        opener,
        "/login",
        method="POST",
        data=form_data({"username": "admin", "password": "admin123"}),
    )
    assert status == 200 and headers.get("Content-Location") is None

    status, dashboard_html, _ = request(opener, "/")
    assert status == 200 and "Research paper records" in dashboard_html

    record = {
        "paper_id": "WEB-SMOKE-001",
        "title": "Web Smoke Test Paper",
        "authors": "Web Test Author",
        "institution": "Research Management Lab",
        "publication": "Web Verification Journal",
        "publication_date": "2024-07-01",
        "abstract": "Temporary record used to verify web routes.",
        "keywords": "web; smoke test",
    }
    request(opener, "/papers/WEB-SMOKE-001/delete", method="POST")
    status, _, _ = request(
        opener,
        "/papers/new",
        method="POST",
        data=form_data(record),
    )
    assert status == 200

    status, search_html, _ = request(opener, "/?q=Web+Smoke")
    assert status == 200 and "Web Smoke Test Paper" in search_html

    updated_record = {**record, "title": "Updated Web Smoke Test Paper"}
    status, _, _ = request(
        opener,
        "/papers/WEB-SMOKE-001/edit",
        method="POST",
        data=form_data({key: value for key, value in updated_record.items() if key != "paper_id"}),
    )
    assert status == 200

    status, statistics_html, _ = request(opener, "/statistics")
    assert status == 200 and "Web Verification Journal" in statistics_html

    status, export_text, export_headers = request(opener, "/papers/export")
    assert status == 200 and "WEB-SMOKE-001" in export_text
    content_disposition = next(
        (
            value
            for key, value in export_headers.items()
            if key.lower() == "content-disposition"
        ),
        "",
    )
    assert "attachment" in content_disposition

    sample = (ROOT / "data" / "sample_papers.csv").read_bytes()
    body, content_type = multipart_data("file", "sample_papers.csv", sample)
    status, import_html, _ = request(
        opener,
        "/papers/import",
        method="POST",
        data=body,
        headers={"Content-Type": content_type},
    )
    assert status == 200 and "imported" in import_html.lower()

    status, _, _ = request(opener, "/papers/WEB-SMOKE-001/delete", method="POST")
    assert status == 200
    status, final_html, _ = request(opener, "/")
    assert status == 200 and "Updated Web Smoke Test Paper" not in final_html
    for paper_id in ("P-001", "P-002", "P-003"):
        status, _, _ = request(opener, f"/papers/{paper_id}/delete", method="POST")
        assert status == 200

    print("Web smoke test passed: login, CRUD, search, statistics, import, and export.")


if __name__ == "__main__":
    main()
