# notes/tests/test_forms.py
from django.test import TestCase
from ..forms import NoteForm # Use relative import

class NoteFormTests(TestCase):
    """Tests for the NoteForm."""
    def test_valid_note_form(self):
        # Test form validity with correct data.
        form_data = {'title': 'Valid Title', 'content': 'Valid content.'}
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_note_form_no_title(self):
        # Test form invalidity if title is missing.
        form_data = {'content': 'Some content without a title.'}
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_note_form_no_content(self):
        # Test form invalidity if content is missing.
        form_data = {'title': 'Title without content.'}
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_note_form_widgets_classes(self):
        # Test form widgets have expected CSS classes.
        form = NoteForm()
        # These classes are from your NoteForm Meta class
        self.assertEqual(form.fields['title'].widget.attrs.get('class'), 'w-full p-2 border rounded')
        self.assertEqual(form.fields['content'].widget.attrs.get('class'), 'w-full p-2 border rounded h-48')
