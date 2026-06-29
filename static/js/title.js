/****************************************
    タイトルメニュー
****************************************/

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
        case "new":
            location.replace("/new");
            break;

        case "load":
            location.replace("/load");
            break;

        case "option":
            location.replace("/option");
            break;
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