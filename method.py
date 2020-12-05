import pandas as pd
import datetime
import urllib3
import os
import time
import re
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.select import Select

class Main:
    def __init__(self):
        self.csv_path = ""  # CSVファイルパス内部保持用変数

    ### Chromeを起動する関数
    def set_driver(self,driver_path,headless_flg):
        # Chromeドライバーの読み込み
        options = ChromeOptions()

        # ヘッドレスモード（画面非表示モード）をの設定
        if headless_flg==True:
            options.add_argument('--headless')

        # 起動オプションの設定
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
        #options.add_argument('log-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--incognito')          # シークレットモードの設定を付与

        # ChromeのWebDriverオブジェクトを作成する。
        return Chrome(executable_path=os.getcwd() + "\\" + driver_path,options=options)

    ### 対象ランキングページ表示処理
    def openRankingPage(self):
        print("対象ランキングページ")

    ### 対象検索ページ表示処理
    def openSearchPage(self):
        print("対象検索ページ")

    ### 商品一覧取得処理
    def getProductUrlList(self, url):
        # 商品URL一覧
        product_url_list = []
        # ドライバ起動
        driver = self.set_driver("chromedriver.exe",False)
        # ブラウザを開き、URLにアクセス
        driver.get(url)
        time.sleep(2)

        while True:
            # 商品名と商品ページURLを取得
            if url.startswith("https://www.amazon.co.jp/gp/"):
                # ランキングページの場合
                atag_list = driver.find_elements_by_css_selector("span > div > span > a:nth-of-type(1)")
            else:
                # 検索ページの場合
                atag_list = driver.find_elements_by_css_selector("h2 > a")

            for atag in atag_list:
                product_url = []
                # 商品名
                if url.startswith("https://www.amazon.co.jp/gp/"):
                    # ランキングページの場合
                    product_url.append(atag.find_element_by_class_name("p13n-sc-truncate-desktop-type2").get_attribute("textContent"))
                else:
                    # 検索ページの場合
                    product_url.append(atag.find_element_by_tag_name("span").get_attribute("textContent"))
                # 商品ページURL
                product_url.append(atag.get_attribute("href"))
                # 商品URL一覧に追加
                product_url_list.append(product_url)

            # トランザクション開始（※次のページの存在確認）
            try :
                # 次のページへのリンク
                next_page_url = driver.find_element_by_css_selector(".a-last > a").get_attribute("href")
                driver.get(next_page_url)
                time.sleep(1)
            except :
                # 次のページが存在しない為、ループを終了
                break

        # ブラウザを閉じる
        driver.close()
        # URLリストを返却
        return product_url_list

    ### 個別ページ情報取得処理
    def getProductsDetailInfo(self, url_list):
        # 個別ページ情報一覧
        product_info_list = []
        # ドライバ起動
        driver = self.set_driver("chromedriver.exe",False)
        # ブラウザを開き、URLにアクセス
        driver.get("https://www.amazon.co.jp/ref=nav_logo")
        time.sleep(1)
        # 1件ずつ情報を抽出
        for target_info in url_list :
            name = target_info[0]   # 商品名
            url = target_info[1]    # 商品ページURL
            stock_info = ""         # 在庫情報
            delivery_datetime = ""  # お届け日時
            asin = ""               # ASIN,ISBN-13
            price = ""              # 価格
            shipper = ""            # 出荷元
            distributor = ""        # 販売元

            # URLを開く
            driver.get(url)
            time.sleep(2)
            # トランザクション開始
            try :
                print("----------------------------------------------------------------------------------------------")
                print("商品名：" + name)

                # 服のサイズ選択がある場合に一番小さいサイズを選択する
                dropdown = driver.find_elements_by_css_selector("#native_dropdown_selected_size_name")
                if len(dropdown) > 0 :
                    select = Select(dropdown[0])
                    select.select_by_index(1)
                    time.sleep(2)
                
                # 定期おトク便の選択項目がある場合に通常の注文を選択する
                if len(driver.find_elements_by_css_selector("#buyNew_cbb")) > 0 :
                    driver.find_element_by_id("buyNew_cbb").click()

                # 在庫情報を取得
                stock_info = re.sub("\n","",driver.find_element_by_css_selector("#availability > span").get_attribute("textContent"))
                print("在庫情報：" + stock_info)

                # ダウンロード版を除外
                if stock_info == "今すぐダウンロードできます。" :
                    raise Exception
                
                # ASINまたはISBN-13を取得
                if len(driver.find_elements_by_css_selector("#productDetails_detailBullets_sections1 > tbody > tr")) > 0 :
                    reg_info_box = driver.find_elements_by_css_selector("#productDetails_detailBullets_sections1 > tbody > tr")
                    for reg_info in reg_info_box :
                        if "ASIN" in reg_info.find_element_by_tag_name("th").get_attribute("textContent") :
                            asin = re.sub("\n","",reg_info.find_element_by_tag_name("td").get_attribute("textContent"))
                            print("ASIN/ISBN-13：" + asin)
                            break
                else :
                    reg_info_box = driver.find_elements_by_css_selector("#detailBullets_feature_div > ul > li > span")
                    for reg_info in reg_info_box :
                        if "ASIN" in reg_info.find_element_by_css_selector("span:nth-of-type(1)").get_attribute("textContent") or "ISBN-13" in reg_info.find_element_by_css_selector("span:nth-of-type(1)").get_attribute("textContent"):
                            asin = reg_info.find_element_by_css_selector("span:nth-of-type(2)").get_attribute("textContent")
                            print("ASIN/ISBN-13：" + asin)
                            break

                # 出品者が複数存在する場合
                if stock_info == "出品者からお求めいただけます。" :
                    time.sleep(2)
                    # すべての出品を見るボタンをクリック
                    driver.find_element_by_id("buybox-see-all-buying-choices-announce").click()
                    time.sleep(2)
                    # 新品の出品のみに絞り込み
                    driver.find_element_by_id("aod-filter-string").click()
                    driver.find_element_by_css_selector("#new > div > label > i").click()
                    time.sleep(1)

                # お届け日時を取得
                if len(driver.find_elements_by_css_selector("#ddmDeliveryMessage > b")) > 0 :
                    delivery_datetime = re.sub("\n|^ +","",driver.find_element_by_css_selector("#ddmDeliveryMessage > b").get_attribute("textContent"))
                elif len(driver.find_elements_by_css_selector("#ddmDeliveryMessage > div > b")) > 0 :
                    delivery_datetime = re.sub("\n|^ +","",driver.find_element_by_css_selector("#ddmDeliveryMessage > div > b").get_attribute("textContent"))
                elif len(driver.find_elements_by_css_selector("#ddmDeliveryMessage > div > span > b")) > 0 :
                    delivery_datetime = re.sub("\n|^ +","",driver.find_element_by_css_selector("#ddmDeliveryMessage > div > span > b").get_attribute("textContent"))
                else :
                    pass
                print("お届け日時：" + delivery_datetime)

                # 価格を取得
                if len(driver.find_elements_by_css_selector("#priceblock_ourprice")) > 0 :
                    price = re.sub("\n|￥","",driver.find_element_by_id("priceblock_ourprice").get_attribute("textContent"))
                elif len(driver.find_elements_by_css_selector("#price_inside_buybox")) > 0 :
                    price = re.sub("\n|￥","",driver.find_element_by_id("price_inside_buybox").get_attribute("textContent"))
                elif len(driver.find_elements_by_css_selector("#newBuyBoxPrice")) > 0 :
                    price = re.sub("\n|￥","",driver.find_element_by_id("newBuyBoxPrice").get_attribute("textContent"))
                elif len(driver.find_elements_by_css_selector("#aod-price-1 > span > span.a-offscreen")) > 0 :
                    price = re.sub("\n|￥","",driver.find_element_by_css_selector("#aod-price-1 > span > span.a-offscreen").get_attribute("textContent"))
                else :
                    price = re.sub("\n|￥","",driver.find_element_by_css_selector("#tmmSwatches > ul > .selected > span > span > span > a > span:nth-of-type(2) > span:nth-of-type(1)").get_attribute("textContent"))
                print("価格：" + price)
                
                # 出荷元を取得
                if len(driver.find_elements_by_css_selector("#tabular-buybox-truncate-0 > span > span")) > 0 :
                    shipper = re.sub("\n","",driver.find_element_by_css_selector("#tabular-buybox-truncate-0 > span > span").get_attribute("textContent"))
                elif len(driver.find_elements_by_css_selector("#merchant-info > a")) > 0 :
                    shipper = re.sub("\n","",driver.find_element_by_css_selector("#merchant-info > a").get_attribute("textContent"))
                else :
                    shipper = re.sub("\n","",driver.find_element_by_css_selector("#aod-offer-shipsFrom > div > div > div.a-fixed-left-grid-col.a-col-right > span").get_attribute("textContent"))
                print("出荷元：" + shipper)

                # 販売元を取得
                if len(driver.find_elements_by_css_selector("#tabular-buybox-truncate-1 > span > span > a")) > 0 :
                    distributor = re.sub("\n","",driver.find_element_by_css_selector("#tabular-buybox-truncate-1 > span > span > a").get_attribute("textContent"))
                elif len(driver.find_elements_by_css_selector("#merchant-info > a")) > 0 :
                    distributor = re.sub("\n","",driver.find_element_by_css_selector("#merchant-info > a").get_attribute("textContent"))
                else :
                    distributor = re.sub("\n","",driver.find_element_by_css_selector("#aod-offer-soldBy > div > div > div.a-fixed-left-grid-col.a-col-right > a").get_attribute("textContent"))
                print("販売元：" + distributor)

                # 個別ページ情報リストに格納
                product_info_list.append([asin, name, price, delivery_datetime, shipper, distributor, url])
            except Exception as e:
                # 除外対象の商品の為、コンソールに情報を出力して処理をスキップ
                print(e)
                print("抽出対象外の商品のため処理をスキップしました。 商品名：{0}, URL：{1}".format(name,url))
        
        # ブラウザを閉じる
        driver.close()
        # 個別ページ情報リストを返却
        return product_info_list

    ### CSV出力処理
    def outputCsv(self,url,list):
        if url == self.csv_path :
            # ASIN/ISBN-13情報ファイル更新
            print("CSV更新")
        else :
            # 現在時刻を取得
            dt_now = datetime.datetime.now()    # 現在時刻
            path = url + "/{}.csv".format(dt_now.strftime("%Y%m%d_%H%M%S")) # 出力ファイルのパス

            # データフレームを作成し、個別ページ情報リストを格納
            df = pd.DataFrame(list,columns=["ASIN","商品名","価格","お届け日時","出荷元","販売元","商品ページURL"])
            # CSVファイルを出力
            df.to_csv(path, index=False)
            # 出力ファイルのパスを返却
            return path

    ### ASIN情報リスト取得処理
    def getAsinList(self, csv_path):
        try:
            # CSVファイルを読み込み、データをリストに格納
            self.csv_path = csv_path
            asin_list = pd.read_csv(self.csv_path, dtype=str, encoding='utf-8-sig').values.tolist()
            # ASIN情報リストを返却
            return asin_list
        except:
            # アラート用テキストを返却
            return "ERROR：対象のCSVファイルが見つかりません path=" + self.csv_path

    ### URLアクセス先確認処理
    def checkUrl(self, url):
        try:
            http = urllib3.PoolManager()
            http.request('GET', url)
            return True
        except:
            return False