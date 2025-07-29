import unittest

from iam_policy.aws.aws_iam_policy_builder import AWSIAMPolicyBuilder, Statement, Effect


class TestAWSIAMPolicyBuilder(unittest.TestCase):
    def test_aws_iam_policy_builder(self):
        expected_iam_policy = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Effect': 'Allow',
                    'Action': [
                        'iam:ListUsers'
                    ],
                    'Resource': [
                        'arn:aws:s3:::my-bucket/*'
                    ],
                    'Condition': {
                        'StringEquals': {
                            'aws:username': 'alice'
                        }
                    },
                    'Sid': 'AllowListUsers',
                    'Principal': {'AWS': 'arn:aws:iam::123456789012:user/alice'},
                }
            ]
        }

        iam_policy = AWSIAMPolicyBuilder(version='2012-10-17')

        iam_policy.add_statement(
            Statement(
                Effect=Effect.Allow.value,
                Action=['iam:ListUsers'],
                Resource=['arn:aws:s3:::my-bucket/*'],
                Sid='AllowListUsers',
                Condition={
                    'StringEquals': {
                        'aws:username': 'alice'
                    }
                },
                Principal={'AWS': 'arn:aws:iam::123456789012:user/alice'},
            )._asdict()
        )

        self.assertEqual(iam_policy.build(), expected_iam_policy)
