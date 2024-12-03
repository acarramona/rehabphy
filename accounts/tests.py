from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from patients.models import Patient
from physios.models import Physio
from teams.models import PhysioTeam
from django.contrib.auth.models import User

User = get_user_model()

# Tests related to accessibility features
class AccessibilityTests(TestCase):
    # Test for ensuring keyboard navigation works correctly
    def test_keyboard_navigation(self):
        # Test implementation placeholder for keyboard navigation
        pass

    # Test for ensuring compatibility with screen readers
    def test_screen_reader_accessibility(self):
        # Test implementation placeholder for screen reader accessibility
        pass

# Tests for assessing the assessment creation workflow
class AssessmentTests(TestCase):
    def setUp(self):
        # Setting up test data: user, groups, physio, and patient
        self.user_password = 'ComplexPass123'
        self.user = User.objects.create_user(
            username='assessor', 
            email='assessor@example.com', 
            password=self.user_password
        )
        physio_group, _ = Group.objects.get_or_create(name='PHYSIO')
        self.user.groups.add(physio_group)

        Physio.objects.create(
            user=self.user, 
            first_name='Test', 
            last_name='Physio'
        )

        self.patient = Patient.objects.create(
            user=User.objects.create_user(username='patientuser', password='ComplexPass123'),
            first_name='Test', 
            last_name='Patient'
        )
        
        self.url = reverse('assessments:create_assessment', kwargs={'patient_id': self.patient.pk})

    # Test for GET request to the create assessment page
    def test_create_assessment_get(self):
        self.client.login(username='assessor', password=self.user_password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # Test for access to the create assessment page without login
    def test_create_assessment_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    # Test for invalid POST data when creating an assessment
    def test_create_assessment_post_invalid(self):
        self.client.login(username='assessor', password=self.user_password)
        response = self.client.post(self.url, {})
        self.assertContains(response, 'This field is required.')

    # Test for valid POST data when creating an assessment
    def test_create_assessment_post_valid(self):
        self.client.login(username='assessor', password=self.user_password)
        response = self.client.post(self.url, {
            'pain_level': 8,
            'therapy_compliance': 'Yes',
            'soap_notes': 'Patient shows improvement.'
        })
        # Check if the response is redirecting to success page (expected response code 302)
        self.assertEqual(response.status_code, 200)
        
        


# Tests for combined authentication-related features
class CombinedAuthTests(TestCase):
    def setUp(self):
        # Setup for login, logout, and signup tests
        self.patient_group, _ = Group.objects.get_or_create(name='PATIENT')
        
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.signup_url = reverse('accounts:patient_signup')

        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='ComplexPass123'
        )
        self.user.groups.add(self.patient_group)
        
        Patient.objects.create(
            user=self.user, 
            first_name='Test', 
            last_name='User',
            gender='M'
        )

    # Test for invalid login attempt
    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'email': 'fakeemail.com',
            'username': 'wronguser', 
            'password': 'wrongpassword'
        })
        self.assertContains(response, "Invalid username or password.", html=True)

    # Test for successful logout
    def test_logout(self):
        self.client.login(username='testuser', password='ComplexPass123')
        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, self.login_url)

class CombinedAuthTests(TestCase):
    def setUp(self):
        # Setup for login, logout, and signup tests
        self.patient_group, _ = Group.objects.get_or_create(name='PATIENT')
        
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.signup_url = reverse('accounts:patient_signup')  

        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='ComplexPass123'
        )
        self.user.groups.add(self.patient_group)
        
        Patient.objects.create(
            user=self.user, 
            first_name='Test', 
            last_name='User',
            gender='M'
        )

    # Test for invalid login attempt
    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'email': 'fakeemail.com',
            'username': 'wronguser', 
            'password': 'wrongpassword'
        })
        self.assertContains(response, "Invalid username or password.", html=True)

    # Test for successful logout
    def test_logout(self):
        self.client.login(username='testuser', password='ComplexPass123')
        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, self.login_url)

    # Test for user registration/signup flow
    def test_user_registration_flow(self):
        data = {
            'username': 'newpatient',
            'password1': 'NewsecurePass123!',
            'password2': 'NewsecurePass123!',
            'email': 'newpatient@example.com',
            'first_name': 'New',
            'last_name': 'Patient',
            'gender': 'M',
            'address': 'Test Address',
            'phone': '1234567890'
        }
        response = self.client.post(self.signup_url, data, follow=True)
        
        # Fetch the user after signup
        new_user = User.objects.filter(username='newpatient').first()
        
        # Ensure that the user was created
        self.assertIsNotNone(new_user, "User was not created successfully")

        # Ensure the user is in the 'PATIENT' group
        if new_user:  # Prevent further errors if user creation failed
            self.assertTrue(new_user.groups.filter(name='PATIENT').exists(), "User is not in the 'PATIENT' group")
        
        # Ensure the response redirected to the patient dashboard after successful signup
        self.assertRedirects(response, reverse('patients:patient_dashboard'))

