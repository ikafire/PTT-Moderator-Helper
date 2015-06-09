import count

def rule_6(article):
    sentence = "版規六: \n"
    violated = False

    if count.number_of_lines(article.signature) > 6:
        sentence += "文章簽名檔過長。刪除\n"
        violated = True
    
    artCharsCount = count.art_chars(article.body)
    tradCharsCount = count.traditional_chinese_chars(article.body)
    if artCharsCount > tradCharsCount:
        sentence += "內容含過多色碼、亂碼。刪除\n"
        violated = True

    simpCharsCount = count.simplified_chinese_chars(article.body)
    if simpCharsCount > tradCharsCount:
        sentence += "內容含過多非正體中文。退回並水桶三個月\n"
        violated = True

    return violated, sentence
        

def rule_9(article):
    sentence = "版規九: \n"
    violated = False

    if len(article.body) == 0:
        sentence += "空白文，退回並水桶六個月\n"
        violated = True

    tradCharsCount = count.traditional_chinese_chars(article.body)
    if tradCharsCount < 20:
        sentence += "發表內容之繁體中文字未滿二十個字，退回並水桶六個月\n"
        violated = True
    elif count.number_of_lines(article.body) <= 1:
        sentence += "滿二十個字，但使用電腦觀看為一行文，退回並水桶六個月\n"
        violated = True


    return violated, sentence


def main():
    import article
    articles = article.create_articles_from_file('data.json')
    for a in articles:
        violated, sentence = rule_6(a)
        if violated:
            print(a.title)
            print(a.body)
            print(sentence)
        violated, sentence = rule_9(a)
        if violated:
            print(a.title)
            print(a.body)
            print(sentence)


if __name__ == '__main__':
    main()
