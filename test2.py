from datetime import datetime, timedelta
import re

text = 'https://www.facebook.com/orangebusiness/?locale=ro_RO'
indx = text.find('?locale')
text = text[:indx]

print(text)