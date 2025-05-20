# notes/tests/test_models.py
import time
from django.test import TestCase
from django.utils import timezone
from ..models import Note # Use relative import

class NoteModelTests(TestCase):
    """Tests for the Note model."""
    def test_note_creation(self):
        # Test Note object creation and initial values.
        note = Note.objects.create(
            title="Test Note",
            content="This is the content of the test note."
        )
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "This is the content of the test note.")
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)
        self.assertIsNone(note.summary)
        self.assertTrue(abs((timezone.now() - note.created_at).total_seconds()) < 1)

    def test_note_str_method(self):
        # Test the __str__ method.
        note = Note.objects.create(title="My Test Title", content="Some content.")
        self.assertEqual(str(note), "My Test Title")

    def test_note_timestamps_on_update(self):
        # Test created_at and updated_at on modification.
        note = Note.objects.create(title="Timestamp Test", content="Content.")
        created_at_initial = note.created_at
        updated_at_initial = note.updated_at

        time.sleep(0.01) # Ensure a time difference

        note.content = "Updated content."
        note.save()

        self.assertEqual(note.created_at, created_at_initial)
        self.assertTrue(note.updated_at > updated_at_initial)

    def test_note_summary_update(self):
        # Test updating the summary field.
        note = Note.objects.create(title="Summary Test", content="Content for summary.")
        self.assertIsNone(note.summary)
        note.summary = "This is a test summary."
        note.save()
        note.refresh_from_db()
        self.assertEqual(note.summary, "This is a test summary.")
