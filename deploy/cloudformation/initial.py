import argparse
import os
import random
import string

from awacs.aws import PolicyDocument, Statement
from awacs.s3 import Action as S3Action
from awacs.sqs import Action as SQSAction
from troposphere import *
from troposphere import ec2, rds
from troposphere.iam import Role, InstanceProfile, Policy
from troposphere.s3 import Bucket
from troposphere.sqs import Queue


def init_cloud(args):
    template = Template()

    queue = template.add_resource(
        Queue(
            "{0}".format(args.sqs_name),
            QueueName="{0}".format(args.sqs_name),
        )
    )

    bucket = template.add_resource(
        Bucket(
            "{0}".format(args.s3_name),
            BucketName="{0}".format(args.s3_name)
        )
    )

    kala_security_group = template.add_resource(
        ec2.SecurityGroup(
            "{0}".format(args.kala_security_group),
            GroupName="{0}".format(args.kala_security_group),
            GroupDescription="Enable HTTP and HTTPS access on the inbound port",
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    IpProtocol="tcp",
                    FromPort="80",
                    ToPort="80",
                    CidrIp="0.0.0.0/0",
                ),
                ec2.SecurityGroupRule(
                    IpProtocol="tcp",
                    FromPort="443",
                    ToPort="443",
                    CidrIp="0.0.0.0/0",
                ),
            ]
        )
    )

    database_security_group = template.add_resource(
        ec2.SecurityGroup(
            "{0}".format(args.database_security_group),
            GroupName="{0}".format(args.database_security_group),
            GroupDescription="Enable Database access for the security groups",
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    IpProtocol="tcp",
                    FromPort="5432",
                    ToPort="5432",
                    SourceSecurityGroupName=Ref(kala_security_group),
                ),
            ]
        )
    )

    database = template.add_resource(
        rds.DBInstance(
            "{0}".format(args.rds_instance_name),
            DBInstanceIdentifier="{0}".format(args.rds_instance_name),
            DBName=args.rds_name,
            MasterUsername="{0}".format(args.rds_username),
            MasterUserPassword="{0}".format(args.rds_password),
            AllocatedStorage=args.rds_allocated_storage,
            DBInstanceClass=args.rds_instance_class,
            Engine="postgres",
            MultiAZ=args.production,
            StorageEncrypted=True,
            VPCSecurityGroups=[GetAtt(database_security_group, "GroupId")]
        )
    )

    s3_policy = PolicyDocument(
        Version="2012-10-17",
        Id="{0}Policy".format(args.s3_name),
        Statement=[
            Statement(
                Effect="Allow",
                Action=[S3Action("*")],
                Resource=[
                    Join("", [GetAtt(bucket, "Arn"), "/*"])
                ]
            ),
        ]
    )

    sqs_policy = PolicyDocument(
        Version="2012-10-17",
        Id="{0}Policy".format(args.s3_name),
        Statement=[
            Statement(
                Effect="Allow",
                Action=[
                    SQSAction("*")
                ],
                Resource=[GetAtt(queue, "Arn")]
            )
        ]
    )
    role = Role(
        '{0}Role'.format(args.iam_role),
        RoleName='{0}Role'.format(args.iam_role),
        AssumeRolePolicyDocument={
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                    }
                }
            ]
        },
        Policies=[
            Policy(
                PolicyName="KalaS3Policy",
                PolicyDocument=s3_policy
            ),
            Policy(
                PolicyName="KalaSQSPolicy",
                PolicyDocument=sqs_policy
            )
        ]
    )
    template.add_resource(
        role
    )
    template.add_resource(
        InstanceProfile(
            "{0}InstanceProfile".format(args.iam_role),
            Roles=[Ref(role)],
            InstanceProfileName="{0}InstanceProfile".format(args.iam_role)
        )
    )

    return template


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        help='Specify an output format',
        choices=['json', 'yaml'],
        type=str,
        default='json'
    )
    parser.add_argument(
        '--production',
        help='Specify if this is production. The default is False',
        choices=[True, False],
        type=bool,
        default=False
    )

    parser.add_argument(
        '--iam_role',
        help='Give the IAM role a different name. The default is KalaInstanceProfile',
        type=str,
        default='KalaInstanceProfile'
    )
    parser.add_argument(
        '--kala_security_group',
        help='Give the kala security group a different name. The default is KalaSecurityGroup',
        type=str,
        default='KalaSecurityGroup'
    )
    parser.add_argument(
        '--database_security_group',
        help='Give the database security group a different name. The default is DatabaseSecurityGroup',
        type=str,
        default='DatabaseSecurityGroup'
    )
    parser.add_argument(
        '--sqs_name',
        help='Change the export queue name to something else. The default is ExportQueue',
        type=str,
        default='ExportQueue'
    )
    parser.add_argument(
        '--s3_name',
        help='Change the export bucket name to something else. The default is exports{random_string}',
        type=str,
        default='exports'
    )
    parser.add_argument(
        '--elb_name',
        help='Give the ELB a different name. The default is KalaELB',
        type=str,
        default='KalaELB'
    )
    parser.add_argument(
        '--rds_username',
        help='Database username. The default is kala',
        type=str,
        default='kala'
    )
    parser.add_argument(
        '--rds_password',
        help='Database password',
        type=str,
        required=True
    )
    parser.add_argument(
        '--rds_allocated_storage',
        help='Database storage size in (GB)',
        type=str,
        default='100'
    )
    parser.add_argument(
        '--rds_instance_class',
        help='Database instance type. The default is db.t2.medium',
        type=str,
        default='db.t2.medium'
    )
    parser.add_argument(
        '--rds_instance_name',
        help='Database name. The default is kala',
        type=str,
        default='kala'
    )
    parser.add_argument(
        '--rds_name',
        help='Database name',
        type=str,
        default='kala'
    )

    args = parser.parse_args()
    if args.s3_name == 'exports':
        args.s3_name += ''.join([random.choice(string.ascii_lowercase) for n in range(10)])

    print("Export Queue Name: {0}".format(args.s3_name))
    template = init_cloud(args)

    os.makedirs('../build', exist_ok=True)
    with open('../build/initial.{0}'.format(args.output), 'w') as _file:
        data = template.to_json() if args.output == 'json' else template.to_yaml()
        _file.write(data)
