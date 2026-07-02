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
            
    }, 600000); // 10分 = 10 * 60 * 1000 ミリ秒
    // }, 5000);
});
// BFCache対策（戻る/進むで復元されたときに初期化を再実行）
window.addEventListener('pageshow', function (event) {
    if (event.persisted) {
        initPage();
    }
});

const menuItems = document.querySelectorAll("#menuList li");

// 現在選択中のメニュー番号
let selectedIndex = 0;

// 選択表示更新
function updateSelection() {

    menuItems.forEach(item => {
        item.classList.remove("selected");
    });

    menuItems[selectedIndex].classList.add("selected");

}

// メニュー決定処理
function executeMenu() {

    const action = menuItems[selectedIndex].dataset.action;

    switch (action) {
        default:
            alert("メニューが指定されていません。");
    }
}

// キーボード操作
document.addEventListener("keydown", function (e) {

    switch (e.key) {
        case "ArrowUp":
            selectedIndex--;
            if (selectedIndex < 0) {
                selectedIndex = menuItems.length - 1;
            }
            updateSelection();
            e.preventDefault();
            break;

        case "ArrowDown":
            selectedIndex++;
            if (selectedIndex >= menuItems.length) {
                selectedIndex = 0;
            }
            updateSelection();
            e.preventDefault();
            break;

        case "Enter":
            executeMenu();
            e.preventDefault();
            break;
    }

});

// マウス操作
menuItems.forEach((item, index) => {

    // マウスを乗せたら選択
    item.addEventListener("mouseenter", function () {

        selectedIndex = index;
        updateSelection();

    });

    // クリックで決定
    item.addEventListener("click", function () {

        selectedIndex = index;
        updateSelection();

        executeMenu();

    });

});

// 初期表示
updateSelection();