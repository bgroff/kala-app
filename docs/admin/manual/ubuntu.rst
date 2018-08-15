Manual Ubuntu 16.04 Install
===========================

Spin up a new EC2 machine (Ubuntu 16.04), it should have a security group with ssh access (your IP/32 is a good rule), http and https open to the world (If that is what you want).

If you want to use S3 [0] and SQS [1], which I recommend, then you should create a bucket for your documents and a queue for background jobs. You will also need an IAM role that has the correct permissions for these resources (the easiest thing to do is grant all access, but up to the user). Attach the IAM role either during the creation of the EC2 machine, or after the machine has booted.

Once the machine is up, run:

.. code-block:: bash

    git clone https://github.com/bgroff/kala-app.git
    sudo mv kala-app/ /srv/
    sudo sh /srv/kala-app/deploy/provision/ubuntu.sh 

This should get you a running instance of the application, with the two test users described in the README.

You can then edit the deployment environment variables to setup your AWS account information

.. code-block:: bash

    sudo nano /etc/uwsgi/apps-enabled/{your-ec2-instance-hostname}.ini

| Change the DEPLOYMENT_ENVIRONMENT=dev to DEPLOYMENT_ENVIRONMENT=production
| Add env = EXPORT_QUEUE={YOUR_SQS_QUEUE_NAME}
| Add env = AWS_REGION={YOUR_REGION}
| Add env = S3_STORAGE_BUCKET={YOUR_BUCKET_NAME}

Then you can restart uwsgi:

.. code-block:: bash

    sudo systemctl restart uwsgi

If everything went right, you should now be able to use S3 for document storage.

It is recommended to add an SSL certificate for your install. You can get a free certificate from letsencrypt. Directions are available from the Digital Ocean page [2].

| [0] - https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html
| [1] - https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-create-queue.html
| [2] - https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04
