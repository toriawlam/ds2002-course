# Tips & Tricks

Short notes for the course AWS project: linking to the Chalice automation lab, wiring Lambda in a VPC for outbound internet access, and using Secrets Manager from Lambda.

## AWS Lambda functions with Chalice

- [Event-triggered pipelines with Chalice](../practice/12-automation/README.md#event-triggered-pipelines-with-aws-chalice)

- [Scheduled Lambda functions with Chalice](../practice/12-automation/README.md#scheduled-lambda-functions-with-aws-chalice)

If your Lambda function must reach the public internet, run it in a **private subnet** that routes outbound traffic through a **NAT gateway**, and attach a **security group** whose rules allow the outbound access your code needs (your instructor’s VPC setup may already include this).

The appropriate VPC, subnet, route tables, and NAT are already set up in AWS. Use this in the Chalice app’s `config.json`:
```json
{
  "version": "2.0",
  "app_name": "iss-tracker",
  "stages": {
    "dev": {
      "api_gateway_stage": "api",
      "subnet_ids": ["subnet-0e4259410bd8fd6f5"],
      "security_group_ids": ["sg-0be6679b34372f15a"]
    }
  }
}
```

## AWS Secrets Manager

**AWS Secrets Manager** is a managed **key–value** store for any sensitive information you want to keep out of source code and Git (API keys, tokens, database credentials, and so on). You can restrict who may read a secret (for example only a Lambda execution role), optionally rotate credentials, and audit access. For this course, **plan to keep database credentials in Secrets Manager for every project** that talks to a database instead of hard-coding them or checking them into a repository.

0. Service account vs individual account

- **Individual account** (what you used in earlier labs): an IAM user and access keys tied to *you* as a person, plus often a personal database login. That is fine when *you* run queries from your laptop or notebook. Those credentials identify a human and should not be embedded in Lambda or shared across teammates.

- **Service account** (recommended for the team project): a dedicated database user (and matching secret in Secrets Manager) used *only* by your application—for example the Lambda execution role reads the secret and connects as that DB user. It is not anyone’s personal login. Permissions can be narrow (only what the app needs), you can rotate or revoke it without touching people’s own accounts, and the whole team uses the same automation path.

1. Store the Secret:

- In the AWS Secrets Manager console, choose **Store a new secret**.

- Select **Credentials for an Amazon RDS database** (or **Credentials for another database** for engines such as MongoDB).

- Enter the database username and password and associate it with your RDS instance.

2. Grant Lambda Permissions:

- The Lambda function’s execution role must have permission to call `secretsmanager:GetSecretValue` (and to decrypt the secret if you use a customer-managed KMS key).

- You can attach the managed policy `SecretsManagerReadWrite` for broad access, or add a custom inline policy that allows only the specific secret ARN.

3. Retrieve in Code:

- Use the AWS SDK (for example **Boto3** in Python) to call **`GetSecretValue`**.

- **Tip:** Retrieve secrets during initialization (outside the handler) and cache them so you do not call `GetSecretValue` on every invocation—this cuts latency and API cost.

## Database access from UVA HPC

- Job arrays run under your **individual** HPC account; there is no separate HPC “service account.”

- Your personal AWS CLI profile still lets jobs call **AWS Secrets Manager** to read the team’s database secret (service-account **username** and **password**, plus **URL** and **port** for the instance). The team keeps connection details in one place; when the database or credentials change, update the secret in Secrets Manager instead of editing every member’s job scripts.

## Resources

- [AWS Secrets Manager User Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [AWS Chalice documentation](https://aws.github.io/chalice/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Lambda in a VPC (NAT and subnets)](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html)
- [Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [Boto3: Secrets Manager client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html)