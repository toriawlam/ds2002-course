# Setup

To get started with your AWS project, you have been given a new AWS user account with broader permissions.

Your new AWS credentials are in the `Teams-Group Project` spreadsheet (link on Canvas).

**Please do not use the `ds2002` user account for the final project.**

Use the steps below to sign in to the **AWS Console** and to create your personal **access keys** for command-line access.

## AWS Console login & CLI configuration

1. Open the AWS Console URL in your web browser.

2. Enter your AWS username.

3. Enter your temporary password. You will be prompted to change your password during your first login. You can save your new password to your password manager if you like, but don't share it with anyone.

4. In the AWS console, go to `IAM` > `Users`.

5. In the users list, click your name.

6. Inside the `Summary` box, locate the `Create access keys` button.

7. In the next window, select `Command Line Interface (CLI)`. Click the confirmation check box at the bottom of the window, then click `Next`.

8. On the next screen, click `Create access key`.

9. On the next screen, click the `Show` button to reveal both your `Access key` and your `Secret access key`. **Keep the window open until you have completed all steps.**

10. Start an Open OnDemand Code Server session.

11. Activate your `ds2002` environment.

12. Add the keys to your AWS CLI profile.

In the next step, you will override your current `ds2002-user` credentials. That is OK; you will not need them anymore.

Execute:
```bash
aws configure
```

You will be prompted to enter:
- **AWS Access Key ID**: Enter the Access Key ID from the previous step.
- **AWS Secret Access Key**: Enter the Secret Access Key from the previous step.
- **Default region name**: Enter your preferred AWS region (use `us-east-1`; you generally want the one that is geographically closest).
- **Default output format**: Enter `json` (recommended), `text`, or `table`.

13. Check the configuration files.

You can verify your AWS configuration by viewing these files:
```bash
cat ~/.aws/config
cat ~/.aws/credentials
```

Or test your configuration by running:
```bash
aws sts get-caller-identity
```

This command will display in JSON format the associated AWS account ID, user ARN, and user ID, confirming that your credentials are working correctly.

It should look similar to this:
```json
{
    "UserId": "xxxxxxxxxxxxx",
    "Account": "nnnnnnnnnnnnnnn",
    "Arn": "arn:aws:iam::nnnnnnnnnnnnn:user/peter"
}
```

14. You can now close the `IAM` window in the AWS Console.
