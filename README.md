# BoothScraping_PostMisskey

## 注意点
- もともと個人で計画性なしで拡張しながら作ったプログラムであるため冗長なコードが多くあります。過去の残骸も多く残っています。
- ほぼgithub初心者なのでコミットの打つ間隔、コミット名等わかりにくいところがあります。また、質問やpull requestsが来ても対応に時間がかかる場合があります。あらかじめご了承ください。

## 直近のメモ
- GCP以降失敗により直近のコミット（GCP移行のため、GCP用に24時間のプログラムから特定時間に実行させる形式へ変更）の内容は一時的に凍結

## 以後以下のものの実装を検討
- 冗長コードの削除
- boothでの大まかな取得時間のデータ蓄積を行うシステムの開発
- 違法商品を弾く仕組みの開発
- CSV以外での投稿した商品の商品番号管理（mysql等）　やるなら上と一緒に実装。

## 期待値が低いが実装を検討
- 再度GCPまたはHeroku等のクラウドサービスでの実行

## 実装予定だったが廃止したもの
- GUIでの遠隔操作の手法（tkinter）　複雑なうえ同期関係、バグ等で開発難航。そもそも使う意味が学習のためだったため、理由を失い廃止。
- GUIでの遠隔操作の手法（flask）　これによりsecure.pyは廃止の方向性で検討。

### apikey.pyの内容

#misskey instance
misskey_instance = "MISSKEYINSTANCE"

#api token
misskey_api_token = "APIKEY"  #発信Botが投稿する際に使用するAPIKEY
analysis_api_token = "APIKEY" #発信Botが投稿した情報を取得できるか検証する際に使用していたAPIKEY

secure_api_token = "APIKEY"   #もともとsecure.pyに使用していたアカウントのAPIKEY ※1つだけ別のアカウント
