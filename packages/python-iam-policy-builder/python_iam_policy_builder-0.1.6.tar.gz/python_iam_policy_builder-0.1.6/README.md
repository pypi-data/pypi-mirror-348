## <ins> IAM Policy Builder </ins>

Build valid IAM policies for Google Cloud (GCP) and Amazon Web Services (AWS) <br>

### <ins> Features </ins>

Fluent chaining for clean code <br>
Output standard JSON-compatible dictionaries <br>
Avoid error-prone string manipulation <br>

### <ins> Installation </ins>

You can install this package via PIP: _pip install python-iam-policy-builder_

### <ins> Usage </ins>

<ins> GCP </ins>

```python
from iam_policy.gcp.gcp_iam_policy_builder import GCPIAMPolicyBuilder, Condition

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

print(iam_policy.build())

# [Output]
# {
#     "bindings": [
#         {
#             "role": "roles/viewer",
#             "members": [
#                 "user:alice@example.com",
#                 "serviceAccount:compute@example.com"
#             ],
#             "condition": {
#                 "title": "TimeBoundAccess",
#                 "expression": "request.time < timestamp(\"2024-12-31T23:59:59Z\")",
#                 "description": "Temporary access until end of year"
#             }
#         }
#     ],
#     "version": 3
# }
```

<ins> AWS </ins>

```python
from iam_policy.aws.aws_iam_policy_builder import AWSIAMPolicyBuilder, Statement, Effect

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

print(iam_policy.build())

# [Output]
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "iam:ListUsers"
#             ],
#             "Resource": [
#                 "arn:aws:s3:::my-bucket/*"
#             ],
#             "Condition": {
#                 "StringEquals": {
#                     "aws:username": "alice"
#                 }
#             },
#             "Sid": "AllowListUsers",
#             "Principal": {'AWS': 'arn:aws:iam::123456789012:user/alice'}
#         }
#     ]
# }
```

### <ins> Notes </ins>

<ins> GCP </ins>

- Multiple conditions per binding are not supported, as GCP IAM currently allows only one condition per binding (as of May 2025) <br>
- auditConfigs (Used for configuring audit logging) are not supported <br>
- Role names, member identifiers, and condition expressions are not validated <br>

<ins> AWS </ins>

- No validation is performed on ARNs, actions, or conditions <br>
