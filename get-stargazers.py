#!/usr/bin/env python3
import sys
import urllib.request
import json
import csv
import time

PAUSE = 0.1

def main(argv):
  owner = argv[0]
  repo = argv[1]
  token = argv[2]

  print('Getting stargazers...')
  users = get_users(owner, repo, token)

  info = []

  print('Looking up user info...')
  info = get_info(users, token)

  if len(info) == 0:
    print('No users to lookup...exiting...')
    return

  csvf = open('stargazers.csv', 'w')
  csvw = csv.writer(csvf)

  header = info[0].keys()
  csvw.writerow(header)

  for i in info:
    csvw.writerow(i.values())

  csvf.close()
  print("File writen to 'stargazers.csv'")
  return

def get_users(owner, repo, token):
  users = []
  reading = True
  page = 0

  while reading:
    url = 'https://api.github.com/repos/'+str(owner)+'/'+str(repo) \
          +'/stargazers?page='+str(page)+'&access_token='+str(token)
    try:
      time.sleep(PAUSE)
      resp = urllib.request.urlopen(url)
      data = json.loads(resp.read())

      if data and len(data) > 0:
        for u in data:
          if u['login'] not in users:
            users.append(u['login'])
        print('Finished page '+str(page))
        page += 1
      else:
        reading = False

    except:
      print('Expception with URL... over rate limit?')
      reading = False

  print('Users found: '+str(len(users)))
  return users

def get_info(users, token):
  cnt = 1
  info = []

  for u in users:
    time.sleep(PAUSE)
    lookup = get_user_info(u, token)
    if lookup:
      info.append(lookup)
    if cnt % 10 == 0:
      print('Looked up '+str(cnt)+'/'+str(len(users))+' users')
    cnt += 1

  return info

def get_user_info(user, token):
  info = {}
  url = 'https://api.github.com/users/'+str(user)+'?access_token='+str(token)

  try:
    resp = urllib.request.urlopen(url)
    data = json.loads(resp.read())

    if data and len(data) > 0:
      return data
    else:
      return None

  except:
    print('Expception with URL... over rate limit?')
    return None

if __name__ == "__main__":
  if len(sys.argv) > 3:
    main(sys.argv[1:])
  else:
    print('Usage:')
    print('\t'+sys.argv[0]+' <owner> <repo> <token>')
