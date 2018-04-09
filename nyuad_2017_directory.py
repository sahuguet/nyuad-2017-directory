# coding: utf-8

import csv

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

USERS = []
with open('data.csv') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    for row in reader:
        (t,
            email,
            name,
            facebook,
            linkedin,
            twitter,
            role,
            first_time,
         experience,
         affiliation,
         gender,
         country_ori,
         country_resi,
         bio,
         picture,
         secret_power,
         secret_fact,
         offline_hobby,
         github,
         itunes,
         google_play,
         preferred_pl,
         preferred_frontend,
         preferred_backend,
         looking_for,
         tech_interest,
         topics,
         my_idea,
         ideation_talk_yes_no,
         technical_talk_yes_no,
         anything_else,
         job_title,
         excited_about,
         long_bio,
         empty,
         full_name_empty) = row
        # We process Google Dirve images.
        if picture.startswith('https://drive.google.com'):
            slices = picture.split('/')
            if len(slices) != 7:
                print >> sys.stderr, "ERROR for %s" % picture
                continue
            picture = 'https://drive.google.com/uc?export=view&id=' + slices[5]
        USERS.append({
            'name': name,
            'role': role,
            'affiliation': affiliation,
            'picture': picture,
            'country_ori': country_ori,
            'country_resi': country_resi,
            'bio': bio,
            'secret_fact': secret_fact,
            'secret_power': secret_power,
            'looking_for': looking_for,
            'tech_interest': tech_interest,
            'offline_hobby': offline_hobby,
            'linkedin': linkedin})


from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("."),
        extensions=['jinja2.ext.with_'])
template = env.get_template('nyu_ad_2017_directory_template.html')
html = template.render({'users': USERS})
print html
