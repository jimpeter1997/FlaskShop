from fdfs_client.client import Fdfs_client, get_tracker_conf



client_conf = get_tracker_conf('/home/alex/programs/client.conf')
print(client_conf)
for i in client_conf:
    print(i)
client = Fdfs_client(client_conf)

# client = Fdfs_client('/home/alex/programs/client.conf')
# ret = client.upload_by_filename('av.png')
ret = client.upload_by_filename('/home/alex/programs/FlaskShop/admin-flask/flaskmain/utils/fdfs/av.png')

print(ret)
