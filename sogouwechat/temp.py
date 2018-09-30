import re

str = 'var publish_time = "2018-09-30" || "";'

print(re.match('^var\spublish_time\s=\s\"(.*?)\"', str).group(1))