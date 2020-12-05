import eel
import urllib3
import desktop
import method
from os import path

# htmlファイルのディレクトリ
app_name="html"
# htmlファイル名
end_point="view.html"
# ウィンドウのサイズ
size=(680,800)
# インスタンス
main = method.Main()
# ASIN情報リスト
asin_list = []

### 商品情報抽出処理
@ eel.expose
def startAmazonResearch(search_type, input_list):
    # 変数定義
    url = ""                # 抽出開始ページのURL
    output_directory = ""   # 結果ファイル出力先
    url_list = []           # 商品個別ページのURLリスト
    product_info_list = []  # 情報抽出結果リスト

    # 検索種別判定
    if search_type == "ranking":
        # ランキング検索の場合
        print("ランキング検索")
    elif search_type == "keyword":
        # キーワード検索の場合
        print("キーワード検索")
    elif search_type == "asin":
        # ASIN検索の場合
        print("ASIN検索")
    else:
        # 入力リストの値を各変数に格納
        url = input_list[0]
        output_directory = input_list[1]
        # URLアクセス先確認処理呼び出し・結果判定
        if not main.checkUrl(url):
            # 戻り値がFalseの場合、アラート表示処理呼び出し
            eel.displayAlert("ERROR：URLアクセス先が見つかりません URL=" + url)
            return

    # 結果出力先ディレクトリ存在確認・結果判定
    if not path.exists(output_directory):
        # 戻り値がFalseの場合、アラート表示処理呼び出し
        eel.displayAlert("ERROR：結果ファイル出力先が見つかりません 結果ファイル出力先=" + output_directory)
        return

    # ASIN検索以外の場合、商品一覧情報取得処理呼び出し
    if search_type != "asin":
        url_list = main.getProductUrlList(url)

    # 個別ページ情報取得処理呼び出し
    product_info_list = main.getProductsDetailInfo(url_list)

    # 結果出力先ディレクトリ存在再確認・結果判定
    if not path.exists(output_directory):
        # 戻り値がFalseの場合、アラート表示処理呼び出し
        eel.displayAlert("ERROR：結果ファイル出力先が見つかりません 結果ファイル出力先=" + output_directory)
        return

    # CSV出力処理呼び出し
    result = main.outputCsv(output_directory, product_info_list)

    # アラート表示処理呼び出し
    eel.displayAlert("情報抽出が正常に終了しました。 結果ファイル=" + result)

### ASIN一覧取得処理
@ eel.expose
def getAsinTable(csv_path):
    # ASIN情報リスト取得処理呼び出し
    asin_list = main.getAsinList(csv_path)
    # エラー判定（アラート用テキストが返却された場合）
    if type(asin_list) is str :
        # アラート表示処理呼び出し
        eel.displayAlert(asin_list)
        # 入力フォームの値をリセット
        eel.clearInputValue("target_csv")
    else :
        # ASIN一覧表示処理呼び出し
        eel.displayAsinTable(asin_list)

# ASIN情報更新処理

# 画面生成処理呼び出し
desktop.start(app_name,end_point,size)