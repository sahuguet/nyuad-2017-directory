# coding: utf-8

import csv
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

INPUT_DATA = 'data.csv'
INPUT_TEMPLATE = 'template.html'

"""
Loads a manual blacklist from 'blacklist.csv' for people who have been having problems with their profile pictures. Reason is that people without images must appear at the end of the website, otherwise it looks bad.
"""
def load_blacklist():
  blacklist = []
  try:
    with open('blacklist.csv') as blacklist_fp:
      for email in blacklist_fp:
        email = email.rstrip("\n\r")
        if email:
          print >> sys.stderr, "INFO: blacklisting: %s." % email
          blacklist.append(email)
  except IOError as e:
    print >> sys.stderr, "INFO: blacklist.csv file not found."
  return blacklist


print >> sys.stderr, "INFO: loading blacklist."
blacklist = load_blacklist()

print >> sys.stderr, "\n"
print >> sys.stderr, "INFO: loading people."
users = []
picture_ok = 0
with open(INPUT_DATA) as csvfile:
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
        if (not picture):
          data.append(row)
        elif (email in blacklist):
          data.append(row)
        else:
          picture_ok += 1
          data.insert(0, row)

    # shuffle people that have valid pictures. Otherwise the default order is least recently edited in Google Forms.
    data_copy = data[:picture_ok]
    random.shuffle(data_copy)
    data[:picture_ok] = data_copy

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
                print >> sys.stderr, "ERROR %s (%s) with image %s" % (name, email, picture)

        users.append({
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
template = env.get_template(INPUT_TEMPLATE)
html = template.render({'users': users})
print html
print >> sys.stderr, "\nCompleted!"
