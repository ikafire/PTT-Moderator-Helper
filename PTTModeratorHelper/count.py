# -*- coding: utf-8 -*-

def traditional_chinese_chars(string):
    import zhon.cedict
    count = 0
    for char in string:
        if char in zhon.cedict.trad:
            count = count + 1
    return count


def simplified_chinese_chars(string):
    import zhon.cedict
    count = 0
    for char in string:
        if char in zhon.cedict.simp:
            count = count + 1
    return count


def number_of_lines(string):
    return string.lstrip('\n').rstrip('\n').count('\n') + 1


def art_chars(string):
    count = 0
    artFile = open('artchars.txt', 'r', encoding='utf-8')
    artChars = artFile.read()
    artFile.close()
    for char in string:
        if char in artChars:
            count = count + 1
    return count


def main():
    string = '我有九個繁體中文字!*# blabla，。'
    tradCount = traditional_chinese_chars(string)
    print('There\'re {} zhtw chars in {}'.format(tradCount, string))

    string = '\n第一行\n\n第三行\n第四行\n\n\n'
    lineCount = number_of_lines(string)
    print('There\'re {} lines in \n{}'.format(lineCount, string))

    string = '今天╳▋﹎—︳=︿﹣真不開勳'
    artCount = art_chars(string)
    print('There\'re {} art chars in {}'.format(artCount, string))


if __name__ == '__main__':
    main()
