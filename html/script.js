$(function() {
  // タブがクリックされた時
  $(".tab li").click(function() {
    // クリックされたタブの順番を変数に格納
    let index = $(".tab li").index(this);
    // クリック済みタブのデザインを設定したcssのクラスを一旦削除
    $(".tab li").removeClass("active");
    // クリックされたタブにクリック済みデザインを適用する
    $(this).addClass("active");
    // コンテンツを一旦非表示にし、クリックされた順番のコンテンツのみを表示
    $(".forms form").removeClass("show").eq(index).addClass("show");
  });
  
  // CSVファイルパス入力完了時
  $("#target_csv").blur(function() {
    // 入力チェック
    let csv_path = target_csv.value;
    // ファイル拡張子確認
    if ('.csv' != csv_path.slice(-4)) {
        // アラートを表示して処理を終了
        alert("ERROR：ファイルの拡張子が不正です。 path=" + csv_path);
        return;
    }

    // ASIN一覧取得処理呼び出し
    eel.getAsinTable(csv_path);
  });

  // 結果ファイル出力先入力時
  $(".output_destination").blur(function() {
    let value = this.value
    // 入力情報を全タブに反映
    let output_destination = document.getElementsByClassName("output_destination");
    for (let i = 0; i < output_destination.length; i++) {
      output_destination[i].value = value;
    }
  });

  // 情報抽出ボタン（URL検索）クリック時
  $("#url_button").click(function() {
    // 入力値取得
    let input_list = []
    input_list[0] = target_url.value;
    let output_directory = document.getElementsByClassName("output_destination");
    input_list[1]  = output_directory[0].value;
    // 入力チェック
    if (input_list[0] == "") {
      alert("ERROR：URLが入力されていません");
    } else if (input_list[1] == "") {
      alert("ERROR：結果ファイル出力先が入力されていません");
    } else {
      // 商品情報抽出処理呼び出し
      eel.startAmazonResearch("url", input_list);
    }
  });

  // 情報抽出ボタン（ランキング検索）クリック時
  $("#ranking_button").click(function() {
  });

  // 情報抽出ボタン（キーワード検索）クリック時
  $("#keyword_button").click(function() {
  });

  // 情報抽出ボタン（ASIN検索）クリック時
  $("#asin_button").click(function() {
  });

  // 追加 or 除外ボタンクリック時
  $('.update_asin_button').click(function() {
  });

  // ASIN一覧表示処理
  eel.expose(displayAsinTable)
  function displayAsinTable(asin_list) {
    // ASIN一覧を削除
    $('#add_table').remove()
    // ASIN一覧のHTML作成
    var asin_list_html = "<div id='add_table'><p class='form_text'>■ ASIN/ISBN-13一覧</p><table id='asin_table'><tr><th id='asin_width'>ASIN/ISBN-13</th><th id='product_width'>製品名</th><th></th></tr>";
    for (let i = 0; i < asin_list.length; i++) {
      asin_list_html = asin_list_html + "<tr><td>" + asin_list[i][0] + "</td><td>" + asin_list[i][1] + "</td><td><button class='update_asin_button' type='button' value='" + i + "'>除外</button></td></tr>";
    }
    asin_list_html = asin_list_html + "</table><div id='add_form'><input id='add_asin' type='text' placeholder='ASIN/ISBN-13を追加できます'><button class='update_asin_button' type='button' value='add'>追加</button></div></div>";
    // ASIN一覧を出力
    $(asin_list_html).appendTo($('#asin_table_box'));
  }

  // アラート表示処理
  eel.expose(displayAlert)
  function displayAlert(alert_txt) {
    alert(alert_txt);
  }

  // 入力値のリセット
  eel.expose(clearInputValue)
  function clearInputValue(id) {
    let target_id = document.getElementById(id);
    target_id.value = "";
  }
});