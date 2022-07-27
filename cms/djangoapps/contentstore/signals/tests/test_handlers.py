"""
Tests for signal handlers in the contentstore.
"""

from datetime import datetime
from unittest.mock import patch

from django.test.utils import override_settings
from opaque_keys.edx.locator import CourseLocator, LibraryLocator
from openedx_events.content_authoring.data import CourseCatalogData, CourseScheduleData

import cms.djangoapps.contentstore.signals.handlers as sh
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import SampleCourseFactory


class TestCatalogInfoSignal(ModuleStoreTestCase):
    """
    Test functionality of triggering catalog info signals (and events) from course_published signal.
    """

    def setUp(self):
        super().setUp()
        self.course = SampleCourseFactory.create(
            org='TestU',
            number='sig101',
            display_name='Signals 101',
            run='Summer2022',
        )
        self.course_key = self.course.id

        self.expected_data = CourseCatalogData(
            course_key=CourseLocator(org='TestU', course='sig101', run='Summer2022', branch=None, version_guid=None),
            name='Signals 101',
            schedule_data=CourseScheduleData(
                start=datetime.fromisoformat('2030-01-01T00:00+00:00'),
                pacing='instructor',
                end=None,
                enrollment_start=None,
                enrollment_end=None),
            short_description=None,
            effort=None,
            hidden=False,
            invitation_only=False
        )

    @override_settings(SEND_CATALOG_INFO_SIGNAL=True)
    @patch('cms.djangoapps.contentstore.signals.handlers.COURSE_CATALOG_INFO_CHANGED', autospec=True)
    def test_emit_regular_course(self, mock_signal):
        """On a normal course publish, send an event."""
        sh.emit_catalog_info_changed_signal(self.course_key)
        mock_signal.send_event.assert_called_once_with(catalog_info=self.expected_data)

    @override_settings(SEND_CATALOG_INFO_SIGNAL=True)
    @patch('cms.djangoapps.contentstore.signals.handlers.COURSE_CATALOG_INFO_CHANGED', autospec=True)
    def test_ignore_library(self, mock_signal):
        """When course key is actually a library, don't send."""
        sh.emit_catalog_info_changed_signal(LibraryLocator(org='SomeOrg', library='stuff'))
        mock_signal.send_event.assert_not_called()

    @override_settings(SEND_CATALOG_INFO_SIGNAL=False)
    @patch('cms.djangoapps.contentstore.signals.handlers.COURSE_CATALOG_INFO_CHANGED', autospec=True)
    def test_disabled(self, mock_signal):
        """When toggle is disabled, don't send."""
        sh.emit_catalog_info_changed_signal(self.course_key)
        mock_signal.send_event.assert_not_called()
