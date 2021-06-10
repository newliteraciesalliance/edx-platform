from openedx.core.djangoapps.waffle_utils import CourseWaffleFlag


WAFFLE_NAMESPACE = 'learning_sequences'

# .. toggle_name: learning_sequences.use_for_outlines
# .. toggle_implementation: CourseWaffleFlag
# .. toggle_description: Waffle flag to enable the use of the Learning Sequences
#   Course Outline API (/api/learning_sequences/v1/course_outline/{course_key}).
#   Staff can always use this endpoint. If you are a student and this endpoint
#   is not enabled, it will return a 403 error. The Courseware MFE should know
#   how to detect this condition.
# .. toggle_use_cases: temporary, open_edx
# .. toggle_creation_date: 2021-06-07
# .. toggle_target_removal_date: 2020-08-01
USE_FOR_OUTLINES = CourseWaffleFlag(WAFFLE_NAMESPACE, 'use_for_outlines', __name__)
