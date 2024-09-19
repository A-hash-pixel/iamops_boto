import datetime

class Rds():
    def __init__(self,rds_client,engine):
        self.rds_client=rds_client
        self.engine=engine
    def list_db_instances(self):
        db_status=[]
        response = self.rds_client.describe_db_instances(
            Filters=[
                {
                    'Name': 'engine',
                    'Values': [self.engine]
                },
            ],
        )
        for i in response['DBInstances']:
            db_status.append({"DB_identifier":i['DBInstanceIdentifier'],"Status":i['DBInstanceStatus']})
        return db_status
    
    @staticmethod
    def logger(logfile,db_status):
        with open(logfile,"a") as file:
            for i in db_status:
                file.writelines(f"DB {i['DB_identifier']} is in {i['Status']} at {datetime.datetime.now()} \n") 


