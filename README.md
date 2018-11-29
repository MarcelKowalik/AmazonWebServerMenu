# AWS Instance Manager

## Name: Marcel Kowalik

#### What is an AWS Instance Manager?
This program was created to manage basic AWS EC2 instances task using Python/Boto3.

## What can this program do?

#### Introduction
The user will be promted to provide all required data at the start for each of the task.
This enables users to manualy configure each task and provide information such as the required keypair created with the AWS account.

#### 1. Create Instance
The program will require you to provide security group id for the instance we wish to create and keypair that we want to associate with the EC2 instance that we are creating.
* Creates EC2 instance
* Sets specified Security Group
* Installs nginix and python 3.6 on the EC2
* Prints out the Public Ip to the console

#### 2. List Instances
Lists out all the instances, their state and public ip address to the console.
* Prints out all the Instances
* Shows their current state: (Terminated,Running,Stoped)
* Displays public IP addresses of the instances.

#### 3. Terminates Instance.
Terminates the instance using the id and waits until the instance is terminated using the waiter function. 
* Terminates Instance
* Waits until the instance is fully terminated before continuing 

#### 4. Create Bucket.
Since there is only one thing required to start an s4 bucket it prompts the user for the name of the bucket.
* Creates S3 Bucket with the specified name
* Promps the user if the Bucket already exists

#### 5. List Buckets.
Lists all the buckets created by the user.
* Displays all s3 Buckets created by the user and their name.

#### 6. Delete Bucket.
This deletes the bucket created by the user and files inside it.
* Deletes s3 Bucket by name selected by the user.

#### 7. Put Image into Bucket.
Inserts a file into a s3 Bucket which is specified by the user.
* Inserts a file into the specified s3 Bucket
* Changes permission of this file.

#### 8. Check Web server for nginix
Copies the check_webserver.py script onto the server using secure copy(scp) which copies the file onto the instance of our choice. The check_webserver.py script check if nginx server is running on the specified instance.
* Copies check_webserver.py script onto specified instance.
* The script checks if nginx is running on the instance.

#### Send image to webserver.
Creates a html file and uploads it into the instance, it the uses the link of the uploaded image in the html to view it on the server. 
* Creates a html file for the webserver to view the image.
* Copies the file usic scp onto the instance to the change the default index.html page.






