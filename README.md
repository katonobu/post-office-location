# 郵便局位置情報抽出(Japanese only)
## 注意
参照しているデータは、非商用、再配布禁止なため、gitコミット対象外としています。
データ生成には別途データダウンロード等が必要です。
### 動かすまでのデータダウンロード/修正手順
#### P30-13.xmlの差し替え
1. [国土数値情報（郵便局データ)](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P30.html)を開く
1. 全国版データである、P30-13.zipをダウンロードする。
1. ダウンロードしたP30-13.zipを解凍して、そこに含まれるP30-13.xmlで、本ディレクトリ以下のP30-13.xmlを上書きする。

#### pref_town_code.csvの差し替え
1. [行政区域コード](https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx)をダウンロードする。
1. 「行政区域コード」シートをutf-8 csvでpref_town_code.csvに上書き。

## 参照データ出典
- 国土数値情報（[郵便局データ](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P30.html)）（国土交通省）（https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P30.html）（2024年5月10日取得）
  - 全国データ(P30-13.zip)中のP30-13.xmlをスクリプトから直接利用
  - 参照している属性情報
    - 位置
      - 緯度経度情報を抽出
    - 行政区域コード（P30_001）
      - 都道府県名、市区町村名を紐づけ
    - 名称（P30_005）
      - 冗長な文字「郵便局」を削除して抽出
    - 所在地（P30_006）
      - そのまま抽出

- [行政区域コード](https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx)
  - 当該ファイルの「行政区域コード」シートをutf-8 csvでpref_town_code.csvに上書き。
  - 郵便局データ中に含まれる行政区域コードをキーとしてこのデータを参照し、対応する都道府県名、市区町村名を抽出。

- [国土数値情報 利用規約](https://nlftp.mlit.go.jp/ksj/other/agreement_02.html)では、
  - 郵便局データは非商用、複製物の再配布禁止のためコミット対象外。

## 生成データ
- 上記参照データを元にスクリプトで必要な情報のみを抽出。
  - `post_office_loc.json`
  - 利用規約に加工データの再配布が明示的に記載されていないため、コミット対象外。
- 郵便局データに含まれる郵便局名称、都道府県名、市区町村名、住所、緯度、経度
- 詳細データ構造はschema.jsonを参照のこと。

## 背景
- ゆうちょ銀行の振込状況を管理したい。
- ダウンロード可能なpdfからのtext抽出で、郵便局名はわかる。
- しかし、振込人は画像データに含まれる手書き文字。OCRでは厳しそう。。。。
- 振込人候補の住所はわかっているので、、、
  - 全振込人候補者の住所から緯度経度を推定する。
    - [Geocoding.jp API](https://www.geocoding.jp/api/)を使うとか、、
  - pdfから抽出した郵便局名から近い順に候補者を列挙/画像データを表示し、振込人の特定/記録を容易にしたい。。。
