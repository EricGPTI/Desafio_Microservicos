import boto3

class S3:
    def __init__(self, service, region_name, access_key, secret_key):
        self.service = service
        self.region_name = region_name
        self.access_key = access_key
        self.secret_key = secret_key

    def create_resource(self):
        return boto3.resource(
                    service_name = 's3',
                    region_name = self.region_name,
                    aws_access_key_id = self.access_key,
                    aws_secret_access_key = self.secret_key
                    )

    def create_client(self):
        return boto3.client(
                    service_name = 's3',
                    region_name = self.region_name,
                    aws_access_key_id = self.access_key,
                    aws_secret_access_key = self.secret_key
                    )

    def list_buckets(self):
        bucket_names = []
        for bucket in self.create_resource().buckets.all():
            bucket_names.append(bucket.name)
        return bucket_names

    def save_object(self, bucket_name, name, data):
        self.create_resource().Bucket(bucket_name).put_object(Key=name, Body=data)
        
        
    def get_latest_created_file(self, bucket_name):
        s3_client = self.create_client()
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        all = response['Contents']
        latest = max(all, key=lambda x: x['LastModified'])
        return latest
