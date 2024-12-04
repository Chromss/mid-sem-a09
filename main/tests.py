from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Journal, Souvenir
from django.urls import reverse

User = get_user_model()

class JournalModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.journal = Journal.objects.create(
            author=self.user,
            title='Test Journal',
            content='This is a test journal.'
        )

    def test_journal_creation(self):
        self.assertEqual(self.journal.title, 'Test Journal')
        self.assertEqual(self.journal.content, 'This is a test journal.')
        self.assertEqual(self.journal.author, self.user)

    def test_total_likes(self):
        self.assertEqual(self.journal.total_likes(), 0)

    def test_is_liked_by(self):
        self.assertFalse(self.journal.is_liked_by(self.user))

class SouvenirModelTests(TestCase):
    def setUp(self):
        self.souvenir = Souvenir.objects.create(
            name='Test Souvenir',
            price=10.00,
            place_name='Test Place',
            description='This is a test souvenir.'
        )

    def test_souvenir_creation(self):
        self.assertEqual(self.souvenir.name, 'Test Souvenir')
        self.assertEqual(self.souvenir.price, 10.00)
        self.assertEqual(self.souvenir.place_name, 'Test Place')
        self.assertEqual(self.souvenir.description, 'This is a test souvenir.')

class JournalViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_journal_view(self):
        response = self.client.post(reverse('main:create_journal'), {
            'title': 'New Journal',
            'content': 'Content for the new journal.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Journal.objects.filter(title='New Journal').exists())

    def test_like_journal_view(self):
        journal = Journal.objects.create(author=self.user, title='Test Journal', content='Content for testing.')
        response = self.client.post(reverse('main:like_journal', args=[journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(journal.likes.filter(id=self.user.id).exists())

        # Unliking the journal
        response = self.client.post(reverse('main:like_journal', args=[journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(journal.likes.filter(id=self.user.id).exists())

    def test_journal_home_view(self):
        response = self.client.get(reverse('main:journal_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/journal_home.html')

class SouvenirViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.souvenir = Souvenir.objects.create(
            name='Test Souvenir',
            price=15.00,
            place_name='Test Place',
            description='Description of test souvenir.'
        )

    def test_souvenir_list_view(self):
        response = self.client.get(reverse('main:souvenir_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Souvenir')
        self.assertTemplateUsed(response, 'main/souvenir_list.html')