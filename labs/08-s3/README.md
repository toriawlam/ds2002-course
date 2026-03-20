# Lab 08: S3 Storage

In this lab you will connect what you have learned about the command line, AWS accounts, and scripting to work hands-on with **Amazon S3**. You will create and configure a bucket, move files between UVA's HPC system and AWS, and write small scripts that automate common storage tasks.

When you are done, you will have a working pattern for securely storing, sharing, and retrieving data in S3—both from the CLI and from Python. Paste the URL to your `mywork/lab8` folder in Canvas for grading.

## Learning goals

By completing this lab, you will be able to:

- Use the AWS CLI, create a bucket in S3.
- Upload a file into the bucket.
- Verify the file is in the bucket.
- Verify the file is not publicly accessible.
- Create an expiring URL for the file and verify access.
- Modify the bucket ACL to allow for public access.
- Upload a new file with public access enabled, and verify access.
- Upload a file and delete it.
- Finally, write Python3 scripts using the `boto3` package to upload a private files, a public file, and to presign an object in S3. This includes copying files from UVA's HPC system to AWS S3 storage.

## Setup

**Environment**
This lab requires that you have a working Python3 environment and both the AWS CLI tool (with access keys configured) and Python3 / `boto3` installed. 

1. Start a Code Server (VSCode) session in Open OnDemand on UVA's HPC system.

2. Activate your environment:
   ```bash
   module load miniforge
   source activate ds2002
   ```

3. AWS CLI and Python packages  
   The `ds2002` environment should have the AWS CLI and `boto3` packages installed. If you need to reinstall (on the HPC system or elsewhere), follow these steps:

    AWS CLI installation:  
    ```bash
    python3 -m pip install awscli
    ```
    
    `boto3` installation:
    ```bash
    python3 -m pip install boto3
    ```

**AWS CLI configuration**

You are set up as user `ds2002` in AWS. Your credentials are posted in the Canvas assignment for this lab. Look them up now. You will need:

- AWS_ACCESS_KEY
- AWS_SECRET_ACCESS_KEY

> **It is highly advised NOT to use root credentials for access in this way.**

In the terminal, follow these steps to configure the `aws` command line tools:
```bash
aws configure
```

You will be prompted to enter:
- **AWS Access Key ID**: Enter the Access Key ID (from Canvas)
- **AWS Secret Access Key**: Enter the Secret Access Key (from Canvas)
- **Default region name**: Enter your preferred AWS region (use `us-east-1`, you generally want to choose the one that's geographically closest)
- **Default output format**: Enter `json` (recommended) or `text` or `table`   

The AWS account you enter in these steps must have at least read permission to access the resources you want to download. 

Upon completion of `aws configure` you will see a hidden directory `~/.aws`. 

> **Note:** Remember, the creation of personal config files in hidden directories inside your home directory is a best-practice pattern. 

**Check the config file**

You can verify your AWS configuration by viewing the config file:
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
    "Arn": "arn:aws:iam::nnnnnnnnnnnnn:user/ds2002-user"
}
```

## S3 Security and HTTP Access by URL

S3 buckets are PRIVATE by default. No files or objects uploaded to a plain, unaltered bucket are ever publicly accessible. In this lab you will learn more about public and private buckets and objects.

AWS operates many `regions` of infrastructure around the world. We will be using the `us-east-1` region, the first and one of their largest regions. To get the web URL to any public file in `us-east-1` this is the syntax:

```text
https://s3.amazonaws.com/ + BUCKET_NAME + / file/path.sfx
```
For example, this URL points to a publicly accessible file within a publicly accessible bucket:
[`https://s3.amazonaws.com/ds2002-resources/cloud.jpg`](https://s3.amazonaws.com/ds2002-resources/cloud.jpg)

## Task 1: Working with S3 Buckets via AWS CLI

> **Note:** Replace all references to `ds2002-mst3k` with `ds2002-<YOUR_COMPUTING_ID>` where `<YOUR_COMPUTING_ID>` is your actual computing ID. This ensures you each have a unique bucket and can complete the lab without interfering with others.

