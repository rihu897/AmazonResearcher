# Amazon情報抽出ツール

## 抽出可能項目
・商品名  
・商品URL  
・ASIN/ISBN-13  
・価格  
・在庫情報  
・お届け日時  
・出荷元  
・販売元  

## 抽出対象外、除外方法
・ダウンロード版："今すぐダウンロードできます" in driver.find_element_by_css_selector("#availability > span").get_attribute("textContent")で除外
・Kindle本：在庫情報取得時にエラー発生で除外可能
・Audibleストア：在庫情報取得時にエラー発生で除外可能
・プライムVideo：ページの構造が完全に違うため、エラー発生で除外
・デジタルミュージック：ページの構造が全く違うため、エラー発生で除外
・Android アプリストア：ページの構造が全く違うため、エラー発生で除外
・Alexaスキル：ページの構造が全く違うため、エラー発生で除外
・中古品（すべてのカテゴリ）

## その他仕様
・Amazonデバイス、Apple製品などASINが設定されてない製品はASINの取得をスキップする。(空文字)
・お届け日時が記載されていないページはお届け日時の取得をスキップする。(空文字)
・服などサイズ指定のあるものについては一番小さいサイズの情報が設定される。
・複数の業者が出品している商品については新品を最安値で出品している業者の情報が取得される。

## 追加予定
・ASIN/ISBN-13、ランキング、キーワードタグの処理(現在はURLしか動かない)
・マルチスレッド化(スレッド数も指定可能にしたい)
・中古品に対応させて新品or中古品のみを選択して調査可能にする。

## AmazonのHTML調査まとめ
### ----- 商品一覧取得処理用 ----------------------------
#### 商品名
・span > div > span > a:nth-of-type(1) > .p13n-sc-truncate-desktop-type2\n
・h2 > a > span\n

#### 商品URL
・span > div > span > a:nth-of-type(1)
・h2 > a

【メモ】
・ランキングページと検索ページでaタグの位置が異なる

### ----- 個別ページ情報取得処理用 -----------------------
#### 商品名、商品URL
・引数のリストから取得

#### 在庫情報
・#availability > span

#### お届け日時
・#ddmDeliveryMessage > b
・#ddmDeliveryMessage > div > b
・#ddmDeliveryMessage > div > span > b

#### ASIN、ISBN-13
・#productDetails_detailBullets_sections1 > tbody > tr > td
・#detailBullets_feature_div > ul > li > span:nth-of-type(?) > span:nth-of-type(2)

#### 価格
・#priceblock_ourprice
・#price_inside_buybox
・#newBuyBoxPrice
・#aod-price-1 > span > span.a-offscreen
・#tmmSwatches > ul > .selected > span > span > span > a > span:nth-of-type(2) > span:nth-of-type(1)

#### 出荷元
・#aod-offer-shipsFrom > div > div > div.a-fixed-left-grid-col.a-col-right > span
・#tabular-buybox-truncate-0 > span > span
・#merchant-info > a

#### 販売元
・#aod-offer-soldBy > div > div > div.a-fixed-left-grid-col.a-col-right > a
・#tabular-buybox-truncate-1 > span > span > a
・#merchant-info > a

【メモ】
・ページ構成はカテゴリで細かい違いはあるものの大体は以下のグループ単位で考えて現状は問題なさそう
①：DIY・工具・ガーデン、おもちゃ、スポーツ&アウトドア、ペット用品、ドラッグストア、パソコン・周辺機器、文房具・オフィス用品、家電&カメラ、楽器・音響機器、大型家電、車&バイク、食品・飲料・お酒、ベビー＆マタニティ
②：PCソフト、ゲーム、ホーム&キッチン、ジュエリー、ホビー、産業・研究開発用品、腕時計、ビューティー、ラグジュアリー
③：本、洋書、DVD、ミュージック、クラシック
④：ファッション、シューズ＆バッグ、服＆ファッション小物
・在庫情報が「出品者からお求めいただけます。」のページの「すべての出品を見る」ボタンはページを開いてすぐにクリックした場合と少し待ってからクリックした場合で動作が変化する。

### その他
・中古品対応時のためのURLメモ
https://www.amazon.co.jp/%E4%B8%AD%E5%8F%A4%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3-%E3%83%87%E3%82%B9%E3%82%AF%E3%83%88%E3%83%83%E3%83%97-DELL-OptiPlex-7010/dp/B07ZQ5634P/ref=sr_1_24?dchild=1&fst=as%3Aoff&qid=1607196036&refinements=p_n_feature_twelve_browse-bin%3A3662535051%2Cp_89%3ADell%2Cp_72%3A2150400051&rnid=2150399051&s=computers&sr=1-24
