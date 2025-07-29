from enum import Enum
from typing import NamedTuple, List, Optional, Dict, Any


class Effect(Enum):
    Allow = 'Allow'
    Deny = 'Deny'


class Statement(NamedTuple):
    """
    Helper class for declaring AWS IAM policy statements.

    Attributes:
    - Effect (Effect): Either "Allow" (Effect.Allow) or "Deny" (Effect.Deny)
    - Action (List[str]): One or more AWS service actions (E.G. "s3:GetObject")
    - Resource (List[str]): One or more ARNs specifying the resources
    - Condition (Optional[Dict[str, Dict[str, Any]]]): Optional condition block
    - Sid (Optional[str]): Statement ID for easier tracking
    - Principal (Optional[Dict[str, Any]]): Used in trust policies (E.G. {"Service": "ec2.amazonaws.com"})

    Example:
        Statement(
            Effect=Effect.Allow,
            Action=["s3:GetObject"],
            Resource=["arn:aws:s3:::my-bucket/*"],
            Condition={"StringEquals": {"s3:prefix": "home/"}},
            Sid="AllowReadAccess"
        )._asdict()
    """
    Effect: Effect
    Action: List[str]
    Resource: List[str]
    Condition: Optional[Dict[str, Dict[str, Any]]] = None
    Sid: Optional[str] = None
    Principal: Optional[Dict[str, Any]] = None


class AWSIAMPolicyBuilder:
    """
    A builder for AWS IAM policy documents.

    [Usage]
    iam_policy = AWSIAMPolicyBuilder(version="2012-10-17")

    iam_policy.add_statement(
        Statement(
            Effect=Effect.Allow.value,
            Action=["iam:ListUsers"],
            Resource=["arn:aws:s3:::my-bucket/*"],
            Sid="AllowListUsers",
            Condition={
                "StringEquals": {
                    "aws:username": "alice"
                }
            },
            Principal={"AWS": "arn:aws:iam::123456789012:user/alice"},
        )._asdict()
    )

    print(iam_policy.build())

    [Output]
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "iam:ListUsers"
                ],
                "Resource": [
                    "arn:aws:s3:::my-bucket/*"
                ],
                "Condition": {
                    "StringEquals": {
                        "aws:username": "alice"
                    }
                },
                "Sid": "AllowListUsers",
                "Principal": {"AWS": "arn:aws:iam::123456789012:user/alice"}
            }
        ]
    }

    Notes:
        - No validation is performed on ARNs, actions, or conditions
    """

    def __init__(self, version: str):
        self._version = version
        self._statements: List[Dict] = []

    def add_statement(self, statement: dict) -> 'AWSIAMPolicyBuilder':
        """
        Adds a new IAM policy statement to the policy

        This method filters out any keys in the statement dictionary that have `None` values
        This helps avoid generating invalid AWS IAM policy JSON, as AWS does not accept -
        keys like "Sid", "Condition", or "Principal" with null values

        Parameters:
            statement (dict): A dictionary representation of a policy statement, typically
                              generated from 'Statement(...)._asdict()`

        Returns:
            AWSIAMPolicyBuilder: The builder instance for chaining
        """
        clean_statement = {k: v for k, v in statement.items() if v is not None}
        self._statements.append(clean_statement)
        return self

    def build(self) -> Dict:
        return {'Version': self._version, 'Statement': self._statements}
