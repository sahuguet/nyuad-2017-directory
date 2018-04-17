# coding: utf-8

import csv

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

USERS = []
with open('data.csv') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    data = []
    for row in reader:
        (
            t,
            email,
            name,
            facebook,
            linkedin,
            twitter,
            role,
            first_time,
            experience,
            affiliation,
            job_title,
            gender,
            country_ori,
            country_resi,
            bio_short,
            bio_long,
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
            anything_else) = row
        if (picture):
          data.insert(0, row)
        else:
          data.append(row)

    for row in data:
        (
              t,
              email,
              name,
              facebook,
              linkedin,
              twitter,
              role,
              first_time,
              experience,
              affiliation,
              job_title,
              gender,
              country_ori,
              country_resi,
              bio_short,
              bio_long,
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
              anything_else) = row
        # We process Google Dirve images.
        picture = picture.replace(' ', '')
        if picture.startswith('https://drive.google.com'):
            slices = picture.split('/')
            if len(slices) == 7:
                picture = 'https://drive.google.com/uc?export=view&id=' + slices[5]
            elif len(slices) == 4:
                picture = 'https://drive.google.com/uc?export=view&id=' + picture.split('=')[1]
            else:
                print >> sys.stderr, "ERROR for %s" % picture

        USERS.append({
            'name': name,
            'role': role,
            'affiliation': affiliation,
            'picture': picture,
            'country_ori': country_ori,
            'country_resi': country_resi,
            'bio': bio_short,
            'secret_fact': secret_fact,
            'secret_power': secret_power,
            'looking_for': looking_for,
            'tech_interest': tech_interest,
            'offline_hobby': offline_hobby,
            'linkedin': linkedin,
            'github': github})


from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("."),
        extensions=['jinja2.ext.with_'])
template = env.get_template('nyu_ad_2017_directory_template.html')
html = template.render({'users': USERS})
print html
