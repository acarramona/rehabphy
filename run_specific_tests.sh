#!/bin/bash

# Run specific Django tests
python manage.py test \
  accounts.tests.CombinedAuthTests.test_invalid_login \
  accounts.tests.CombinedAuthTests.test_logout \
  accounts.tests.CreateAssessmentViewTests.test_create_assessment_get \
  accounts.tests.PhysioAssessmentsViewTests.test_physio_assessments_view \
  accounts.tests.FetchAllPatientAssessmentsViewTests.test_fetch_all_patient_assessments_logged_in_as_physio
