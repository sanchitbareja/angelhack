def parse(filename):
    """ Parses a file given a filename and returns an list 
    ready for impress.js
    """
    opened = open(filename, 'r')
    lines = strip_newlines(opened.readlines())
    two_list, body = list(), list() 
    title, bold, underline, italic, ordered_list, unordered_list = (False for _ in range(6))
    for index in range(len(lines)):
        lines[index] = lines[index].replace('#', '<h1>')
        lines[index] = lines[index].replace('_', '<u>')
        lines[index] = lines[index].replace('*', '<b>')
        lines[index] = lines[index].replace('~', '<i>')
        if lines[index][1:2] == '.':
            # They can only list up to the number 9 
            for i in range(1, 10):
                if lines[index][0] == str(i):
                    lines[index] = lines[index][:2].replace(str(i) + '.', '<li>') + lines[index][2:] + '</li>'
            if not ordered_list:
                lines[index] = '<ol>\n' + lines[index]
                ordered_list = True
        else:
            if ordered_list:
                lines[index] = '</ol>\n' + lines[index]
                ordered_list = False

        if lines[index][0] == '-':
            lines[index] = lines[index][:1].replace('-', '<li>') + lines[index][1:] + '</li>'

            if not unordered_list:
                lines[index] = '<ul>\n' + lines[index]
                unordered_list = True
        else:
            if unordered_list:
                lines[index] = '</ul>\n' + lines[index]
                unordered_list = False

        lines[index] = lines[index].replace('[', '')
        lines[index] = lines[index].replace(']', '</a>')
        lines[index] = lines[index].replace('{', '<a href="')
        lines[index] = lines[index].replace('}', '">')

        lines[index] += '\n'

        for c in range(len(lines[index])):
            if lines[index][c] == '<':
                if lines[index][c+1] == 'i':
                    if not italic:
                        italic = True
                    else:
                        lines[index] = lines[index][:c+1] + '/' + lines[index][c+1:]
                        italic = False
                if lines[index][c+1] == 'u':
                    if not underline:
                        underline = True
                    else:
                        lines[index] = lines[index][:c+1] + '/' + lines[index][c+1:]
                        underline = False
                if lines[index][c+1] == 'b':
                    if not bold:
                        bold = True
                    else:
                        lines[index] = lines[index][:c+1] + '/' + lines[index][c:]
                        bold = False
                if lines[index][c+1] == 'h':
                    if not title:
                        title = True
                    else:
                        lines[index] = lines[index][:c+1] + '/' + lines[index][c+1:]
                        title = False

    opened.close()
    try: 
        new_file = open('result.html', 'w')
        new_file.writelines(lines)
        new_file.close()
    except IOError:
        pass


    return lines


def strip_newlines(lines):
    """ Takes in a list of lines and strips newline characters, extra spaces
    and extra lines
    """
    stored = list()
    for line in lines:
        stored.append(line.strip())
    return list(filter(lambda line: len(line) > 0, stored))

if __name__ == '__main__':
    testing = parse('toaster_test.toast')
    for element in testing:
        # print element[0] + ":"
        # print element[1] + "\n"
         print element
