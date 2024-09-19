import boto3
import os
import rds_status_check
import ec2_status_check
import datetime
from dotenv import load_dotenv, dotenv_values 
from smtplib import SMTP  
load_dotenv() 
access_key=os.getenv("ACCESS_KEY")
secret_key=os.getenv("SECRET_KEY")
session=boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name='ap-south-1'
    # profile_name="default"
)
rds_client = boto3.client('rds','ap-south-1')
ec2_client = boto3.client('ec2','ap-south-1')
vpc=os.getenv("VPC_ID")
print(vpc)
# vpc='vpc-02210c43441a2fb83'
engine=os.getenv("engine")
host=os.getenv("HOST")
from_addr=os.getenv("From")
to_addr=os.getenv('TO')
log_file=os.getenv('LOG_FILE')


def send_mail(msg,from_addr,host,to_addr):
    with SMTP(host=host,port=587) as smtp:
        response=smtp.send_message(
            msg=msg,
            from_addr=from_addr,
            to_addrs=to_addr
        )
        # print(response)

def object_creator():
    rds=rds_status_check.Rds(rds_client,engine)
    db_status=rds.list_db_instances()
    # db_status=[{'DB_identifier':'test','Status':'Healthy'},{'DB_identifier':'tester','Status':'Pending'}]
    for i in db_status:
        if i['Status'] != 'Healthy':
            msg=f"Db instance {i['DB_identifier']} is in {i['Status']} at {datetime.datetime.now()} \n"
            try:
                send_mail(msg)
            except Exception as e:
                print("Error in sending email ",e)    
    rds.logger(log_file,db_status)
    instance=ec2_status_check.instances(ec2_client,vpc)
    instance_ids=instance.list_instances()
    instance_status=instance.instance_status(instances_ids=instance_ids)
    for i in instance_status:
        if i['State'] != 'passed':
            msg=f"Instance {i['Instance_id']} is in {i['State']} at {datetime.datetime.now()} \n"
            try:
                send_mail(msg)
            except Exception as e:
                print("Error in sending email ",e)
    instance.logger(log_file,status=instance_status)

if __name__ == '__main__':
    object_creator()
