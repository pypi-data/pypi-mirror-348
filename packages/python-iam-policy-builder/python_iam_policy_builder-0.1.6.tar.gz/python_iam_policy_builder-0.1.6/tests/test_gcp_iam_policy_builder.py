import unittest

from iam_policy.gcp.gcp_iam_policy_builder import GCPIAMPolicyBuilder, Condition


class TestGCPIAMPolicyBuilder(unittest.TestCase):
    def test_gcp_iam_policy_builder(self):
        expected_iam_policy = {
            'version': 3,
            'bindings': [
                {
                    'role': 'roles/viewer',
                    'members': [
                        'user:alice@example.com',
                        'serviceAccount:compute@example.com'
                    ],
                    'condition': {
                        'title': 'TimeBoundAccess',
                        'expression': 'request.time < timestamp("2024-12-31T23:59:59Z")',
                        'description': 'Temporary access until end of year'
                    }
                }
            ]
        }

        iam_policy = GCPIAMPolicyBuilder(version=3)

        iam_policy.add_binding(
            role='roles/viewer',
            members=[
                'user:alice@example.com',
                'serviceAccount:compute@example.com'
            ],
            condition=Condition(
                title='TimeBoundAccess',
                expression='request.time < timestamp("2024-12-31T23:59:59Z")',
                description='Temporary access until end of year'
            )._asdict()
        )

        self.assertEqual(iam_policy.build(), expected_iam_policy)
