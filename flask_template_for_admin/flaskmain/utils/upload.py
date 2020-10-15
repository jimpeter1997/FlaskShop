# -*- coding:utf8 -*-
import paramiko
# from tornado import template
from flask import render_template
import os

#全部变量，指定配置文件的模板为当前目录下的templates文件
# template_path=os.path.join(os.path.dirname(__file__), "templates")

#远程执行命令
def execute(server, port, username, password, shellcmd):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(server, port, username, password)
	stdin, stdout, stderr = ssh.exec_command(shellcmd)
	ssh.close()
	return stdout.readlines()

#上传文件
def upload(server, port, username, password, localfile, remotefile):
	t = paramiko.Transport((server, port))
	t.connect(username = username, password = password)
	sftp = paramiko.SFTPClient.from_transport(t)
	remotepath = remotefile
	localpath = localfile
	ret = sftp.put(localpath, remotepath)
	t.close()
	return ret

#下载文件
def download(server, port, username, password, remotefile, localfile):
	t = paramiko.Transport((server, port))
	t.connect(username = username, password = password)
	sftp = paramiko.SFTPClient.from_transport(t)
	remotepath = remotefile
	localpath = localfile
	ret = sftp.get(remotepath, localpath)
	t.close()
	return ret

#生成配置文件内容
def genconfigstring(configtemplate, configvalues):
    """
    configtemplate:  "nginx.template"  # 模板名称
    configvalues： dianing_nginx # 配置项 字典形式
    """
	global template_path
	# loader = render_template.Loader(template_path)
	# ret = loader.load(configtemplate).generate(**configvalues)
	#print ret
    ret render_template(configtemplate, context=configvalues)
	return ret


def genconfigfile(configfile, configtemplate, configvalues):
    """
    configfile: "test.nginx"	#要生成的配置文件名
    configtemplate:  "nginx.template"  # 模板名称
    configvalues： dianing_nginx # 配置项 字典形式
    """
	# configstring = genconfigstring(configtemplate, dianing_nginx)
    configstring = render_template(configtemplate, context=configvalues)
	fp_config = open(configfile, 'w')
	fp_config.write(configstring )
	fp_config.close()


if __name__ == "__main__":

	#配置项
	dianing_nginx = {
	'user' : 'www',
	'group' : 'www',
	'keepalive_timeout' : '3',
	'access_log' : '/data1/logs/access.log',
	'server_name' : 'www.dianying.at v.dianying.at',
	'www_root' : '/data/dianying/wwwroot/',
	}

	config_file = "test.nginx"	#要生成的配置文件名
	genconfigfile(config_file, "nginx.template", dianing_nginx)		#生成配置文件
	#上传配置文件至/root/nginx/目录下
	upload('192.168.100.200', 22, 'root', 'password', config_file, "/root/nginx/" + config_file)
	#从/root/nginx/下载配置文件test.nginx至本地的/tmp目录并保存为.bak文件
	download('192.168.100.200', 22, 'root', 'password', "/root/nginx/" + config_file, "/tmp/" + config_file + ".bak")
