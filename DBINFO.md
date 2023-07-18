## Table名一覧
- booth_item_info
  - Boothからスクレイピングしたデータを蓄積
  - 違法商品検出のため有名アバターをあらかじめ取得して放り込んでおく
- misskey_post
  - item_idをキーとしてmisskeyへ投稿した情報を記録
  - 削除フラグも管理
- poplar_model_shop
  - white_listに入っているショップがアバターを出品した際の検知に使用
- white_list
  - 違法商品検出のため有名アバターの情報の商品idを格納
- gray_list
  - 違法商品を掲載した投稿時間及びショップ名を記録しておくDB
  - ブラックリスト
  - 万が一優良商品を削除した場合の再投稿に備えて商品id, 商品名, ショップ名は保存

## メモ
- booth_item_infoのデータは取得開始時からのデータになるため注意すること
- booth_item_infoには初期情報として人気3Dmodelの情報を入れること
- 3Dmodel以外の違法商品は手動削除にする予定のため, dbを何かしらの形で更新することができるようにしておくこと
- 投稿時刻はMisskey APIで取得できるか不明なため投稿直前にtime.time()で取得すること
- 削除機構は後で実装方法を検討
- 投稿の自動削除方法はcode_test_and_memo.pyに記載があるため参照すること（note_idを使用）
- 3Dmodelはdata-product-category="208"


## 各テーブル構成

テーブル名 : booth_item_info         
| カラム名     | データ型  | 最大文字数      | Null     | 特記事項    | 説明 |
|:---         | :---:    | :---:          | :---:    | :---:       | ---: |
| item_id     | INT      | 11             | NOT NULL | PRIMARY KEY | 商品id |
| item_name   | VARCHAR  | 150            | NOT NULL |             | 商品名 |
| shop_name   | VARCHAR  | 100            | NOT NULL |             | ショップ名 |
| category_no | INT      | 11             | NOT NULL |             | カテゴリNo 数字3桁 |
| img_md5     | CHAR     | 128            | NOT NULL |             | 画像ハッシュ値 128bit |
| corrent_at  | DATETIME |                | NOT NULL | corrent_timestamp| 追加日時 |


テーブル名 : misskey_post
| カラム名     | データ型  | 最大文字数     | Null     | 特記事項     | 説明 |
|:---         | :---:    | :---:         | :---:    | :---:        | ---: |
| item_id     | INT      | 11            | NOT NULL | PRIMARY KEY1 | 商品id |
| note_id     | INT      | 11            | NOT NULL | PRIMARY KEY2 |ノートid|
| poted_at    | DATETIME |               | NOT NULL |              |投稿時間|
| deleted_flag| TINYINT  |               | NOT NULL | 0/1          |削除フラグ|

テーブル名 : poplar_model_shop
| カラム名     | データ型  | 最大文字数  | Null     | 特記事項     | 説明 |
|:---         | :---:    | :---:      | :---:    | :---:        | ---: |
| shop_name   | VARCHAR  |  100       | NOT NULL | PRIMARY KEY  | ショップ名|


テーブル名 : white_list
| カラム名     | データ型  | 最大文字数  | Null     | 特記事項    | 説明 |
|:---         | :---:    | :---:      | :---:    | :---:       | ---: |
| item_id     | INT      | 11         | NOT NULL | PRIMARY KEY | 商品id |


テーブル名 : gray_list
| カラム名     | データ型  | 最大文字数  | Null     | 特記事項    | 説明 |
|:---         | :---:    | :---:      | :---:    | :---:       | ---: |
| item_id     | INT      | 11         | NOT NULL | PRIMARY KEY | 商品id |

