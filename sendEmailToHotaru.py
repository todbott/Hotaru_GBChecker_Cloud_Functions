import mailjet_rest
import os

MAILJET_API_KEY = os.environ['MAILJET_API_KEY']
MAILJET_API_SECRET = os.environ['MAILJET_API_SECRET']
MAILJET_SENDER = os.environ['MAILJET_SENDER']

def send_email(whichOne, z, s, t, m, u, a, bk):
    client = mailjet_rest.Client(
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')

    if (whichOne == "逆引きチェックの誤訳発見と後の再翻訳によって"):
        body = "<p>各位</p><p>お疲れ様です。トッドです。</p><p>表題の件につきまして、" + whichOne + "翻訳メモリを更新いたしました。</p><ul><li>変更になった文章数：" + str(u) + "</li><li>追加になった文章数：" + str(a) + "</li></ul><p>この案件と関連あるメイン翻訳メモリを近日中に更新を行ってからまた連絡致します。</p><p>以上です。よろしくお願いいたします。</p>"
    else:
        body = "<p>各位</p><p>お疲れ様です。トッドです。</p><p>表題の件につきまして、" + whichOne + "翻訳メモリを更新いたしました。</p><ul><li>変更になった文章数：" + str(u) + "</li><li>追加になった文章数：" + str(a) + "</li></ul><p>本社のサーバーにある「" + m + "」の翻訳メモリファイルは更新済になりました。</p><p>以上です。よろしくお願いいたします。</p>"
    
    data = {
        'Messages': [{
            "From": {
                    "Email": MAILJET_SENDER,
                    "Name": "メモリ更新サービス"
            },
            "To": [
                {
                    "Email": 'gillies@hotaru.ltd'
                },
                {
                    "Email": 'shirai@hotaru.ltd'
                },           
                {
                    "Email": 'fukuda@hotaru.ltd'
                },      
                {
                    "Email": 'ddg@hotaru.ltd'
                },        
                {
                    "Email": bk
                },
                {
                    "Email": 'r-hirokawa@hotaru.ltd'
                },
            ],
            "Subject": "【翻訳メモリ更新連絡】　" + z + " ・ " + s + "=>" + t, 
            "TextPart": body,
            "HTMLPart": body
        }]
    }      
    client.send.create(data=data) 

def cors_enabled_function(request):

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    else:

        if request_json and 'shinki_or_saihonyaku' in request_json:
            shinki_or_saihonyaku = request_json['shinki_or_saihonyaku']
            z = request_json['zuban']
            s = request_json['source']
            t = request_json['target']
            m = request_json['memory']
            u = request_json['updates']
            a = request_json['additions']
            bk = request_json['BorK']
            if (shinki_or_saihonyaku == 'shinki'):
                send_email("新規翻訳によって", z, s, t, m, u, a, bk)
            else:
                send_email("逆引きチェックの誤訳発見と後の再翻訳によって", z, s, t, m, u, a, bk)
            
        elif request_args and 'shinki_or_saihonyaku' in request_args:
            shinki_or_saihonyaku = request_args('shinki_or_saihonyaku')
            z = request_args('zuban')
            s = request_args('source')
            t = request_args('target')
            m = request_args('memory')
            u = request_args('updates')
            a = request_args('additions')
            bk = request_args('BorK')
            if (shinki_or_saihonyaku == 'shinki'):
                send_email("新規翻訳によって", z, s, t, m, u, a, bk)
            else:
                send_email("逆引きチェックの誤訳発見と後の再翻訳によって", z, s, t, m, u, a, bk)
        

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    returnString = {'message': 'I think it worked!'}
        
    
    return (returnString, 200, headers)
