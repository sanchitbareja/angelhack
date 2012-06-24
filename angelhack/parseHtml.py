from slide import Slide
def parseHtml(text):
    """ 
    Parses a filename and adds the divs for impress.js
    """

    # opened = open(filename, 'r')
    linesToAdd = []
    # new_file = open('tryTest.html', 'w')
    # lines = opened.readlines()
    lines = text
    x, y, counter = 0, 0, 1
    currentBody = ''
    for index in range(len(lines)):
        # print lines[index]
        # print lines[index][0:4]
        # print '-----'
        # if (lines[index][0:4] == '<h1>'):
        if '<h1>' in lines[index]:
            if (currentBody != ''):
                slideObject = Slide(x, y, content=currentBody, title="slide-" + str(counter))
                counter += 1
                x += 1000
                print '------------'
                linesToAdd.append('<div id={0} class="step slide" data-x={2} data-y={3}>\n'.format(slideObject.title(), slideObject.format(), slideObject.x(), slideObject.y()))
                linesToAdd.append('<p>\n{0}\n</p>\n</div>\n'.format(slideObject.content()))
                currentBody = lines[index]
                continue
            else:
                currentBody += lines[index]
                continue
        else:
            currentBody += lines[index]
            continue
    if(currentBody != ''):
        slideObject = Slide(x, y, content=currentBody, title="slide-" + str(counter))
        counter += 1
        x += 1000
        linesToAdd.append('<div id={0} class="step slide" data-x={2} data-y="{3}">\n'.format(slideObject.title(), slideObject.format(), slideObject.x(), slideObject.y()))
        linesToAdd.append('<p>\n{0}\n</p>\n</div>'.format(slideObject.content()))
        currentBody = lines[index]
    # new_file.writelines(linesToAdd)
    # opened.close()
    # new_file.close()
    return linesToAdd

# if __name__ == '__main__':
#     testing = parseHtml('result.html')
#     for element in testing:
#         print element 