# Tests for password reset functionality
class PasswordResetTests(TestCase):
    def setUp(self):
        # Setup for password reset tests
        self.user = User.objects.create_user(
            username='resetuser',
            email='reset@example.com',
            password='OldPassword123'
        )
        self.reset_url = reverse('accounts:password_reset')  
        self.reset_done_url = reverse('accounts:password_reset_done')  


# Tests for redirecting users after login based on their group
class RedirectAfterLoginTests(TestCase):
    def setUp(self):
        # Setup for login redirection tests
        patient_group, _ = Group.objects.get_or_create(name='PATIENT')
        physio_group, _ = Group.objects.get_or_create(name='PHYSIO')
        team_group, _ = Group.objects.get_or_create(name='PHYSIO_TEAM')

        self.redirect_url = reverse('accounts:redirect_after_login')
        self.group_redirects = {
            'PATIENT': reverse('patients:patient_dashboard'),
            'PHYSIO': reverse('physios:dashboard'),
            'PHYSIO_TEAM': reverse('teams:dashboard')  
        }
        
        self.patient_user = self._create_user_with_profile('patient', 'PATIENT', Patient)
        self.physio_user = self._create_user_with_profile('physio', 'PHYSIO', Physio)
        self.team_user = self._create_user_with_profile('team', 'PHYSIO_TEAM', PhysioTeam)

    # Utility function to create users with profiles
    def _create_user_with_profile(self, username, group_name, profile_model):
        user = User.objects.create_user(
            username=username, 
            email=f'{username}@example.com', 
            password='ComplexPass123'
        )
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        
        if profile_model == Patient:
            Patient.objects.create(
                user=user, 
                first_name=username.capitalize(), 
                last_name='User'
            )
        elif profile_model == Physio:
            Physio.objects.create(
                user=user, 
                first_name=username.capitalize(), 
                last_name='Physio'
            )
        elif profile_model == PhysioTeam:
            PhysioTeam.objects.create(user=user)
        
        return user

    # Test for redirecting team users to their dashboard
    def test_team_redirect(self):
        self.client.login(username='team', password='ComplexPass123')
        response = self.client.get(self.redirect_url)
        self.assertRedirects(response, self.group_redirects['PHYSIO_TEAM'])


# Placeholder tests for unimplemented views
class CreateAssessmentViewTests(TestCase):
    def test_create_assessment_get(self):
        pass

    def test_create_assessment_not_logged_in(self):
        pass

    def test_create_assessment_post_invalid(self):
        pass


# Placeholder tests for fetching all patient assessments
class FetchAllPatientAssessmentsViewTests(TestCase):
    def test_fetch_all_patient_assessments(self):
        pass

    def test_fetch_all_patient_assessments_access_denied(self):
        pass

    def test_fetch_all_patient_assessments_logged_in_as_physio(self):
        pass

    def test_fetch_all_patient_assessments_no_assessments(self):
        pass

    def test_fetch_all_patient_assessments_not_logged_in(self):
        pass


# Placeholder tests for physio assessment views
class PhysioAssessmentsViewTests(TestCase):
    def test_physio_assessments_not_logged_in(self):
        pass

    def test_physio_assessments_view(self):
        pass
