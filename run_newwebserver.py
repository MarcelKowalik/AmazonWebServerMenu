#Created by Marcel Kowalik, Student number:20076466
#!/usr/bin/env python3
import os
import sys
import boto3
import time
import subprocess

##Menu
def print_menu():  
    print ("MENU")
    print ("1. Create an Instance")
    print ("2. List Instances")
    print ("3. Terminate Instance")
    print ("4. Create Bucket")
    print ("5. List Buckets")
    print ("6. Delete Bucket")
    print ("7. Put Image into Bucket")
    print ("8. Check Web server for nginix")
    print ("9. Send image to webserver")
    print ("10. Exit")
    print ("------------------")

##Creates an EC2 instance
def create_instance():
    key_pem = input("Please input the security key name:")
    security_group = input("Enter Security group id:")
    ec2 = boto3.resource('ec2')
    instance = ec2.create_instances(
        ImageId='ami-047bb4163c506cd98',
        KeyName=key_pem,     # Security key name from previous input.
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[security_group],    # my HTTP/SSH sec group 
        UserData='''#!/bin/bash 
                    yum -y update                   
                    yum install python36 -y          
                    yum -y install nginx
                    service nginx start
                    chkconfig nginx on
                    touch /home/ec2-user/testfile''',  # Installs nginix and python 3.6 on the EC2
        InstanceType='t2.micro')    
    print ("An instance with ID", instance[0].id, "has been created.")
    time.sleep(5)               #Sleep to allow time to create EC2 and public ip adress
    instance[0].reload()
    print ("Public IP address:", instance[0].public_ip_address)

##lists all the instances to 
def list_instance():
    time.sleep(2)
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        print ("Instance ID:", instance.id, "State:", instance.state, "Instance Public Address:", instance.public_ip_address)

##Creates a bucket an names it.
def create_bucket():
    s3 = boto3.resource("s3")
    bucket_name = input("Enter Bucket name:")
    try:
        response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},ACL="public-read")
        print (response)        #Prints out the bucket ip address if the instance is successfully created.
    except Exception as error:
        print (error)

#Lists all the buckets.
def list_bucket():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    print("Bucket List: %s" % buckets)

##Deletes the bucket by its name.
def delete_bucket():
    s3 = boto3.resource('s3')
    bucket_name = input("Enter Bucket name to delete:")
    bucket = s3.Bucket(bucket_name)
    try:
        response = bucket.delete()          #deletes the bucket
        print (response)
    except Exception as error:
        print (error)

#terminates the instance using the id and waits until the instance is terminated.
def terminate():
    client = boto3.client('ec2')
    waiter = client.get_waiter('instance_terminated')
    id = input("Instance ID:")
    client.terminate_instances(InstanceIds=[id])        #Sets the instance to terminate state.
    waiter.wait(InstanceIds=[id])      #The waiter checks every 15 seconds until a successful state is reached. An error is returned after 40 failed checks.        
    print ("Instance with id: "+id+" has been terminated.")

##Inserts a file into the bucket
def put_image():
    s3 = boto3.resource("s3")
    bucket_name = input("Enter Bucket name to send image:")
    object_name = input("Enter Image name:")
    try:
        response = s3.Object(bucket_name, object_name).put(Body=open(object_name, 'rb'), ACL="public-read")     #Puts an file into the bucket and sets "public-read" on the file.
        print (response)
    except Exception as error:
        print (error)

##Loads in the check_server.py file from the local machine and executes
def check_server():
    instance_ip = input("Please input the public ip address of the Instance:")
    key_pem = input("Please input the security key name:")
    copycommand="scp -i "+key_pem+".pem check_webserver.py ec2-user@"+instance_ip+":."      #Copies the "check_webserver.py" into the instance
    print(copycommand)
    subprocess.run(copycommand, shell=True)
    runcommand="ssh -i "+key_pem+".pem ec2-user@"+instance_ip+" python3 check_webserver.py"        #Logs into the instance and runs the python script.
    time.sleep(2)

##Creates a html file and uploads it into the instance, it the uses the link of the uploaded image in the html to view it on the server. 
def set_image():
    bucketname = input("Put in Bucket Name:")
    instance_ip = input("Please input the public ip address of the Instance:")
    key_pem = input("Please input the security key name:")
    subprocess.run("echo '<html lang='en'><head><meta charset='utf-8'><title>The HTML5 Herald</title></head><body><h1>Image</h1><img src='https://s3-eu-west-1.amazonaws.com/"+bucketname+"/test.jpg'></</body></html>' >  index.html", check=True,shell=True)
    copycommand="scp -i "+key_pem+".pem index.html ec2-user@"+instance_ip+":."
    print(copycommand)
    subprocess.run(copycommand, shell=True)
    #creates a html file to view the file that was uploaded onto the bucket and copies it onto the instance.

loop=True      
  
while loop:  ## While loop which will keep going until loop = False
    print_menu()    ## Displays menu
    choice = input("Enter your choice [0-9]: ")
     
    if choice=='1':
        print ("Creating Instance...")     
        create_instance()  
    elif choice=='2':
        print ("Listing Instances...")
        list_instance()
    elif choice=='3':
        print ("Terminating Instance...")
        terminate()
    elif choice=='4':
        print ("Creating Bucket...")
        create_bucket()
    elif choice=='5':
        print ("Listing Buckets...")
        list_bucket()
    elif choice=='6':
        print ("Deleting Bucket...")
        delete_bucket()
    elif choice=='7':
        print ("Puting Image into a selected Bucket...")
        put_image()
    elif choice=='8':
        print ("Checking the Webserver for nginix...")
        check_server()
    elif choice=='9':
        print ("Set Image on the Web server...")
        set_image()
    elif choice=='0':
        print ("Exiting...")
        loop=False # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        print ("Invalid number. Try again...")


