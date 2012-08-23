# coding: utf-8
import os
import sys
import tarfile
import subprocess
import json
import hashlib
import shutil

from ubik_toolbelt.logger import stream_logger

archs = ['noarch', 'x86_64', 'i386']
dist = ['nodist', 'debian', 'centos', 'darwin', 'ubuntu', 'redhat', 'archlinux']
packages_list = 'Packages.list'
packages_json = 'Packages.json'

def create(repo_name):

	if os.path.exists(repo_name):
		stream_logger.info(' :: Dir already exist')
		sys.exit(1)

	stream_logger.info(' :: Create repositorie structure')
	os.makedirs(repo_name)
	os.chdir(repo_name)
	open('.repo_root', 'w').close

	stream_logger.info(' :: Create default "stable" branch and two examples')
	os.makedirs('stable')
	os.makedirs('stable/noarch/nodist/novers')
	os.makedirs('stable/x86_64/debian/6')

def get_md5(path):
	fh = open(path, 'rb')
	m = hashlib.md5()
	while True:
		data = fh.read(8192)
		if not data:
			break
		m.update(data)
	return m.hexdigest()

def unarchiver(path, name):
	src = "%s/%s.tar" % (path, name)
	dst = "%s" % path

	# Open tarfile
	tar = tarfile.open(src)
	if tarfile.is_tarfile(src):
		tar.extractall(dst)
	else:
		raise Exception('Archive invalid (not a tarfile)')

def get_package_infos(path, name):
	infos = {}

	for info in ['name', 'version', 'release', 'description', 'requires']:
		cmd = ['. %s/%s/control; echo $%s' % (path, name, info.upper())]
		pipe = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell=True)
		infos[info] = pipe.communicate()[0].replace('\n', '')

		infos['arch'] = path.split('/')[0]
		infos['dist'] = path.split('/')[1]
		infos['vers'] = path.split('/')[2]
		infos['md5'] = get_md5(path + '/' + name + '.tar')
	return infos

def write_packages_json(infos):
	if os.path.exists(packages_json):
		os.remove(packages_json)

	json.dump(infos, open(packages_json, 'w'))

def write_packages_list(infos):
	if os.path.exists(packages_list):
		os.remove(packages_list)

	with open(packages_list, 'w') as packages_file:
		for package in infos:
			packages_file.write('%s|%s-%s||%s|%s|%s|%s|%s\n'
				% (	package['name'], package['version'],
					package['release'], package['md5'],
					package['requires'], package['arch'],
					package['dist'], package['vers']))

def clean(path, name):
	shutil.rmtree('%s/%s' % (path, name))

def generate(branches=False, old_format=False):
	if not os.path.exists('.repo_root'):
		stream_logger.info(' :: Need to be at repositorie root')
		sys.exit(1)

	if not branches:
		branches = filter(os.path.isdir, os.listdir('.'))
	elif not isinstance(branches, list):
		branches = [branches]

	for branch in branches:
		_json = []

		for (path, dirs, files) in os.walk(branch):
			if len(path.split('/')) == 1:
				stream_logger.info(' |_ %s' % path.split('/')[0])
			elif len(path.split('/')) == 2:
				stream_logger.info('   |_ %s' % path.split('/')[1])
			elif len(path.split('/')) == 3:
				stream_logger.info('     |_ %s' % path.split('/')[2])
			elif len(path.split('/')) == 4:
				stream_logger.info('       |_ %s' % path.split('/')[3])
				for package in files:
					if package[-4:] != '.tar':
						stream_logger.info('         |_ %s (ignored)' % package[:-4])
						continue
					package = package[:-4]
					stream_logger.info('         |_ %s' % package)
					unarchiver(path, package)
					_json.append(get_package_infos(path, package))
					clean(path, package)
		write_packages_json(_json)
		if old_format:
			write_packages_list(_json)
