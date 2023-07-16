Table名
- post
- model_info
- delete_note

テーブル構成 : post         
| カラム名     | データ型 | 最大文字数 | Null | 特記事項 | 説明 |
|:---         | :---:    | :---: | :---: | :---: | ---: |
| item_id     | INT      | AUTO_INCREMENT | NOT NULL | PRIMARY KEY | 商品id |
| item_name   | VARCHAR  | 100            | NOT NULL |             | 商品名 |
| shop_name   | VARCHAR  | 50             | NOT NULL |             | ショップ名 |
| category_no | INT      | 3              | IS NULL  |             | カテゴリNo 数字3桁 |
| img_md5     | CHAR     | 128            | IS NULL  |             | 画像ハッシュ値 128bit |
| posted_at   | DATETIME | YYYY-MM-DD hh:nn:dd | NOT NULL |  | misskeyへの投稿時刻 |

テーブル構成 : model_info
| カラム名     | データ型 | 最大文字数 | Null | 特記事項 | 説明 |
|:---         | :---:    | :---: | :---: | :---: | ---: |
| item_id     | INT      | AUTO_INCREMENT | NOT NULL | PRIMARY KEY | 商品id |
| item_name   | VARCHAR  | 100            | NOT NULL |             | 商品名 |
| shop_name   | VARCHAR  | 50             | NOT NULL |             | ショップ名 |
| category_no | INT      | 3              | IS NULL  |             | カテゴリNo 数字3桁 |
| img_md5     | CHAR     | 128            | IS NULL  |             | 画像ハッシュ値 128bit |

テーブル構成 : delete_note
| カラム名     | データ型 | 最大文字数 | Null | 特記事項 | 説明 |
|:---         | :---:    | :---: | :---: | :---: | ---: |
| item_id     | INT      | AUTO_INCREMENT | NOT NULL | PRIMARY KEY | 商品id |
| item_name   | VARCHAR  | 100            | NOT NULL |             | 商品名 |
| shop_name   | VARCHAR  | 50             | NOT NULL |             | ショップ名 |
| category_no | INT      | 3              | IS NULL  |             | カテゴリNo 数字3桁 |
| img_md5     | CHAR     | 128            | IS NULL  |             | 画像ハッシュ値 128bit |
| posted_at   | DATETIME | YYYY-MM-DD hh:nn:dd | NOT NULL |  | misskeyへの投稿時刻 |


## 今後正規化について考慮すること