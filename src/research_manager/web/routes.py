from __future__ import annotations

import csv
import io
from datetime import date

from fastapi import File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse

from ..services.auth_service import AuthService
from ..services.paper_service import (
    PAPER_FIELDS,
    DuplicatePaperError,
    PaperService,
    PaperValidationError,
)
from .app import app, templates
from .security import current_username, is_authenticated

auth_service = AuthService()
paper_service = PaperService()


def redirect(path: str) -> RedirectResponse:
    return RedirectResponse(path, status_code=303)


def require_login(request: Request) -> RedirectResponse | None:
    if not is_authenticated(request):
        return redirect("/login")
    return None


def template_context(request: Request, **values: object) -> dict:
    return {
        "request": request,
        "username": current_username(request),
        "today": date.today().isoformat(),
        **values,
    }


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if is_authenticated(request):
        return redirect("/")
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=template_context(request, error=None),
    )


@app.post("/login", response_class=HTMLResponse)
def login_action(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
):
    if auth_service.authenticate(username, password):
        request.session["username"] = username.strip()
        return redirect("/")
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=template_context(request, error="Invalid username or password."),
        status_code=401,
    )


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return redirect("/login")


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, q: str = "", sort: str = "newest"):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    descending = sort != "oldest"
    papers = paper_service.list_papers(q, descending=descending)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=template_context(
            request,
            papers=papers,
            query=q,
            sort=sort,
            descending=descending,
            paper_count=len(papers),
        ),
    )


def paper_form_data(
    paper_id: str,
    title: str,
    authors: str,
    institution: str,
    publication: str,
    publication_date: str,
    abstract: str,
    keywords: str,
) -> dict[str, str]:
    return {
        "paper_id": paper_id,
        "title": title,
        "authors": authors,
        "institution": institution,
        "publication": publication,
        "publication_date": publication_date,
        "abstract": abstract,
        "keywords": keywords,
    }


@app.get("/papers/new", response_class=HTMLResponse)
def new_paper_page(request: Request):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    return templates.TemplateResponse(
        request=request,
        name="paper_form.html",
        context=template_context(request, paper=None, form_data={}, error=None),
    )


@app.post("/papers/new", response_class=HTMLResponse)
def create_paper(
    request: Request,
    paper_id: str = Form(""),
    title: str = Form(""),
    authors: str = Form(""),
    institution: str = Form(""),
    publication: str = Form(""),
    publication_date: str = Form(""),
    abstract: str = Form(""),
    keywords: str = Form(""),
):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    form_data = paper_form_data(
        paper_id,
        title,
        authors,
        institution,
        publication,
        publication_date,
        abstract,
        keywords,
    )
    try:
        paper_service.add_paper(form_data)
    except (PaperValidationError, DuplicatePaperError) as exc:
        return templates.TemplateResponse(
            request=request,
            name="paper_form.html",
            context=template_context(request, paper=None, form_data=form_data, error=str(exc)),
            status_code=400,
        )
    return redirect("/")


@app.get("/papers/{paper_id}/edit", response_class=HTMLResponse)
def edit_paper_page(request: Request, paper_id: str):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    paper = paper_service.get_by_id(paper_id)
    if paper is None:
        return redirect("/")
    return templates.TemplateResponse(
        request=request,
        name="paper_form.html",
        context=template_context(request, paper=paper, form_data={}, error=None),
    )


@app.post("/papers/{paper_id}/edit", response_class=HTMLResponse)
def update_paper(
    request: Request,
    paper_id: str,
    title: str = Form(""),
    authors: str = Form(""),
    institution: str = Form(""),
    publication: str = Form(""),
    publication_date: str = Form(""),
    abstract: str = Form(""),
    keywords: str = Form(""),
):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    paper = paper_service.get_by_id(paper_id)
    if paper is None:
        return redirect("/")
    form_data = paper_form_data(
        paper_id,
        title,
        authors,
        institution,
        publication,
        publication_date,
        abstract,
        keywords,
    )
    try:
        paper_service.update_paper(paper.id, form_data)
    except (PaperValidationError, DuplicatePaperError) as exc:
        return templates.TemplateResponse(
            request=request,
            name="paper_form.html",
            context=template_context(request, paper=paper, form_data=form_data, error=str(exc)),
            status_code=400,
        )
    return redirect("/")


@app.post("/papers/{paper_id}/delete")
def delete_paper(request: Request, paper_id: str):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    paper = paper_service.get_by_id(paper_id)
    if paper:
        paper_service.delete_papers([paper.id])
    return redirect("/")


@app.get("/statistics", response_class=HTMLResponse)
def statistics(request: Request):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    return templates.TemplateResponse(
        request=request,
        name="statistics.html",
        context=template_context(
            request,
            counts=paper_service.count_by_publication(),
            total=len(paper_service.list_papers(descending=False)),
        ),
    )


@app.get("/papers/import", response_class=HTMLResponse)
def import_page(request: Request):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    return templates.TemplateResponse(
        request=request,
        name="import.html",
        context=template_context(request, result=None),
    )


@app.post("/papers/import", response_class=HTMLResponse)
async def import_action(request: Request, file: UploadFile = File(...)):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    content = await file.read()
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    imported = 0
    errors: list[str] = []
    missing_headers = [
        field for field in PAPER_FIELDS if field not in (reader.fieldnames or [])
    ]
    if missing_headers:
        errors.append(f"CSV is missing columns: {', '.join(missing_headers)}.")
    else:
        for row_number, row in enumerate(reader, start=2):
            try:
                paper_service.add_paper(row)
                imported += 1
            except (PaperValidationError, DuplicatePaperError) as exc:
                errors.append(f"Row {row_number}: {exc}")
    return templates.TemplateResponse(
        request=request,
        name="import.html",
        context=template_context(
            request,
            result={
                "filename": file.filename or "uploaded file",
                "imported": imported,
                "errors": errors,
            },
        ),
    )


@app.get("/papers/export")
def export_papers(request: Request):
    login_redirect = require_login(request)
    if login_redirect:
        return login_redirect
    papers = paper_service.list_papers(descending=False)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=PAPER_FIELDS)
    writer.writeheader()
    for paper in papers:
        writer.writerow(
            {
                "paper_id": paper.paper_id,
                "title": paper.title,
                "authors": paper.authors,
                "institution": paper.institution,
                "publication": paper.publication,
                "publication_date": paper.publication_date.isoformat(),
                "abstract": paper.abstract,
                "keywords": paper.keywords,
            }
        )
    return StreamingResponse(
        iter([output.getvalue().encode("utf-8")]),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="papers_export.csv"'},
    )
