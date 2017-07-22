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
            exist_warning = 'Warning: the file {} already exists: ' + \
                            'skipping download...'
            print(exist_warning.format(fn))
        else:
            s3_anon.download_file(Bucket='bcsa-data',
                                  Key=key,
                                  Filename=target+'/'+key)
    return


def getAwsKeypair(directory=None):
    """
    getAwsKeypair expects two files named access.key and secret.key located in
    directory
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


def startS3SignedSession(access_key, secret_key,
                         region='ca-central-1'):
    import boto3
    s3_signed = boto3.client('s3',
                             region_name=region,
                             aws_access_key_id=access_key,
                             aws_secret_access_key=secret_key)
    return s3_signed


def listSubfolders(session, bucket, prefix, delimiter='/'):
    result = session.list_objects_v2(Bucket=bucket,
                                     Prefix=prefix,
                                     Delimiter=delimiter)
    return [o.get('Prefix') for o in result.get('CommonPrefixes')]


def listObjectKeys(session, bucket, prefix, delimiter='/'):
    result = session.list_objects_v2(Bucket=bucket,
                                     Prefix=prefix,
                                     Delimiter=delimiter)
    return [o.get('Key') for o in result.get('Contents')]


def getFileHierarchy(session, bucket, prefix, delimiter='/', verbose=True):
    subFolders = listSubfolders(session, bucket, prefix, delimiter)
    result = {sf.split('/')[-2]: None for sf in subFolders}
    num_keys = len(result.keys())
    for j, subfolderKey in enumerate(sorted(result.keys())):
        if verbose and ((j % 10) == 0):
            print('\rProportion complete: {}'.format(round(j/num_keys, 2)),
                  end='')
        result[subfolderKey] = listObjectKeys(session, bucket,
                                              prefix+subfolderKey+'/',
                                              delimiter)
    print('\rdone!')
    return result


def uploadLocalToS3(local_file_directory,
                    session, bucket, prefix,
                    verbose=True):
    """
    uploadLocalToS3(local_file_directory, session, bucket,
                    prefix, verbose[=True])
    is a function that crawls a file directory on the local machine and
    uploads files to a remote AWS bucket - preserving the directory
    structure - if it does not find a corresponding match on AWS.
    Input:
    local_file_directory : the local file directory in which
                           the files are found.
                 session : the s3 session that has valid upload permissions
                           (e.g., created using boto3)
                  bucket : the S3 bucket to which uploading will be done
                  prefix : the prefix for the bucket, where the files on
                           remote should be found
                 verbose : whether to be verbose while running.

    Note that this function was taylor made to upload directories
    where files are only stored in the leaves files in the leaves
    of a file hierarchy. Hence, it is good for uploading directory
    strucutres like the following, but would have to be adapted to
    accommodate others.
    Folder 1:
        Folder 1A:
            Folder 1AI:
                File 1AI11
                File 1AI12
                File 1AI13
            Folder 1AII:
                File 1AII11
                File 1AII12
                File 1AII13
                File 1AII14
            Folder 1AIII:
                File 1AIII11
        Folder 1B:
            File 1BI
            File 1BII
            File 1BIII
            File 1BIV
    Folder 2:
        .
        .
        .
    """
    import os
    if verbose:
        print('constructing local walk object')
    local_walk = os.walk(local_file_directory)
    if verbose:
        print('fetching remote directory structure')
    remote_hierarchy = getFileHierarchy(session, bucket, prefix,
                                        verbose=verbose)
    print('walking...')
    for sourceDir, folder_list, file_list in local_walk:
        if verbose:
            print('sourceDir: {}'.format(sourceDir))
        if len(folder_list) == 0:
            # then we're in a leaf
            folder_name = sourceDir.split('/')[-1]
            print('in leaf: {}'.format(folder_name))
            if folder_name in remote_hierarchy.keys():
                # okay so the folder exists, now search for missing files
                full_key_names = remote_hierarchy[folder_name]
                short_key_names = [x.split('/')[-1] for x in full_key_names]
                for file in (set(file_list) - set(short_key_names)):
                    print('uploading file: {}'.format(sourceDir + '/' + file))
                    print('to bucket {} as:'.format(bucket))
                    print('{}'.format(prefix + folder_name + '/' + file))
                    session.upload_file(sourceDir + '/' + file, bucket,
                                        prefix + folder_name + '/' + file)
            else:
                # create folder on remote
                if verbose:
                    print('uploading whole folder: {}'.format(folder_name))
                for file in file_list:
                    session.upload_file(sourceDir + '/' + file, bucket,
                                        prefix + folder_name + '/' + file)
        else:
            print('folder list was not empty')
    return


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
        self._download = partial(self.s3_session.download_file, Bucket=Bucket)
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
            self._download(Key=current_key,
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
        self._last_batch_dir = save_directory
        return

    def rmLastBatch(self, confirm=False):
        """
        rmLastBatch removes the batch last downloaded by the BatchDownloader
        instance.
        Input:
        confirm : if True, ask for confirmation from the user before removing
                  the batch
        """
        if confirm:
            msg = 'Are you sure you want to remove' + \
                  ' the batch that was last downloaded? (y/N) '
            verification = input(msg)
        else:
            verification = 'y'
        if verification == 'y':
            self._rm(self._last_batch_dir)
        return

    def _rm(folder):
        """
        Internal function to remove a folder and its contents.
        """
        import os
        import shutil
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        return
