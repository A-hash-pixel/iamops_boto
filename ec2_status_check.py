
import datetime


class instances():
    def __init__(self,ec2_client,vpc_id):
        self.ec2_client=ec2_client
        self.vpc_id=vpc_id

    def list_instances(self):
        instance_ids=[]

        response=self.ec2_client.describe_instances(
            Filters=[
                {
                    'Name' : 'vpc-id',
                    'Values' : [
                        self.vpc_id
                    ]
                },
            ]
        )
        try:
            instances_list=response['Reservations'][0]['Instances']
            for i in instances_list:
                instance_ids.append(i['InstanceId'])
        except:
            print("No ec2s present in mentioned vpc")        
        return instance_ids

    
    def instance_status(self,instances_ids):
        statuses=[]
        response=self.ec2_client.describe_instance_status(
            InstanceIds=instances_ids
        )
        status=response['InstanceStatuses']
        for i in status:
            statuses.append({"Instance_id":i['InstanceId'],"State":i['InstanceStatus']['Details'][0]['Status']})
        return statuses
    
    @staticmethod
    def logger(log_file,status):
        with open(log_file,"a") as file:
            for i in status:
                file.writelines(f"Instance {i['Instance_id']} is in {i['State']} at {datetime.datetime.now()} \n") 
