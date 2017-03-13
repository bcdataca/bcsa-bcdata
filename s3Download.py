def bcsa(target='.'):
    # import necessary libraries
    import boto3
    from botocore import UNSIGNED
    from botocore.client import Config
    # initialize s3 client
    s3_anon = boto3.client('s3', region_name='ca-central-1',
                           config=Config(signature_version=UNSIGNED))
    # list objects in data directory
    bcsa_list = s3_anon.list_objects(Bucket='bcsa-data', Delimiter='/')
    # get key names from object list
    bcsa_keys = [key['Key'] for key in bcsa_list['Contents']]
    # Make sure target exists; create it if it does not
    try:
        import os
        os.mkdir('./tmp')
    except FileExistsError as FEE:
        pass
    print('Fetching files:\n{}'.format(bcsa_keys))
    # download $key to $target/$key
    for key in bcsa_keys:
        s3_anon.download_file(Bucket='bcsa-data',
                              Key=key,
                              Filename=target+'/'+key)
    return

