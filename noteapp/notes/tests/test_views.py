# notes/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from ..models import Note # Use relative import

class NoteViewTests(TestCase):
    """Tests for the Note views."""
    def setUp(self):
        # Create some notes for view tests.
        self.note1 = Note.objects.create(title="First Note", content="Content for first.")
        self.note2 = Note.objects.create(title="Second Note", content="Content for second.", summary="Summary for second")

    def test_note_list_view_get(self):
        # Test GET request for note_list view.
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertContains(response, self.note1.title)
        self.assertContains(response, self.note2.title)
        self.assertContains(response, "Summary for second")

    def test_note_list_search_view(self):
        # Test search functionality in note_list view.
        response = self.client.get(reverse('note_list'), {'search': 'First'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note1.title)
        self.assertNotContains(response, self.note2.title)

    def test_note_list_search_no_results(self):
        # Test search with no matching results.
        response = self.client.get(reverse('note_list'), {'search': 'NonExistentSearchTerm'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.note1.title)
        self.assertContains(response, 'No notes found matching')

    def test_note_detail_view_get(self):
        # Test GET request for note_detail view.
        response = self.client.get(reverse('note_detail', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        self.assertContains(response, self.note1.title)
        self.assertContains(response, self.note1.content)

    def test_note_detail_view_not_found(self):
        # Test note_detail view for a non-existent note.
        response = self.client.get(reverse('note_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    @patch('notes.views.generate_summary')
    def test_note_create_view_post_valid(self, mock_generate_summary):
        # Test POST request for note_create view with valid data.
        mock_generate_summary.return_value = "Mocked summary for new note"
        initial_note_count = Note.objects.count()
        
        response = self.client.post(reverse('note_create'), {
            'title': 'New Test Note From View',
            'content': 'Content for new test note from view.'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('note_list'))
        self.assertEqual(Note.objects.count(), initial_note_count + 1)
        
        new_note = Note.objects.latest('id')
        self.assertEqual(new_note.title, 'New Test Note From View')
        self.assertEqual(new_note.summary, "Mocked summary for new note")
        mock_generate_summary.assert_called_once_with('Content for new test note from view.')

    def test_note_create_view_post_invalid(self):
        # Test POST request for note_create view with invalid data.
        initial_note_count = Note.objects.count()
        response = self.client.post(reverse('note_create'), {
            'title': '', # Invalid
            'content': 'Some content.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')
        self.assertContains(response, 'This field is required.') # Django's default error message for required field
        self.assertEqual(Note.objects.count(), initial_note_count)

    @patch('notes.views.generate_summary')
    def test_note_update_view_post_valid(self, mock_generate_summary):
        # Test POST request for note_update view with valid data.
        mock_generate_summary.return_value = "Updated summary via mock"
        
        response = self.client.post(reverse('note_update', args=[self.note1.pk]), {
            'title': 'Updated Title by View Test',
            'content': 'Updated content by view test.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('note_detail', args=[self.note1.pk]))
        
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'Updated Title by View Test')
        self.assertEqual(self.note1.content, 'Updated content by view test.')
        self.assertEqual(self.note1.summary, "Updated summary via mock")
        mock_generate_summary.assert_called_once_with('Updated content by view test.')

    def test_note_update_view_post_invalid(self):
        # Test POST request for note_update view with invalid data.
        original_title = self.note1.title
        response = self.client.post(reverse('note_update', args=[self.note1.pk]), {
            'title': '', # Invalid
            'content': 'Attempting to update with no title.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, original_title)

    def test_note_delete_view_get(self):
        # Test GET request for note_delete confirmation page.
        response = self.client.get(reverse('note_delete', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_confirm_delete.html')
        self.assertContains(response, self.note1.title)

    def test_note_delete_view_post(self):
        # Test POST request to delete a note.
        initial_note_count = Note.objects.count()
        response = self.client.post(reverse('note_delete', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('note_list'))
        self.assertEqual(Note.objects.count(), initial_note_count - 1)
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(pk=self.note1.pk)

    def test_note_delete_view_not_found(self):
        # Test note_delete view for a non-existent note (POST).
        response = self.client.post(reverse('note_delete', args=[999]))
        self.assertEqual(response.status_code, 404)