1. From either the VS Code or your local terminal, list any existing buckets (there should be none):

    ```bash
    aws s3 ls
    ```

2. Create a new bucket using the `mb` S3 subcommand. Add your computing ID to the name of the bucket, i.e. `ds2002-mst3k` and so on. Note the use of the `s3://` protocol before the bucket name.

    ```bash
    aws s3 mb s3://ds2002-mst3k
    ```

3. Grab an image file. Using the `curl` command below you can retrieve any image from the Internet you want to use for this lab. Once you have the URL copied for the image, use this command syntax:

    ```bash
    curl URL > file
    ```
    For example, to fetch a sample cloud image. You can output the image to a new file name.
    ```bash
    curl https://decisionstats.com/wp-content/uploads/2016/09/april-fools-day-the-7-funniest-data-cartoons-r-bloggers.jpg > cloud.jpg
    ```

4. So now you have a local file. Imagine you want to upload the file to your new S3 bucket. Use the AWS CLI to do this. The syntax is:
    ```bash
    aws s3 cp FILE s3://BUCKET/
    ```

    For example, to upload the `cloud.jpg` image:

    ```bash
    aws s3 cp cloud.jpg s3://ds2002-mst3k/
    ```

5. Go ahead and upload your file. List the contents of your bucket to verify it is there. Notice it is the same `ls` command, but specifying the bucket to list the contents of:

    ```
    aws s3 ls s3://ds2002-mst3k/
    ```
    which should return something like:
    ```text
    2026-03-17 15:56:35     124639 cloud.jpg
    ```

## Working with Presigned Objects

6. Take the bucket and file path and assemble a public URL to your file as described at the start of this lab:
    ```text
    # https://s3.amazonaws.com/ + BUCKET_NAME + / FILE_PATH
    
    https://s3.amazonaws.com/ds2002-mst3k/cloud.jpg
    ```
    Test that URL using your web browser. What do you see?

7. You cannot retrieve the file using a plain HTTPS address because anonymous web access is not allowed to your bucket or your file. Let's do a special trick S3 is capable of by creating an "expiring" URL that allows access to your file for a specified amount of time.

    The syntax for the command is:
    ```
    aws s3 presign --expires-in 30 s3://ds2002-mst3k/cloud.jpg

    # The --expires-in flag is how many seconds the file should be public.
    # The s3:// is the BUCKET+FILE path to your specific file.
    ```

    Once you issue this command, it will return a long URL with signature:
    
    ```
    https://s3.amazonaws.com/ds2002-mst3k/pdfs/json-overview.pdf?AWSAccessKeyId=AKIAJLBYZFLFQQT256OQ&Signature=cjcY98KLjZ6CXbTnaZ9Srt8MQVM%3D&Expires=1708376373
    ```
    
    Open that link in a browser - you should be able to see your file.

    If you refresh the browser after the expiration period has elapsed, what do you see then?

8. Write a simple `bash` script, `presigned-upload.sh` that performs two actions:

    1. Uploads a file (image, PDF, etc.) to a private bucket.
    2. Presigns a URL to that file with an expiration of `604800` (7 days).
    3. Write the script so that it takes three positional arguments: the name of the local file to upload, the name of the bucket in your account, and the length of expiration in seconds.

    Test your script a few times, with enough of a short expiration that you can observe it timing out.

9. Update your bucket's ACL (Access Control List)

    - Open the AWS Management Console (use the credentials for `ds2002-user` posted in Canvas assignemnt for this lab).
    - Within the AWS Management Console, open the S3 service and find your bucket.
    - Click the name of the bucket to get detailed settings.
    - Select the Permissions tab within your bucket settings.
    - Click "Edit" within the Block public access section.
    - Uncheck all boxes and save your settings. Confirm the change.
    - Click "Edit within the Object Ownership section.
    - Enable ACLs by checking the right-hand radio button. Confirm your changes by checking the box. Leave "Bucket owner preferred" selected. Save your changes.

    These changes have not made your bucket or any of its contents public. However, they have now allowed you the option to specifically make any contents public if you choose to do so. (Without the above changes this would not be possible.)

    S3 also allows you to set a bucket policy to allow public access to ALL objects, or only objects of certain types, among many other policy options if needed.

