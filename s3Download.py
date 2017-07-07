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


class BatchDownloader:
    def __init__(self, key_size_df=None, s3_session=None, Bucket=None,
                 save_directory=None, max_batch_size=None,
                 aws_access=None, aws_secret=None, region_name=None):
        # Setting up the list of files for download
        if key_size_df is None:
            # assume that a new list will be passed in for each batch
            self.batch_lists = True
        # Setting up the S3 Session
        if s3_session is None:
            if not (aws_access is None) and not (aws_secret is None):
                import boto3
                if region_name is None:
                    s3_session = boto3.client('s3', region_name='ca-central-1',
                                              aws_access_key_id=aws_access,
                                              aws_secret_access_key=aws_secret)
                else:
                    s3_session = boto3.client('s3',
                                              aws_access_key_id=aws_access,
                                              aws_secret_access_key=aws_secret)
                self.s3_session = s3_session
            else:
                raise Exception('must provide AWS S3 session or AWS ' +
                                'credentials to intialize new session')
        else:
            from botocore.client import BaseClient
            if isinstance(s3_session, BaseClient):
                self.s3_session = s3_session
            else:
                raise ValueError('Expected botocore.client.s3 ' +
                                 'object for s3_session.')
        # setting up the function to download from Bucket
        from functools import partial
        self.download = partial(self.s3_session.download_file, Bucket=Bucket)
        # set up save_directory
        from os import makedirs
        if save_directory is None:
            self.parent_directory = './DownloadedBatches/'
        else:
            if save_directory[-1] != '/':
                save_directory += '/'
            self.parent_directory = save_directory
        makedirs(self.parent_directory, exist_ok=True)
        print('Using save directory {}'.format(self.parent_directory))
        # set up max batch size
        if max_batch_size is None:
            max_batch_size = 50 * 1024 * 1024
            print('Using max batch size of 50 MB.')
        # set up counters
        self.file_index = 0
        self.batch_number = 0
        # make batch_stats dict
        self.batch_stats = {}
        self.batch_stats['num_batches'] = 0

    def downloadBatch(self, key_size_df=None, dir_prefix=None):
        """
        Input:
        key_size_df : has Key / Size as columns with AWS S3 Key and object's
                      size in bytes, respectively. Populated by e.g. calling
                      s3Session.list_objects(Bucket='my-bucket').
        dir_prefix : what the batch folders will be called. By default,
                     the format for this is
                     ./save_directory/dir_prefix{{batch_number}}
        """
        if dir_prefix is None:
            dir_prefix = 'Batch'
        save_directory = self.parent_directory + dir_prefix
        # update the batch number
        self.batch_number += 1
        save_directory += '{:d}'.format(self.batch_number)

        # make save directory if it doesn't exist
        from os import makedirs
        makedirs(save_directory, exist_ok=False)

        size_downloaded = 0
        file_counter = self.file_index
        while True:
            current_key = key_size_df['Key'][file_counter]
            obj_name = current_key.split('/')[-1]
            obj_size = key_size_df['Size'][file_counter]
            self.download(Key=current_key,
                          Filename=save_directory + '/' + obj_name)
            file_counter += 1
            size_downloaded += obj_size
            if size_downloaded >= self.max_batch_size:
                out_str = 'Batch {}: downloaded {} files ' + \
                          'with total size {} bytes.'
                print(out_str.format(self.batch_number,
                                     file_counter - self.file_index,
                                     size_downloaded))
                break
        # Record statistics about files downloaded
        this_batch_stats = {'size': size_downloaded,
                            'num_files': file_counter - self.file_index,
                            'save_dir': save_directory}
        self.batch_stats[self.batch_number] = this_batch_stats
        return
