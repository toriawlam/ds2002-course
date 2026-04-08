from chalice import Chalice

app = Chalice(app_name="s3-event")

# Whenever an object is uploaded to 'mybucket'
# this lambda function will be invoked.


@app.route("/")
def index():
    return {"hello": "This is a simple S3 event handler"}

@app.on_s3_event(bucket="chalice-example")
def handler(event):
    # handle all events
    print(
        f"Object event detected for bucket: {event.bucket}, key: {event.key}. <Add your custom boto3 command to do something>"
    )