10. Now that your bucket allows you to grant public access to specific files, fetch another image file from the Internet (`.gif`, `.png`, `.jpg`, etc.) and upload it with this syntax to make it public. Note the `--acl public-read` option (`acl` stands for access control list):

    ```bash
    aws s3 cp --acl public-read IMAGE s3://BUCKET_NAME/
    ```

    For example:
    ```bash
    aws s3 cp --acl public-read another_image.jpg s3://ds2002-mst3k/
    ```

11. Test access

    Using the `bucket/file` path structure, construct the URL for your file like this: 
    [`https://s3.amazonaws.com/ds2002-mst3k/cloud.jpg`](https://s3.amazonaws.com/ds2002-mst3k/cloud.jpg)

12. Delete a file in your bucket. Using the AWS CLI, upload another image file to the bucket. List the bucket contents to confirm it has been uploaded. And, finally, delete the file using this syntax:

    ```bash
    aws s3 rm s3://BUCKET_NAME/FILE_NAME
    ```

    For example
    ```bash
    aws s3 rm s3://ds2002-mst3k/cloud.jpg
    ```

    And confirm the file has been deleted:
    ```bash
    aws s3 ls s3://ds2002-mst3k/
    ```

13. To empty a bucket completely, a `--recursive` option is available:

    ```bash
    aws s3 rm s3://BUCKET_NAME/FILE_NAME --recursive
    ```

    You can only delete empty buckets. Once empty, to delete:
    ```bash
    aws s3 rb s3://BUCKET_NAME
    ```

## Task 2: Use the `boto3` library with Python3

Developers should keep in mind that S3 is a web service, or API, which means that in addition to using the AWS Management Console or CLI tools you can work with any AWS service using the language of your choice.

In this section of the lab you will perform basic S3 operations using Python3 and the `boto3` library.

Complete documentation for `boto3` is available:

* `boto3` - https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
* `s3` - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

The following tasks assume you are able to import `boto3` successfully.

### Upload a file to S3 and keep it private

1. Each AWS service you connect to via `boto3` needs a `client` or `resource` or some other reusable connection. Let's create a simple client for the S3 service:

    ```python
    import boto3

    s3 = boto3.client('s3', region_name='us-east-1')
    ```
    
    The variable `s3` populated with an instance of the `boto3.client` class can be named anything you like. Once a class object it can be reused for other calls to that specific service.


2. Once you have created a client you are now ready to use it. In your command prompt (in a local terminal or VSCode, etc.), upon invoking the `s3` class object you just created, you will notice many new options:

    ```python
    s3.<TAB>
    ```

3. For instance, list all your buckets:

    ```python
    import boto3

    # create client
    s3 = boto3.client('s3', region_name="us-east-1")

    # make request
    response = s3.list_buckets()

    # now iterate through the response:
    for r in response['Buckets']:
        print(r['Name'])
    ```

    This will return the name(s) of any bucket(s) in your account in a full JSON payload, with all results nested a single array. Note that above, a variable named `response` was created and populated with the results of the `list_buckets()` method. This is an arbitrary variable name - you can always use your own.

4. To upload a file to your bucket:

    ```python
    bucket = 'ds2002-mst3k'
    local_file = 'project/cloud.jpg'

    response = s3.put_object(
        Body = local_file,
        Bucket = bucket,
        Key = local_file
    )
    ```

    Some explanation:

      - `bucket` is an S3 bucket that already exists.
      - `local_file` is the path/file you want to upload.
      - `Key` within the `put_object()` method is the destination path you want for the uploaded path. Key is composed of `prefix` (project in this case) and the `filename`.
      - These three parameters are the minimum required for a `put_object` call. There are many other options.

5. Write your own upload script and test for success. Try getting the file using a public URL. You should get `Permission Denied`.

### Upload a file to S3 and make it public

Upload a new file to S3 with public visibility. The request will be like the one above, but add the following parameter to the function call:

    ACL = 'public-read',

Test your file upload using a public URL to see if you can access it.


### Task 3: Upload files from UVA's HPC system to AWS S3

In Lab 07 you ran a Slurm job array that produced multiple output files on UVA's HPC system (for example, `results-1.csv` through `results-5.csv` in `/scratch/$USER/ds2002-jobruns/text-analysis`). 

**The `scratch` folder is a high-performance filesystem intended for temporary use. Files that have not been accessed for 90 days are automatically deleted.** Therefore, it is important to implement a file transfer strategy to copy output files that need to be retained to a separate storage location, i.e. AWS S3 Storage.

1. Write a Python script according to these specifications
   - The script should accept two command line arguments, the first specifying the input folder with the `results*.csv` files to upload, and the second specifying the **bucket and prefix** to upload to, i.e. `ds2002-mst3k/book-analysis/`.
   - Following the import statements, instantiate a logger. 
   - Create a function `parse_args` to parse the command line arguments, returning the input folder and bucket/prefix destination.
   - Create a function `upload` that accepts two arguments: `input_folder` and `destination`. Wrap the boto3 client setup and the upload commands in a `try`/`except` block. The `except` block should log the error message. 
   - The code should have an `if __name__ == "__main__":` block that calls a `main` function.
   - The main function should call the functions for command line parsing and upload. At the end of the main function log a success/failure message.
   - Each function should have docstrings describing its purpose.    

2. Run your script.
   
3. Log into the AWS console. The login URL and credentials are posted in the Canvas assignment for this lab. In the AWS console, search for the `S3` service and navigate to your corresponding bucket (for example, `ds2002-mst3k`). Confirm that the `book-analysis/` folder contains all uploaded `results-*.csv` files from Lab 07.

### BONUS - Task 4 (optional): Create an S3 bucket for a website

As a web-enabled storage service, S3 buckets can also serve web content including entire websites. Look at https://www.rc.virginia.edu/ as an example. To configure a bucket into a website follow these steps:

1. Create a new bucket `web-mst3k` (replace mst3k with your own computing id). Make it a "General Purpose" bucket.
2. For "Object Ownership" select "ACLs Enabled". Leave "Bucket Owner Preferred" ownership selected.
3. Unselect the "Block All Public Access" box. You want to allow public access.
4. Select the box acknowledging that you understand the impact of these new settings.
5. Leave other settings as-is and create the bucket. Once created, click into the bucket name from the list of all buckets.
6. Select the "Permissions" tab and scroll down to the Bucket Policy area. Edit the policy, inserting this IAM policy (be sure to change the bucket name to your bucket):

    ```
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": "*",
          "Action": "s3:GetObject",
          "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
      ]
    }
    ```

7. Save your changes to the policy. Switch to the "Properties" tab for your bucket and scroll to the bottom.
8. Edit the Static Website Hosting section. For the index document enter `index.html` and for the error document enter `error.html`
9. Save your changes. The page will refresh and you will see a website URL appear, something like http://ds2002-mst3k.s3-website-us-east-1.amazonaws.com/
10. To test your site, upload a sample HTML file named `index.html` to your bucket. Here is such a file: https://s3.amazonaws.com/ds2002-resources/labs/lab4/index.html

    ```
    curl https://s3.amazonaws.com/ds2002-resources/labs/lab4/index.html > index.html
    aws s3 cp index.html s3://BUCKET-NAME/
    ```
11. Then visit the URL of your website-enabled bucket with a browser. The page should be visible.


## Submit your work

By the end of this lab, your repository should contain the following in `mywork/lab8/`:

- A **bash script** from Task 1 named `presigned-upload.sh` that:
  - Uploads a file to a private bucket.
  - Generates a presigned URL with an expiration time (e.g. 7 days).
- A **Python script** from Task 2 that:
  - Uploads a file to S3 (private).
  - Can optionally upload a public file and generate a presigned URL.
- A **Python script** from Task 3 that:
  - Reads `results-*.csv` files from your Lab 07 scratch directory.
  - Uploads them to your `ds2002-<computing_id>` bucket under the `book-analysis/` prefix.

Add, commit, and push your `mywork/lab8` folder, then submit the GitHub URL to that folder in Canvas for lab completion credit.
