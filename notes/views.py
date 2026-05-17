from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import connection
from .models import Note


def index(request):
    """Homepage - list all notes"""
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})


def detail(request, pk):
    """Detail view for a single note"""
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/detail.html', {'note': note})


# ================================================
# ⚠️ INTENTIONAL VULNERABILITY #4: SQL Injection
# Bandit rule B608 (Medium Severity)
# CodeQL will also catch this
# User input directly concatenated into SQL query
# ================================================
def search_notes(request):
    """Search notes by title - VULNERABLE to SQL Injection"""
    query = request.GET.get('q', '')

    with connection.cursor() as cursor:
        # NEVER do this in real code - direct string concatenation
        sql = "SELECT id, title, subject FROM notes_note WHERE title LIKE '%" + query + "%'"
        cursor.execute(sql)
        rows = cursor.fetchall()

    results = [{'id': r[0], 'title': r[1], 'subject': r[2]} for r in rows]
    return JsonResponse({'results': results})


def api_notes(request):
    """Simple API endpoint returning all notes as JSON"""
    notes = Note.objects.values('id', 'title', 'subject', 'created_at')
    return JsonResponse({'notes': list(notes)})
