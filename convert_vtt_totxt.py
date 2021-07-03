#!/usr/bin/python
vttfileName = 'New-ways-to-get-started-with-Azure-Database-for-PostgreSQL_en.vtt'
textfileName = 'New-ways-to-get-started-with-Azure-Database-for-PostgreSQL_en.txt'
newlines = []
bad_words = '-->'
with open(vttfileName, 'r') as oldfile:
    for line in oldfile:
        if not(bad_words in line):
            newlines.append(line.replace('\r\n',''))
# print(newlines)

# 
with open(textfileName, 'w') as newfile:
    tmpline = ''
    for newline in newlines:
        if not(newline.endswith('.')):
            tmpline = tmpline +' '+ newline
        else:
            tmpline = tmpline + newline + '\r\n'
            newfile.write(tmpline)
            tmpline = ''
