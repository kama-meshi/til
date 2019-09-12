# Boto3でS3の全オブジェクトを取得する方法

レスポンスに含まれる `NextContinuationToken` を利用する。
`list.objects_v2` は1000件までしか取得できない。

`boto3.resource` を利用すれば意識せずとも全オブジェクト利用可能。
> **ただしその場合はPrefixによるフィルタリングができない**

``` Python
import boto3

# Use client
s3client = boto3.client('s3')
bucket = 'my-bucket'
contents = []
next_token = ''
while True:
    if next_token == '':
        response = s3client.list_objects_v2(Bucket=bucket, Prefix='xxx')
    else:
        response = s3client.list_objects_v2(Bucket=bucket, Prefix='xxx',
                                            ContinuationToken=next_token)

    contents.extend(response['Contents'])
    if 'NextContinuationToken' in response:
        next_token = response['NextContinuationToken']
    else:
        break

# Use resource
s3resource = boto3.resource('s3')
bucket = s3resource.Bucket(bucket)
for o in bucket.objects.all():
    pass
```
