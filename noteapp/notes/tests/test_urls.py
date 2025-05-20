# notes/tests/test_urls.py
from django.test import SimpleTestCase # Use SimpleTestCase for URL tests as no DB is needed
from django.urls import reverse, resolve
from .. import views # Use relative import for views

class NoteURLTests(SimpleTestCase):
    """Tests for the note app URLs."""

    def test_note_list_url_resolves(self):
        # Test that 'note_list' URL resolves to the correct view.
        url = reverse('note_list')
        self.assertEqual(resolve(url).func, views.note_list)

    def test_note_create_url_resolves(self):
        # Test that 'note_create' URL resolves to the correct view.
        url = reverse('note_create')
        self.assertEqual(resolve(url).func, views.note_create)

    def test_note_detail_url_resolves(self):
        # Test that 'note_detail' URL resolves to the correct view.
        # We need an argument for pk, so we resolve the path directly.
        resolver = resolve('/notes/1/') # Assuming notes are at /notes/
        self.assertEqual(resolver.func, views.note_detail)
        self.assertEqual(resolver.kwargs['pk'], 1)

    def test_note_update_url_resolves(self):
        # Test that 'note_update' URL resolves to the correct view.
        resolver = resolve('/notes/1/update/')
        self.assertEqual(resolver.func, views.note_update)
        self.assertEqual(resolver.kwargs['pk'], 1)

    def test_note_delete_url_resolves(self):
        # Test that 'note_delete' URL resolves to the correct view.
        resolver = resolve('/notes/1/delete/')
        self.assertEqual(resolver.func, views.note_delete)
        self.assertEqual(resolver.kwargs['pk'], 1)

    # Test reversing URLs by name
    def test_reverse_note_list(self):
        self.assertEqual(reverse('note_list'), '/notes/')

    def test_reverse_note_create(self):
        self.assertEqual(reverse('note_create'), '/notes/create/')

    def test_reverse_note_detail(self):
        self.assertEqual(reverse('note_detail', args=[123]), '/notes/123/')

    def test_reverse_note_update(self):
        self.assertEqual(reverse('note_update', args=[123]), '/notes/123/update/')

    def test_reverse_note_delete(self):
        self.assertEqual(reverse('note_delete', args=[123]), '/notes/123/delete/')
