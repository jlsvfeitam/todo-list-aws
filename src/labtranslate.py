import boto3


def labtranslate(text):
    translate = boto3.client(service_name='translate',
                             region_name='us-east-1',
                             use_ssl=True)
    resultTranslate = translate.translate_text(Text=text, 
                                               SourceLanguageCode='en',
                                               TargetLanguageCode='es')
    print('text in language:', resultTranslate.get('TranslatedText'))
    return resultTranslate.get('TranslatedText')
