// ページが読み込まれたら実行する
document.addEventListener("DOMContentLoaded", function() {
    console.log("共通スクリプト（script.js）が読み込まれました。");

    // 10分（600,000ミリ秒）ごとに自分自身（トップページ）にアクセスする関数
    setInterval(function() {
        console.log("スリープ回避のpingを送信中...");
        
        // 開いているサイトのルート「/」に対して、非同期でGETリクエストを送る
        fetch('/')
            .then(response => {
                if (response.ok) {
                    console.log("Ping成功: サーバーの生存を確認しました。");
                }
            })
            .catch(error => console.error("Ping失敗:", error));
            
    // }, 600000); // 10分 = 10 * 60 * 1000 ミリ秒
    }, 5000);
});