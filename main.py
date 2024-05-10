import xmltodict
import json
import re

"""
[郵便局データ](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-P30.html)から
郵便局名、住所、緯度経度を抽出する。

入力(参照)ファイル
  P30-13.xml 全国版データ
  pref_town_code.csvが市町村コード=>県/市変換テーブル
    [行政区域コード](https://nlftp.mlit.go.jp/ksj/gml/codelist/AdminiBoundary_CD.xlsx)
    excelで開いてcsvで出力して、utf-8に変換したファイル

出力ファイル
  post_office_loc.json  
    郵便局名、県、市、住所、緯度経度を要素とするオブジェクトの配列
  以下はファイル出力処理をコメントアウトしている。
#  code_to_pref_city.json
#    pref_town_code.csvから抽出
#    市町村コード文字列をキーとして、要素に、県,市を持つオブジェクト
#  P30-13*.json
#    .xmlをjsonに変換したオブジェクト
      
"""

if __name__ == '__main__':
    # 市町村コード=>県/市 変換テーブルを生成
    code_to_pref_city_obj = {}
    with open("pref_town_code.csv", encoding='utf-8') as f:
        # ヘッダ行は抜く
        for line in f.readlines()[1:]:
            [code_str, pref_str, city_str] = line.split(",")[:3]
            if re.match("[0-9]*", code_str) and 0 < len(city_str):
                code_to_pref_city_obj.update({
                    code_str:{
                        'pref':pref_str,
                        'city':city_str
                    }
                })

    # 市町村コード=>県/市 変換テーブルをファイルに出力しておく
#    with open("code_to_pref_city.json", mode="w", encoding='utf-8') as f:
#        json.dump(code_to_pref_city_obj, f, indent=2, ensure_ascii=False)


    # 郵便局情報のxmlファイルを読み込み、jsonに変換
    zenkoku = "P30-13.xml"
    kanagawa = "P30-13_14.xml"
    read_file_name = zenkoku
    with open(read_file_name, encoding='utf-8') as f:
        xml_str = f.read()
    master_data = xmltodict.parse(xml_str)

    # jsonをファイルに出力しておく
#    with open(read_file_name.replace(".xml",".json"), mode="w", encoding='utf-8') as f:
#        json.dump(master_data, f, indent=2, ensure_ascii=False)


    # マスタデータ前半のid-緯度経度情報を抽出しておく
    pos_tbl = {}
    for item in master_data["ksj:Dataset"]['gml:Point']:
        pos_tbl.update({item["@gml:id"]:item["gml:pos"]})


    # マスタデータから必要な情報だけを抽出
    results = []
    post_offices = master_data["ksj:Dataset"]["ksj:PostOffice"]
    print(f"{len(post_offices)} post offices is given.")
    for item in post_offices:
        # 名前から"郵便局"を除いて登録
        name = item["ksj:name"].replace("郵便局","")
        item_obj = {
            'name':name,
        }

        # 行政コードから、県、市をルックアップ
        code = item["ksj:administrativeArea"]["#text"]
        if code_to_pref_city_obj.get(code):
            pref_city = code_to_pref_city_obj.get(code)
            item_obj.update({
                'pref':pref_city["pref"],
                'city':pref_city["city"]
            })
        else:
            print(f"Can't find code to pref/city, code:{code}, name:{name}")
        item_obj.update({
            'address':item["ksj:address"],
        })

        # 位置情報idから緯度経度をルックアップ
        key = item["ksj:position"]["@xlink:href"].replace("#","")
        if pos_tbl.get(key):
            lat_lon_str =  pos_tbl.get(key)
            [lat_str, lon_str] = lat_lon_str.split()
            item_obj.update({
                'lon':float(lon_str),
                'lat':float(lat_str)
            })
        else:
            print(f"Can't find pos, pos_id:{key}, name:{name}")

        results.append(item_obj)

    print(f"{len(results)} post offices is converted.")

    with open("post_office_loc.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
