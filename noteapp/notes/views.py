import os
import logging
from openai import OpenAI
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Note
from .forms import NoteForm

# Get an instance of a logger
logger = logging.getLogger(__name__)

def generate_summary(content):
    """Generates a summary for the given content using OpenRouter."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not content or not api_key:
        # Don't attempt if no content or API key is missing
        if not api_key:
            logger.warning("OPENROUTER_API_KEY environment variable not set. Cannot generate summary.")
        return None 

    # Initialize client here, only when needed
    client = OpenAI(
        base_url=os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1"),
        api_key=api_key,
    )

    try:
        # Using a cost-effective model like Haiku, adjust as needed
        # Reference: https://posthog.com/tutorials/openrouter-observability
        completion = client.chat.completions.create(
            model="anthropic/claude-3-haiku", 
            messages=[
                {"role": "system", "content": "Summarize the following text concisely:"},
                {"role": "user", "content": content},
            ],
            max_tokens=25, # Limit summary length
            temperature=0.5,
        )
        summary = completion.choices[0].message.content.strip()
        return summary
    except Exception as e:
        logger.error(f"Error generating summary: {e}") # Log error appropriately in production
        return None

def note_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        notes = Note.objects.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        ).order_by('-created_at')
    else:
        notes = Note.objects.all().order_by('-created_at')
        
    return render(request, 'notes/note_list.html', {'notes': notes, 'search_query': search_query})

def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save() # Save the note first to get an instance
            # Generate and save the summary
            note.summary = generate_summary(note.content)
            note.save(update_fields=['summary']) # Save only the summary field
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Create'})

def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            updated_note = form.save()
            # Regenerate and save the summary
            updated_note.summary = generate_summary(updated_note.content)
            updated_note.save(update_fields=['summary']) # Save only the summary field
            return redirect('note_detail', pk=pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'note': note, 'action': 'Update'})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
