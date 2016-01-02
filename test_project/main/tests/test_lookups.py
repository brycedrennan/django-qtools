# coding=utf-8
import unittest

from django.db.models.query_utils import Q
from django.utils import timezone
from qtools.exceptions import InvalidLookupUsage
from qtools.filterq import obj_matches_q
from qtools.lookups import SUPPORTED_LOOKUP_NAMES, evaluate_lookup

from main.models import MiscModel
from .base import QInPythonTestCase


class TestLookups(QInPythonTestCase):
    @unittest.skip("Takes too long to run")
    def test_all_lookups_basic(self):
        field_names = ['nullable_boolean', 'boolean', 'integer', 'float', 'decimal', 'text', 'date', 'datetime', 'foreign', 'many']
        test_values = list(self.generate_test_value_pairs())
        lookup_names = SUPPORTED_LOOKUP_NAMES

        self.assert_lookups_work(field_names, lookup_names, test_values, fail_fast=False, skip_first=0)

    def test_invalid_usage_regex(self):
        m = MiscModel()
        m.save()
        with self.assertRaisesRegexp(InvalidLookupUsage, 'string'):
            obj_matches_q(m, Q(text__regex=[1, 2, 3]))

    def test_week_days(self):
        now = timezone.now()
        for day in range(0, 8):
            self.assert_lookup_works('week_day', 'datetime', now, day)

    def test_case_sensitivity(self):
        m = MiscModel(text='a')
        assert obj_matches_q(m, Q(text__iexact='A'))
        assert not obj_matches_q(m, Q(text__exact='A'))

