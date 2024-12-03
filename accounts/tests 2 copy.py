from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.contrib.auth import SESSION_KEY
from patients.models import Patient
from physios.models import Physio

User = get_user_model()

class PatientSignUpViewTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:patient_signup')
        self.group_name = 'PATIENT'

    def test_get_signup_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/patient_signup.html')

    def test_valid_signup(self):
        data = {
            'email': 'testpatient@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
            'first_name': 'Test',
            'last_name': 'Patient',
            'gender': 'M',
            'address': 'Express road, Lane 64',
            'phone': '1236547892',
        }
        response = self.client.post(self.url, data)
        user_exists = User.objects.filter(email='testpatient@example.com').exists()
        self.assertTrue(user_exists)
        user = User.objects.get(email='testpatient@example.com')
        self.assertTrue(user.groups.filter(name=self.group_name).exists())
        self.assertIn(SESSION_KEY, self.client.session)
        self.assertRedirects(response, reverse('patients:dashboard'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Your account details is sent to your email." in m.message for m in messages))

    def test_invalid_signup(self):
        data = {
            'email': 'invalidemail.com',
            'password1': 'pass',
            'password2': 'pass',
        }
        response = self.client.post(self.url, data)
        user_exists = User.objects.filter(email='invalid-email').exists()
        self.assertFalse(user_exists)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/patient_signup.html')


class RedirectAfterLoginViewTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:redirect_after_login')
        self.group_redirects = {
            'PATIENT': reverse('patients:dashboard'),
            'PHYSIO': reverse('physios:dashboard'),
            'PHYSIO_TEAM': reverse('teams:dashboard'),
        }
        self.user_password = 'ComplexPass123'
        
        self.patient_user = User.objects.create_user(
            username='patientuser@example.com',
            email='patientuser@example.com', password=self.user_password)
        patient_group, _ = Group.objects.get_or_create(name='PATIENT')
        self.patient_user.groups.add(patient_group)
        self.patient_user.is_active = True
        self.patient_user.save()

        self.physio_user = User.objects.create_user(
            username='physiouser@example.com',
            email='physiouser@example.com', password=self.user_password)
        physio_group, _ = Group.objects.get_or_create(name='PHYSIO')
        self.physio_user.groups.add(physio_group)
        self.physio_user.is_active = True
        self.physio_user.save()

        self.team_user = User.objects.create_user(
            username='teamuser@example.com',
            email='teamuser@example.com', password=self.user_password)
        team_group, _ = Group.objects.get_or_create(name='PHYSIO_TEAM')
        self.team_user.groups.add(team_group)
        self.team_user.is_active = True
        self.team_user.save()

    def test_patient_redirect(self):
        self.client.login(username='patientuser@example.com', password=self.user_password)
        Patient.objects.create(user=self.patient_user, first_name='Test', last_name='Patient')
        response = self.client.get(self.url)
        self.assertRedirects(response, self.group_redirects['PATIENT'])

    def test_physio_redirect(self):
        self.client.login(username='physiouser@example.com', password=self.user_password)
        Physio.objects.create(user=self.physio_user, first_name='Test', last_name='Physio')
        response = self.client.get(self.url)
        self.assertRedirects(response, self.group_redirects['PHYSIO'])

    def test_team_redirect(self):
        self.client.login(username='teamuser@example.com', password=self.user_password)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.group_redirects['PHYSIO_TEAM'])

    def test_no_group_user(self):
        user = User.objects.create_user(username='nousergroup@example.com', email='nousergroup@example.com', password=self.user_password)
        user.is_active = True
        user.save()
        self.client.login(username='nousergroup@example.com', password=self.user_password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        login_url = reverse('accounts:login')
        expected_redirect = f'{login_url}?next={self.url}'
        self.assertRedirects(response, expected_redirect)





class DashboardAccessTests(TestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user(username='patient@example.com', email='patient@example.com', password='ComplexPass123')
        Group.objects.get_or_create(name='PATIENT')[0].user_set.add(self.patient_user)
        self.physio_user = User.objects.create_user(username='physio@example.com', email='physio@example.com', password='ComplexPass123')
        Group.objects.get_or_create(name='PHYSIO')[0].user_set.add(self.physio_user)

    def test_patient_dashboard_access(self):
        self.client.login(username='patient@example.com', password='ComplexPass123')
        response = self.client.get(reverse('patients:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_physio_dashboard_access(self):
        self.client.login(username='physio@example.com', password='ComplexPass123')
        response = self.client.get(reverse('physios:dashboard'))
        self.assertEqual(response.status_code, 200)


class SessionManagementTests(TestCase):
    def test_session_timeout(self):
        self.client.login(username='patient@example.com', password='ComplexPass123')
        self.client.logout()
        response = self.client.get(reverse('patients:dashboard'))
        self.assertRedirects(response, reverse('accounts:login'))


class AccessibilityTests(TestCase):
    def test_keyboard_navigation(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<button', status_code=200)

    def test_screen_reader_accessibility(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'alt=', status_code=200)


class MobileResponsivenessTests(TestCase):
    def test_mobile_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


# Combined Test Cases
class CombinedTests(TestCase):
    def setUp(self):
        self.user_email = 'test@patient.com'
        self.user_password = 'ComplexPass123'
        self.user = User.objects.create_user(email=self.user_email, password=self.user_password)

    def test_user_registration_flow(self):
        self.client.get(reverse('accounts:patient_signup'))
        data = {
            'email': 'newpatient@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
            'first_name': 'New',
            'last_name': 'Patient',
            'gender': 'M',
            'address': 'New Address',
            'phone': '1234567890',
        }
        response = self.client.post(reverse('accounts:patient_signup'), data)
        self.assertRedirects(response, reverse('patients:dashboard'))

    def test_patient_login_flow(self):
        self.client.login(email=self.user_email, password=self.user_password)
        response = self.client.get(reverse('patients:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'wronguser@example.com',
            'password': 'wrongpassword',
        })
        self.assertContains(response, "Please enter a correct username and password.")

    def test_logout(self):
        self.client.login(email=self.user_email, password=self.user_password)
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('home'))
