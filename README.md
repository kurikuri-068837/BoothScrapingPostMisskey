# BoothScraping_PostMisskey


## 注意点
- もともと個人で計画性なしで拡張しながら作ったプログラムであるため冗長なコードが多くあります。過去の残骸も多く残っています。
- ほぼgithub初心者なのでコミットの打つ間隔、コミット名等わかりにくいところがあります。また、質問やpull requestsが来ても対応に時間がかかる場合があります。あらかじめご了承ください。

## 直近のメモ
- GCP以降失敗により直近のコミット（GCP移行のため、GCP用に24時間のプログラムから特定時間に実行させる形式へ変更）の内容は一時的に凍結
- misskeyにおいて通報者（:emergency:）を送られた数が5以上の場合は通知を送付、10以上も何かしら検討 *一時凍結
- 画像をmd5のハッシュ値で管理及び照合を行い, 違法商品の判別を行う
- サイトのレスポンスヘッダーのみを一度取得し, 更新日時を確認, 
スクレイピングの有無を決めるシステムを実装することでboothの負荷を下げるシステムの開発（最優先）
- 投稿用のAPIと情報取得用のAPIを統合する方向で調整を行うこと
- コード検証用のファイルを作成. misskeyAPIの使いそうなコードが説明とともに記載されているため必要があれば参照すること
- エラー原因 定義する前にpostnote_threadを呼んでしまうことがある 以下エラーコード
  > Exception in thread Thread-1:
  > Traceback (most recent call last):
  >   File "C:\Users\username\Anaconda3\lib\threading.py", line 980, in _bootstrap_inner
  >     self.run()
  >   File "C:\Users\username\Anaconda3\lib\threading.py", line 917, in run
  >     self._target(*self._args, **self._kwargs)
  >   File "d:\programs\python\boothscraping_misskey\controller.py", line 98, in scraping_process
  >     postnote_thread.join()
  > UnboundLocalError: local variable 'postnote_thread' referenced before assignment
- エラー原因 その2
  ノートパソコンが自動的にwifiの方に接続してしまい接続不能になっていたが、そもそも有線lanの接続が切れてしまう原因が不明のためいったん保留


## 以後以下のものの実装を検討
- 冗長コードの削除
- boothでの大まかな取得時間のデータ蓄積を行うシステムの開発
- 違法商品を弾く仕組みの開発
- CSV以外での投稿した商品の商品番号管理（mysql等）　やるなら上と一緒に実装
- DBにアクセスをかけ内容を表示, 分析できるシステムの開発
- 再度GCPへの移行

## 期待値が低いが実装を検討
- 再度GCP,AWS,Heroku等のクラウドサービスでの実行(今回oracle系のサーバーで臨時稼働させており、期待値の格上げのため本項目の削除を予定)

## 実装予定だったが廃止したもの
- GUIでの遠隔操作の手法（tkinter）　複雑なうえ同期関係、バグ等で開発難航。そもそも使う意味が学習のためだったため、理由を失い廃止。
- GUIでの遠隔操作の手法（flask）　これによりsecure.pyは廃止の方向性で検討。

## apikey.pyの内容
apikey.py
>
>#misskey instance
>
>misskey_instance = "MISSKEYINSTANCE"
>
>
>#api token
>
>misskey_api_token = "APIKEY"  #発信Botが投稿する際に使用するAPIKEY
>
>analysis_api_token = "APIKEY" #発信Botが投稿した情報を取得できるか検証する際に使用していたAPIKEY
>
>secure_api_token = "APIKEY"   #もともとsecure.pyに使用していたアカウントのAPIKEY ※1つだけ別のアカウント
