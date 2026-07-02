/****************************************
    タイトルメニュー
****************************************/
// メニュー決定処理
function executeMenu() {

    const action = menuItems[selectedIndex].dataset.action;
    sessionStorage.setItem('prevPage', location.pathname);

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