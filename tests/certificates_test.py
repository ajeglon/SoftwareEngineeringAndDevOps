from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.urls import reverse
from matex_app.models import CertificateHolder, CertificateInfo

# Tests for Certificates
class CertificateInfoTests(TestCase):

    def setUp(self):
        # Create cert holder
        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

    def test_certificate_info_save_auto_expiration_date(self):
        # Test that expiration date is 1 year on
        certificate = CertificateInfo(
            certificate_holder=self.certificate_holder,
            certificate_start_date=datetime(2023, 1, 1).date()
        )
        certificate.save()

        self.assertEqual(
            certificate.certificate_expiration_date,
            certificate.certificate_start_date + timedelta(days=365)
        )

    def test_certificate_info_valid_clean(self):
        # Test that valid CertificateInfo passes validation
        certificate = CertificateInfo(
            certificate_holder=self.certificate_holder,
            certificate_start_date=datetime(2023, 1, 1).date(),
            certificate_expiration_date=datetime(2024, 1, 1).date()
        )
        try:
            certificate.full_clean()  # Triggers the certClean method
        except ValidationError:
            self.fail("CertificateInfo.clean() raised ValidationError unexpectedly!")

    def test_certificate_info_missing_start_date(self):
        # Test that missing start date raises ValidationError
        certificate = CertificateInfo(
            certificate_holder=self.certificate_holder,
            certificate_expiration_date=datetime(2024, 1, 1).date()
        )
        with self.assertRaises(ValidationError) as cm:
            certificate.full_clean()

        self.assertIn('certificate_start_date', cm.exception.message_dict)

    def test_certificate_info_missing_expiration_date(self):
        # Test that missing expiration date raises ValidationError
        certificate = CertificateInfo(
            certificate_holder=self.certificate_holder,
            certificate_start_date=datetime(2023, 1, 1).date()
        )
        with self.assertRaises(ValidationError) as cm:
            certificate.full_clean()

        self.assertIn('certificate_expiration_date', cm.exception.message_dict)

    def test_certificate_info_missing_holder(self):
        # Test that missing certificate holder raises ValidationError
        certificate = CertificateInfo(
            certificate_start_date=datetime(2023, 1, 1).date(),
            certificate_expiration_date=datetime(2024, 1, 1).date()
        )
        with self.assertRaises(ValidationError) as cm:
            certificate.full_clean()

        self.assertIn('certificate_holder', cm.exception.message_dict)

# Tests for viewing Certificate-info
class CertificateInfoViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

        self.certificate_info = CertificateInfo.objects.create(
            certificate_holder=self.certificate_holder,
            certificate_start_date='2023-01-01',
            certificate_expiration_date='2024-01-01'
        )

        self.certificate_info_url = reverse('certificate-info', kwargs={'pk': self.certificate_info.certificate_number})
        self.index_url = reverse('index')

    def test_authenticated_user_can_view_certificate_info(self):
        self.client.login(username='testuser', password='testpassword')

        # Send GET request to certificate_info
        response = self.client.get(self.certificate_info_url)

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'certificate-info.html')
        self.assertEqual(response.context['certificate_record'], self.certificate_info)

    def test_unauthenticated_user_cannot_view_certificate_info(self):
        # GET request without logging in
        response = self.client.get(self.certificate_info_url)

        # Check for redirection to index page
        self.assertRedirects(response, self.index_url)

        # Check for the message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Please log in to view this page' for message in messages))

# Tests for Deleting Certificate-info
class DeleteCertificateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')

        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

        self.certificate_info = CertificateInfo.objects.create(
            certificate_holder=self.certificate_holder,
            certificate_start_date='2023-01-01',
            certificate_expiration_date='2024-01-01'
        )

        # URL for the delete_certificate
        self.delete_cert_url = reverse('delete-certificate', kwargs={'pk': self.certificate_info.certificate_number})
        self.certificates_url = reverse('certificates')

    def test_superuser_can_delete_certificate(self):
        # Log in as superuser
        self.client.login(username='admin', password='adminpassword')

        # Send GET request to delete the certificate
        response = self.client.get(self.delete_cert_url)

        # Certificate is deleted from the database
        with self.assertRaises(CertificateInfo.DoesNotExist):
            CertificateInfo.objects.get(certificate_number=self.certificate_info.certificate_number)

        # Success message and redirection
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Certificate deleted successfully' for message in messages))
        self.assertRedirects(response, self.certificates_url)

    def test_non_superuser_cannot_delete_certificate(self):
        # Log in as non-superuser
        self.client.login(username='testuser', password='testpassword')

        # Send GET request to delete the certificate
        response = self.client.get(self.delete_cert_url)

        # Ensure no deletion occurs
        self.assertEqual(CertificateInfo.objects.count(), 1)

        # Check for the 'Admin login required' message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Admin login required' for message in messages))

        # Verify redirection to the certificates list
        self.assertRedirects(response, self.certificates_url)