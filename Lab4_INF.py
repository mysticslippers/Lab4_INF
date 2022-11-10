"""
Лабораторная работа №4
Михайлов Дмитрий Андреевич
Группа P3118
Вариант №7
"""


def MainTask():
    import time
    starting = time.time()
    json_file = open('jsonMain.txt', 'w')
    json_file.write('{' + '\n' + '\t')
    with open('xml.txt', encoding='utf-8') as file:
        names = []
        count_of_blocks = 0
        count_of_options = 0
        for line in file:
            options = []
            for i in line:
                if i == '<' and (('/lesson' in line) or ('/day' in line) or ('/schedule' in line)):
                    line = ''

                if i == '<' and (('/lesson' not in line) and ('/day' not in line) and ('/schedule' not in line)):
                    line = line.replace('<', '"', 1)

                if i == 'n' and ('name' in line):
                    names.append('"_name": ' + line[line.find('=') + 1:line.find('>')])
                    line = '\t' + line[:line.rfind('n') - 1] + '>'

                if i == 'a' and ('audience=' and 'building=' in line):
                    options.append('"_audience": ' + line[line.find('=') + 1:line.find('b') - 1] + ',')
                    options.append('"_building": ' + line[line.rfind('=') + 1:line.find('/') - 1])
                    line = '\t' + line[:line.rfind('a') - 1] + '/>'

                if i == 't' and ('time=' in line):
                    options.append('"_time": ' + line[(line.find('=') + 1):line.find('/') - 1])
                    line = '\t' + line[:line.rfind('t') - 1] + '/>'

                if i == 'l' and ('lecturer=' in line):
                    options.append('"_lecturer": ' + line[line.find('=') + 1:line.find('/') - 1])
                    line = '\t' + line[:line.rfind('l') - 1] + '/>'

                if i == 'f' and ('format=' in line):
                    options.append('"_format": ' + line[line.find('=') + 1:line.find('/') - 1])
                    line = '\t' + line[:line.rfind('f') - 1] + '/>'

                if i == '/' and ('/>' in line):
                    line = line.replace('/>', '": {', 1)

                if i == '>' and ('/>' not in line):
                    line = line.replace('>', '": {', 1)

            json_file.write(line + "\n")
            if len(options) != 0:
                for option in options:
                    json_file.write('\t' * 5 + option + '\n')
                json_file.write('\t' * 4 + '},' + '\n')
                count_of_options += len(options)

                if count_of_options == 5:
                    count_of_options -= 5
                    json_file.write('\t' * 4 + names[1] + '\n')
                    names.pop(1)
                    json_file.write('\t' * 3 + '},')
                    count_of_blocks += 1

                    if count_of_blocks == 3:
                        json_file.write('\n')
                        json_file.write('\t' * 3 + names[0] + '\n')
                        for j in range(3):
                            json_file.write('\t' * (2 - j) + '}' + '\n')
    file.close()
    json_file.close()
    print('Результативное время работы программы №1 - {}.'.format(time.time() - starting))


def AdditionalTask1():
    import xml.etree.ElementTree as ET
    import time
    starting = time.time()
    json_file = open('jsonAdd1.txt', 'w')
    tree = ET.parse('xml.txt')
    root = tree.getroot()

    json_file.write('{' + '\n')
    json_file.write('\t' + '"' + root.tag + '": {' + '\n')
    json_file.write('\t' * 2 + '"' + root[0].tag + '": {' + '\n')

    for i in root[0]:
        json_file.write('\t' * 3 + '"' + i.tag + '": {' + '\n')
        for j in i:
            json_file.write('\t' * 4 + '"' + j.tag + '": {' + '\n')
            j = str(j.attrib).replace("'", '"').replace('{', '}').replace('}', '')

            if 'audience' in j:
                json_file.write('\t' * 5 + '"_' + j[1:j.index(',') + 1] + '\n')
                json_file.write('\t' * 5 + '"_' + j[j.index('b'):] + '\n')

            else:
                json_file.write('\t' * 5 + '"_' + j[1:] + '\n')
            json_file.write('\t' * 4 + '},' + '\n')
        json_file.write('\t' * 4 + '"_' + str(i.attrib).replace("'", '"').replace('{', '}').replace('}', '')[1:] + '\n')
        json_file.write('\t' * 3 + '},' + '\n')

    json_file.write('\t' * 3 + '"_' + str(root[0].attrib).replace("'", '"').replace('{', '}').replace('}', '')[1:len(str(root[0].attrib)) - 1] + '\n')

    for k in range(3):
        json_file.write('\t' * (2 - k) + '}' + '\n')

    json_file.close()
    print('Результативное время работы программы №2 - {}.'.format(time.time() - starting))


def AdditionalTask2():
    import time
    import re
    starting = time.time()
    json_file = open('jsonAdd2.txt', 'w')
    json_file.write('{' + '\n')
    with open('xml.txt', encoding='utf-8') as file:
        names = []
        count_of_options = 5
        count_of_blocks = 0
        for line in file:
            options = []
            if re.match(r'<schedule>', line):
                line = re.sub(line[line.index('<'):], '\t' + '"schedule": {' + '\n', line)

            if re.match(r'\s*<\w*\s\w*=', line):
                if 'name' in line:
                    names.append('"_name": ' + line[line.index('"'):line.index('>')])
                elif 'audience' in line:
                    options.append('"_audience": ' + line[line.index('"'):line.index('b') - 1] + ',')
                    options.append('"_building": ' + line[line.rindex('=') + 1:line.rindex('"') + 1])
                else:
                    options.append('"_' + line[line.index('<') + 1:line.index(' ')] + '": ' + line[line.index('"'):line.rindex('"') + 1])
                line = re.sub(line[line.index('<'):line.index('>') + 1], '\t' + '"' + line[line.index('<') + 1:line.index(' ')] + '": {', line)

            if re.match(r'\s*<lesson(\d)', line):
                line = '\t' * 3 + '"lesson' + line[line.index('n') + 1] + '": { ' + '\n'

            if re.match(r'\s*</\w*>', line):
                line = re.sub(line[line.index('<'):line.index('>') + 1], '', line)

            json_file.write(line)
            if len(options) != 0:
                for option in options:
                    json_file.write('\t' * 5 + option + '\n')
                json_file.write('\t' * 4 + '},' + '\n')
                count_of_options -= len(options)

                if count_of_options == 0:
                    count_of_options += 5
                    json_file.write('\t' * 4 + names[1] + '\n')
                    names.pop(1)
                    json_file.write('\t' * 3 + '},')
                    count_of_blocks += 1

                    if count_of_blocks == 3:
                        json_file.write('\n' + '\t' * 3 + names[0] + '\n')
                        for j in range(3):
                            json_file.write('\t' * (2 - j) + '}' + '\n')
    file.close()
    json_file.close()
    print('Результативное время работы программы №3 - {}.'.format(time.time() - starting))


MainTask()
AdditionalTask1()
AdditionalTask2()
