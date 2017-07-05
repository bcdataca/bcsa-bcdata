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
    import os
    for key in bcsa_keys:
        fn = target + '/' + key
        if os.path.isfile(fn):
            print('Warning: the file {} already exists: skipping download...'.format(fn))
        else:
            s3_anon.download_file(Bucket='bcsa-data',
                                  Key=key,
                                  Filename=target+'/'+key)
    return


def getAwsKeypair(directory=None):
    """
    getAwsKeypair expects two files named access.key and secret.key located in directory
    e.g.
    directory = '~/' or directory = '/Users/myUserName/' but NOT
    direcotry = '~' or direcotry = '/Users/myUserName'
    """
    if directory is None:
        directory = './'
    with open(directory + 'access.key', 'r+') as fp:
        access_key = fp.read()
    with open(directory + 'secret.key', 'r+') as fp:
        secret_key = fp.read()
    return (access_key, secret_key)