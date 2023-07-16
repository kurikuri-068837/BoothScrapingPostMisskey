## Table名一覧
- post
  - 取得, 投稿したデータを取る
- model_info
  - 違法商品検出のための有名アバターDB
  - ここに載っているショップ名が新しくアバターを発売した場合に自動追加できる機能を実装すること
- delete_note
  - 違法商品を掲載した投稿時間及びショップ名を記録しておくDB
  - ブラックリスト
  - 万が一優良商品を削除した場合の再投稿に備えて商品id, 商品名, ショップ名は保存

## メモ
- postのデータはdelete_noteのデータを持っているようにすること
- postのデータは取得開始時からのデータになるため注意すること
- model_infoの初期情報は事前に取得し構築すること
- model_infoの追加機能の実装を忘れないこと
- 3Dmodel以外の違法商品は手動削除にする予定のため, dbを何かしらの形で更新することができるようにしておくこと
- 投稿時刻はMisskey APIで取得できるか不明なため投稿直前にtime.time()で取得すること
- 削除機構を作る際, 投稿時間は誤差がある可能性を考慮すること
- 3Dmodelはdata-product-category="208"
- 正規化及びDB情報の取捨選択を実装前にもう一度行うこと


## 各テーブル構成

テーブル名 : post         
| カラム名     | データ型 | 最大文字数 | Null | 特記事項 | 説明 |
|:---         | :---:    | :---: | :---: | :---: | ---: |
| item_id     | INT      | AUTO_INCREMENT | NOT NULL | PRIMARY KEY | 商品id |
| item_name   | VARCHAR  | 100            | NOT NULL |             | 商品名 |
| shop_name   | VARCHAR  | 50             | NOT NULL |             | ショップ名 |
| category_no | INT      | 3              | IS NULL  |             | カテゴリNo 数字3桁 |
| img_md5     | CHAR     | 128            | IS NULL  |             | 画像ハッシュ値 128bit |
| posted_at   | DATETIME | YYYY-MM-DD hh:nn:dd | NOT NULL |  | misskeyへの投稿時刻 |

テーブル名 : model_info
| カラム名     | データ型 | 最大文字数 | Null | 特記事項 | 説明 |
|:---         | :---:    | :---: | :---: | :---: | ---: |
| item_id     | INT      | AUTO_INCREMENT | NOT NULL | PRIMARY KEY | 商品id |
| item_name   | VARCHAR  | 100            | NOT NULL |             | 商品名 |
| shop_name   | VARCHAR  | 50             | NOT NULL |             | ショップ名 |
| img_md5     | CHAR     | 128            | IS NULL  |             | 画像ハッシュ値 128bit |

テーブル名 : delete_note
| カラム名     | データ型 | 最大文字数 | Null | 特記事項 | 説明 |
|:---         | :---:    | :---: | :---: | :---: | ---: |
| item_id     | INT      | AUTO_INCREMENT | NOT NULL | PRIMARY KEY | 商品id |
| item_name   | VARCHAR  | 100            | NOT NULL |             | 商品名 |
| shop_name   | VARCHAR  | 50             | NOT NULL |             | ショップ名 |
| posted_at   | DATETIME | YYYY-MM-DD hh:nn:dd | NOT NULL |  | misskeyへの投稿時刻 |
