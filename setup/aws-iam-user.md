# Create AWS IAM User

To use the AWS CLI, you need an IAM user with appropriate permissions.

**Prerequisite:** You need your own AWS account to create a new user. AWS offers [free tier accounts](https://aws.amazon.com/free/?trk=ef905f42-3063-4b3c-ad04-fa8211c5f71b&sc_channel=ps&ef_id=Cj0KCQjw9-PNBhDfARIsABHN6-0hwVo7oiOCPSxHKys2XoPvAXek1xblLF1k0PrP-odUE411c4_Zru4aAm6NEALw_wcB:G:s&s_kwcid=AL!4422!3!795877020710!e!!g!!aws%20free%20tier%20account!23527793744!194311064284&gad_campaignid=23527793744&gbraid=0AAAAADjHtp91HJvZWRsW6Ywi9drdsv3Te&gclid=Cj0KCQjw9-PNBhDfARIsABHN6-0hwVo7oiOCPSxHKys2XoPvAXek1xblLF1k0PrP-odUE411c4_Zru4aAm6NEALw_wcB) to get you started.

**It is not recommended to use your AWS root account for these activities.**

Follow these steps in the AWS Console to set up a new IAM user under your account:

1. Log in to the [AWS Management Console](https://console.aws.amazon.com/)
2. Navigate to **IAM** (Identity and Access Management)
3. Click on **Users** in the left sidebar
4. Click **Create user**
5. Enter a username (e.g., "ds2002-cli-user")
6. Create an **access key** for programmatic access (for AWS CLI usage). Console access is optional.
7. Attach policies: 
   - For EC2 access, attach the `AmazonEC2FullAccess` policy (or more restrictive policies as needed)
   - For S3 access (used in storage exercises), attach the `AmazonS3FullAccess` policy
   - You can attach multiple policies to a single IAM user
8. Review and create the user
9. **Important:** Download or copy the **Access Key ID** and **Secret Access Key** — you'll need these to configure the AWS CLI.
