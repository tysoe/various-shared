"""
Lists an entire S3 bucket prefix.
"""
import sys, tempfile, os, boto3

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("""USAGE:
    python prefix-lister.py source-bucket-name source-bucket-prefix

Example:
    python prefix-lister.py 'els-demo-app-bucket' 'content/images'
""")
    
    bucket = sys.argv[1]
    prefix = sys.argv[2]

    s3 = boto3.client('s3')
    marker = ''
    key_count = 0
    global_key_count = 0
    file_count = 1
    file = tempfile.NamedTemporaryFile(mode='w+t', encoding='UTF-8')

    while marker is not None:
        list_response = s3.list_objects(
            Bucket=bucket,
            Marker=marker,
            Prefix=prefix
        )

        if 'Contents' in list_response:
            for result in list_response['Contents']:
                print(f"{result['Key']}")
                key_count += 1
                global_key_count += 1
            
            marker = list_response['Contents'][-1]['Key']
        else:
            # Completely finished
            marker = None
