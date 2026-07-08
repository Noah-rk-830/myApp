import random
import string
import streamlit as st

# ハードコード部分(初期値・選択肢の定義)
DEFAULT_CONVERT_RATIO = 0.1  # 変換させる文字数の割合の初期値(10%)
MODE_OPTIONS = {
  "記号に変換": "symbol",
  "文字化け": "mojibake",
}


def convert_random_chars_to_symbols(text, ratio, symbols):
  """
  テキスト中の文字をランダムに選び、指定した割合だけ記号(配列内からランダム選択)に置き換える

  Args:
    text (str): 変換対象のテキスト
    ratio (float): 変換する文字の割合(0.0〜1.0)
    symbols (list[str]): 置換候補となる記号の配列

  Returns:
    str: 一部の文字が記号に置き換えられたテキスト
  """
  chars = list(text)
  target_indices = [i for i, c in enumerate(chars) if not c.isspace()]
  convert_count = int(len(target_indices) * ratio)
  convert_indices = random.sample(target_indices, convert_count) if convert_count > 0 else []

  for i in convert_indices:
    chars[i] = random.choice(symbols)

  return "".join(chars)


def mojibake_text(text):
  """
  テキスト全体をUTF-8バイト列にエンコードし、それをShift-JISとして誤読(decode)した場合に
  再現される文字化け文字列に変換する

  テキスト全体をまとめて変換することで、実際の文字化け現象(前後の文字とバイト列がずれて
  結合することで起きる連続した誤読)を再現する

  変換できない(Shift-JISとして不正なバイト列になる)場合は、
  デコード可能な範囲まで変換し、残りは固定のフォールバック記号("�")に置き換える

  Args:
    text (str): 変換対象のテキスト

  Returns:
    str: 文字化けを再現した文字列
  """
  utf8_bytes = text.encode("utf-8")
  return utf8_bytes.decode("shift_jis", errors="replace")


def convert_random_chars_to_mojibake(text, ratio):
  """
  テキスト中の文字をランダムに選び、指定した割合の文字を対象として、
  対象文字を「連続する区間」にまとめたうえで、区間ごとにテキスト全体変換方式で
  「UTF-8バイト列をShift-JISとして誤読した場合の文字化け」に置き換える

  Args:
    text (str): 変換対象のテキスト
    ratio (float): 変換する文字の割合(0.0〜1.0)

  Returns:
    str: 一部の区間が文字化け文字列に置き換えられたテキスト
  """
  chars = list(text)
  target_indices = [i for i, c in enumerate(chars) if not c.isspace()]
  convert_count = int(len(target_indices) * ratio)

  if convert_count <= 0:
    return text

  convert_indices = set(random.sample(target_indices, convert_count))

  # 対象インデックスを「連続する区間」にまとめる
  ranges = []
  start = None
  for i in range(len(chars)):
    if i in convert_indices:
      if start is None:
        start = i
    else:
      if start is not None:
        ranges.append((start, i))  # [start, i)
        start = None
  if start is not None:
    ranges.append((start, len(chars)))

  # 区間ごとにテキスト全体をまとめて文字化け変換する
  result_parts = []
  cursor = 0
  for start, end in ranges:
    result_parts.append("".join(chars[cursor:start]))
    segment = "".join(chars[start:end])
    result_parts.append(mojibake_text(segment))
    cursor = end
  result_parts.append("".join(chars[cursor:]))

  return "".join(result_parts)


def convert_text(text, ratio, mode, symbols):
  """
  選択されたモードに応じてテキスト変換処理を振り分ける

  Args:
    text (str): 変換対象のテキスト
    ratio (float): 変換する文字の割合(0.0〜1.0)
    mode (str): 変換モード("symbol","mojibake")
    symbols (list[str]): 記号モード時に使用する記号の配列

  Returns:
    str: 変換後のテキスト
  """
  if mode == "symbol":
    return convert_random_chars_to_symbols(text, ratio, symbols)
  elif mode == "mojibake":
    return convert_random_chars_to_mojibake(text, ratio)
  else:
    raise ValueError(f"未対応のモードです: {mode}")


def render_app(default_ratio, mode_options, default_symbols):
  """
  Streamlit画面の描画と、入力テキストから変換結果を表示する処理をまとめたメソッド

  Args:
    default_ratio (float): 変換する文字の割合の初期値(0.0〜1.0)
    mode_options (dict): 表示名をキー、内部モード名を値とする辞書
    default_symbols (list[str]): 記号配列の初期値
  """
  st.title("テキスト変換ツール")
  st.caption("入力文字の一部をランダムに変換します")

  mode_label = st.selectbox("変換モードを選択", list(mode_options.keys()))
  mode = mode_options[mode_label]

  ratio_percent = st.slider("変換する文字の割合(%)", min_value=0, max_value=100, value=int(default_ratio * 100), step=1)
  ratio = ratio_percent / 100

  # 記号モード選択時のみ、記号配列を画面上で編集可能にする
  symbols_text = st.text_input(
    "使用する記号(カンマ区切り)",
    value=",".join(default_symbols),
    disabled=(mode != "symbol"),
  )
  symbols = [s for s in symbols_text.split(",") if s != ""] or default_symbols

  input_text = st.text_area("入力テキスト（改行OK）", height=200, placeholder="ここに変換したいテキストを入力してください")

  if st.button("変換する"):
    if input_text.strip() == "":
      st.warning("テキストが入力されていません")
    else:
      converted_text = convert_text(input_text, ratio, mode, symbols)
      st.subheader("変換結果")
      st.text_area("出力テキスト", value=converted_text, height=200)


# 呼び出し
render_app(DEFAULT_CONVERT_RATIO, MODE_OPTIONS, ["■","％","＆","＃","！"])