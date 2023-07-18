import uuid
from misskey import Misskey as mk
from apikey import *
from datetime import datetime


Password = "testtest"

SecuretyID = uuid.uuid4()
misskey_api = mk(misskey_instance)
misskey_api.token = secure_api_token

a =  misskey_api.notes_create(text=f"{Password}c\n{SecuretyID}",visibility="specified")
# visibility="specified"は自分自身に投稿し、他の人には見えないようにするための物なので注意すること
print(a['createdNote']['id'])           #これでidの取得が可能
print(a['createdNote']['createdAt'])    #これで投稿時間の取得が可能(フォーマット　ISO 8601 形式[yyyy-MM-ddTHH:mm:ss])


b = misskey_api.notes_delete(note_id="9hbz4dyuu8") #ここにnote_idを指定するとプログラムから削除することができる
misskey_api.notes_create(text=f"{b}",visibility="specified") #消した場合の返り値はTrue
#そのidのノートがない場合以下のエラーが出るため例外処理を一応組み込んでおくこと
### エラー内容 ###

# misskey.exceptions.MisskeyAPIException: NO_SUCH_NOTE(490be23f-8c1f-4796-819f-94cb4f9d1630): No such note.

#################

#### 以下DBへ入れる投稿時間の修正コード
original_format = "%Y-%m-%dT%H:%M:%S.%fZ"
desired_format = "%Y-%m-%d %H:%M:%S"


datetime_obj = datetime.strptime(a['createdNote']['createdAt'], original_format)

formatted_string = datetime_obj.strftime(desired_format)

print(formatted_string)  