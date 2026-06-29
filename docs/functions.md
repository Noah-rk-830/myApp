# functions.md

このドキュメントは、アプリ内の各JSファイルに含まれる関数・処理の一覧と役割をまとめたものです。

---

## 📁 ファイル構成

| ファイル | 役割 |
|---|---|
| `static/js/script.js` | 全ページ共通の処理 |
| `static/js/title.js` | タイトルページ（index.html）専用の処理 |

---

## static/js/script.js（全ページ共通）

### 処理1：Renderスリープ対策 ping
- **役割**：Renderの無料枠でサーバーがスリープしないよう、10分おきに `/ping` へGETリクエストを送る
- **実装**：`setInterval` + `fetch('/ping')`
- **間隔**：600,000ms（10分）

---

### 処理2：BFCache対策
- **役割**：ブラウザの戻る/進むで復元されたとき（BFCacheからの復元）に `initPage()` を再実行する
- **実装**：`window.addEventListener('pageshow', ...)`
- **条件**：`event.persisted` が `true` のとき（BFCacheからの復元時のみ）

---

## static/js/title.js（タイトルページ専用）

### 変数：menuItems
- **役割**：`#menuList` 内の `li` 要素を全て取得して保持する
- **実装**：`document.querySelectorAll("#menuList li")`

---

### 変数：selectedIndex
- **役割**：現在選択中のメニュー項目のインデックスを保持する
- **初期値**：`0`

---

### function updateSelection()
- **役割**：全メニュー項目から `selected` クラスを外し、`selectedIndex` の項目に `selected` クラスを付与して選択表示を更新する

---

### function executeMenu()
- **役割**：現在選択中のメニュー項目の `data-action` 属性を読み取り、対応するページへ遷移する
- **遷移先**：
  - `new` → `/new`
  - `load` → `/load`
  - `option` → `/option`
- **実装**：`location.replace()` を使用（履歴に残さない）

---

### キーボード操作（keydown イベント）
- **役割**：キーボードでメニューを操作する
- **操作**：
  - `ArrowUp`：`selectedIndex` を1つ減らす。0未満になった場合は末尾に折り返す
  - `ArrowDown`：`selectedIndex` を1つ増やす。末尾を超えた場合は0に折り返す
  - `Enter`：`executeMenu()` を呼び出して決定する
- **備考**：各キー操作で `e.preventDefault()` によりブラウザデフォルト動作をキャンセルする

---

### マウス操作（mouseenter / click イベント）
- **役割**：マウスでメニューを操作する
- **操作**：
  - `mouseenter`：カーソルが乗った項目の index を `selectedIndex` に設定し、`updateSelection()` を呼ぶ
  - `click`：`selectedIndex` を更新後、`updateSelection()` と `executeMenu()` を呼ぶ

---

### 初期表示
- **役割**：ページ読み込み時に `updateSelection()` を呼び出して初期選択状態を表示する


## 遷移方針

- アプリ内のページ遷移はすべて `location.replace()` で統一する
- `pushState` は使用しない
- ブラウザバックを押すとアプリ外に離脱する（デフォルト動作）
- 「タイトルへ戻る」はアプリ内ボタンで補う

---

## 更新履歴

| 日付 | 内容 |
|---|---|
| 2026-06-29 | 初版作成 |