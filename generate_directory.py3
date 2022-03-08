# coding: utf-8

from collections import namedtuple
import csv
import random
import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

INPUT_DATA = 'data.csv'
INPUT_TEMPLATE = 'template.html'
SWAPS_FILE = 'swaps.csv'
BLACKLIST_FILE = 'blacklist.csv'
DataRow = namedtuple(
	'DataRow',
	[
		'ttimestamp',
		'email',
		'name',
		'facebook',
		'linkedin',
		'twitter',
		'role',
		#'student_type',
		'first_time',
		'experience',
		'affiliation',
		'job_title',
		'gender',
		'country_ori',
		'country_resi',
		'bio_short',
		'bio_long',
		'picture',
		'secret_power',
		'secret_fact',
		'offline_hobby',
		'github',
		'itunes',
		'google_play',
		'preferred_pl',
		'preferred_frontend',
		'preferred_backend',
		'looking_for',
		'tech_interest',
		'topics',
		'my_idea',
		'ideation_talk_yes_no',
		'technical_talk_yes_no',
		'anything_else',
		'degree_pursiung',  # new fields start here
		'qc_skills',
		'qc_interests',
		'qc_hackathons_participate',
		'qc_language',
		'qc_hardware',
		'social_good_topic'])


"""
Loads a manual blacklist from 'blacklist.csv' for people who have been having problems with their profile pictures. Reason is that people without images must appear at the end of the website, otherwise it looks bad.
"""
def load_blacklist():
	blacklist = []
	try:
		with open(BLACKLIST_FILE) as blacklist_fp:
			for email in blacklist_fp:
				email = email.rstrip("\n\r")
				if email:
					print("INFO: blacklisting: %s.", email, file=sys.stderr)
					blacklist.append(email)
	except IOError as e:
		print("INFO: blacklist.csv file not found.", file=sys.stderr)
	return blacklist


"""
Loads a CSV file that contains <URL_FROM>,<URL_TO> for people who are having troubles getting the URL right, and the logic in this script deson't solve it
"""
def load_swaps():
	swaps = {}
	try:
		with open(SWAPS_FILE) as swaps_fp:
			reader = csv.reader(swaps_fp)
			for rawRow in reader:
				(src, dst) = rawRow
				dst = dst.rstrip("\n\r")
				swaps[src] = dst
	except IOError as e:
		print("INFO: swaps file not found.", file=sys.stderr)
	return swaps


def convertDataRow(rawRow):
	return DataRow(*rawRow)


def put_no_pictures_at_end(data, blacklist):
	result = []
	picture_ok = 0
	for row in data:
		if (not row.picture):
			result.append(row)
		elif (row.email in blacklist):
			result.append(row)
		else:
			picture_ok += 1
			result.insert(0, row)

	return result


def shuffle_participants(data):
	random.shuffle(data)
	return data


def mix_women_men(data, blacklist):
	women = [row for row in data if row.gender == 'Female']
	menAndDefault = [row for row in data if row.gender != 'Female']
	i = 0
	j = 0
	result = []
	while (i < len(women) and j < len(menAndDefault)):
		if women[i].email in blacklist:
			break
		if menAndDefault[i].email in blacklist:
			break
		result.append(women[i])
		result.append(menAndDefault[j])
		i += 1
		j += 1

	# put women with pictures
	while (i < len(women)):
		if women[i].email in blacklist:
			break
		result.append(women[i])
		i += 1

	# put mens with pictures
	while (j < len(menAndDefault)):
		if menAndDefault[i].email in blacklist:
			break
		result.append(menAndDefault[j])
		j += 1

	while (i < len(women)):
		result.append(women[i])
		i += 1

	while (j < len(menAndDefault)):
		result.append(menAndDefault[j])
		j += 1

	return result


def main():
	print("INFO: loading blacklist.", file=sys.stderr)
	blacklist = load_blacklist()

	print("INFO: loading swaps", file=sys.stderr)
	swaps = load_swaps()

	print("\n")
	print("INFO: loading people.", file=sys.stderr)
	users = []
	data = []
	with open(INPUT_DATA) as csvfile:
		reader = csv.reader(csvfile)
		#reader.next()
		next(reader)
		for rawRow in reader:
			row = convertDataRow(rawRow)
			data.append(row)

	data = shuffle_participants(data)
	data = put_no_pictures_at_end(data, blacklist)
	data = mix_women_men(data, blacklist)
	# data_copy = data[:picture_ok]
	# data_copy = shuffle_participants(data_copy)
	# data[:picture_ok] = data_copy

	for row in data:
			# We process Google Dirve images.
			profile_picture_url = row.picture
			if (profile_picture_url in swaps):
				profile_picture_url = swaps[profile_picture_url]

			profile_picture_url = profile_picture_url.replace(' ', '')
			if profile_picture_url.startswith('https://drive.google.com'):
				slices = profile_picture_url.split('/')
				if len(slices) == 7:
					profile_picture_url = 'https://drive.google.com/uc?export=view&id=' + slices[5]
				elif len(slices) == 4:
					profile_picture_url = 'https://drive.google.com/uc?export=view&id=' + profile_picture_url.split('=')[1]
				else:
					print("ERROR %s (%s) with image %s",row.name, row.email, row.picture, file=sys.stderr)

			user = {
				'name': row.name,
				'role': row.role,
				'affiliation': row.affiliation,
				'picture': profile_picture_url,
				'country_ori': row.country_ori,
				'country_resi': row.country_resi,
				'bio': row.bio_short,
				'secret_fact': row.secret_fact,
				'secret_power': row.secret_power,
				'looking_for': row.looking_for,
				'tech_interest': row.tech_interest,
				'offline_hobby': row.offline_hobby,
				'linkedin': row.linkedin,
				'github': row.github};
			users.append(user)


	from jinja2 import Environment, FileSystemLoader
	env = Environment(
		loader=FileSystemLoader("."),
		extensions=['jinja2.ext.with_'])
	template = env.get_template(INPUT_TEMPLATE)
	html = template.render({'users': users})
	print(html)
	print("\nCompleted!", file=sys.stderr)

main()
