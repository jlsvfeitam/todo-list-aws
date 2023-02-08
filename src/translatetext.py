import boto3


def translatetext(text, sourcelanguage, targetlanguage):
    translate = boto3.client(service_name='translate',
                             region_name='us-east-1',
                             use_ssl=True)
    resultTranslate = \
        translate.translate_text(Text=text,
                                 SourceLanguageCode=sourcelanguage,
                                 TargetLanguageCode=targetlanguage)
    print('text in translatetext:', resultTranslate.get('TranslatedText'))
    return resultTranslate.get('TranslatedText')
