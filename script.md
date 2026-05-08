---
engine: name-name
chapter: 1
title: "オグラシア — name-name 機能ショーケース"
default_bgm: bgm.ogg
aspect_ratio: "16:9"
choice_style: "soft"
font_family: "Klee One, cursive"
---

## 1-1: ようこそ

[背景: title.png]
[BGM: bgm.ogg, フェード=800]
[暗転解除]

> ここはオグラシア。

> name-name エンジンの機能を一通り試せる、ささやかなショーケースです。

**ナレーター** (narrator/normal, 中央):
ようこそ、旅人さん。

**ナレーター** (narrator/normal, 中央):
このサンプルでは、漢字《かんじ》のルビ表示や、
場面転換、画面効果など、ひととおりの機能を体験できます。

**ナレーター** (narrator/normal, 中央):
｜美少女《びしょうじょ》戦士、参上！――こんなふうに、`｜` を使えば
漢字以外の文字にもルビを振れます。

[フォント: Hina Mincho, serif]
**ナレーター** (narrator/normal, 中央):
（このセリフは明朝体で表示されます。per-line でフォントを切り替えました。）

[フォント解除]
**ナレーター** (narrator/normal, 中央):
こうしてフォントを解除すれば、章の既定フォントに戻ります。

[ボイス: voice_hello.mp3]
**ナレーター** (narrator/normal, 中央):
このセリフには per-line の音声を仕込んであります。

そして、話者行を省くと、直前のキャラクターの継続セリフになります。

[SE: chime.wav]
[待機: 400]

**ナレーター** (narrator/normal, 中央):
さあ、何から見てみましょうか。

[選択]
- 立ち絵と表情の出し入れを見る → 1-2
- 立ち絵アニメを見る → 1-3
- 画面効果（シェイク・フラッシュ・フェード）を見る → 1-4
- ナレーションと枠なし演出を見る → 1-5
- BGM の停止とフェードを見る → 1-6
- フラグの状態を見る → 1-7
- エンディングへ → 1-9
[/選択]

## 1-2: 立ち絵と表情

[場面転換]
[背景: title.png]

**ナレーター** (narrator/normal, 左):
立ち絵は左・中央・右の 3 つの位置に配置できます。

**ナレーター** (narrator/normal, 右):
位置を変えるとフェードを伴わず、すっと移動します。

**ナレーター** (narrator/normal, 中央):
新規表示と退場には、デフォルトで 300ms のフェードが入ります。

**ナレーター** → smile:

**ナレーター** (narrator/smile, 中央):
表情だけを差し替えることもできます（`** 名前 ** → 表情:` 形式）。

[退場: ナレーター]

> ……（誰もいなくなった画面）

[待機: 400]

**ナレーター** (narrator/normal, 中央):
こうして、ふわっと戻ってこられます。

[フラグ: saw_characters = true]

[選択]
- メニューに戻る → 1-1
- 立ち絵アニメを見る → 1-3
[/選択]

## 1-3: 立ち絵アニメ

[場面転換]
[背景: title.png]

**ナレーター** (narrator/normal, 中央):
立ち絵には fire-and-forget のアニメーションも掛けられます。

[アニメ: target=ナレーター, x=+150, duration=600, easing=ease-out]

**ナレーター** (narrator/normal, 中央):
こうして横にスライドしたり……

[アニメ: target=ナレーター, x=-150, rotation=15, duration=800, easing=ease-in-out]

**ナレーター** (narrator/normal, 中央):
回転や、

[アニメ: 対象=ナレーター, 拡縮=1.2, 時間=400]

**ナレーター** (narrator/normal, 中央):
拡大／縮小もできます（属性は日本語キーも英語キーも受理します）。

[アニメ: target=ナレーター, scale=1, x=0, rotation=0, duration=600, easing=ease-out]

**ナレーター** (narrator/normal, 中央):
元の位置に戻しました。

[フラグ: saw_animate = true]

[選択]
- メニューに戻る → 1-1
- 画面効果を見る → 1-4
[/選択]

## 1-4: 画面効果

[場面転換]
[背景: title.png]

**ナレーター** (narrator/normal, 中央):
画面効果は 3 種類あります。

[シェイク: intensity=12, duration=500]
**ナレーター** (narrator/normal, 中央):
これがシェイク。

[待機: 300]

[フラッシュ: color=#ffffff, alpha=0.8, duration=300]
**ナレーター** (narrator/normal, 中央):
これがフラッシュ。

[待機: 300]

[フェード: target=all, color=#000000, from=0, to=0.6, duration=400]
**ナレーター** (narrator/normal, 中央):
そしてこれが、フェード。

[フェード: target=all, color=#000000, from=0.6, to=0, duration=400]

**ナレーター** (narrator/normal, 中央):
場面転換は `[暗転]` `[暗転解除]` `[場面転換]` で組み立てます。

[フラグ: saw_effects = true]

[選択]
- メニューに戻る → 1-1
- 枠なし演出を見る → 1-5
[/選択]

## 1-5: ナレーションと枠なし

[場面転換]
[背景: title.png]

**ナレーター** (narrator/normal, 中央):
通常のセリフは、半透明の黒い枠の中に出ます。

[退場: ナレーター]

[枠なし]
> 枠を外すと、画面いっぱいの字幕のように見せられます。

> 子供向け動画や、シネマティックな演出に向いています。

[枠あり]

**ナレーター** (narrator/normal, 中央):
こんなふうに、戻すこともできます。

[フラグ: saw_borderless = true]

[選択]
- メニューに戻る → 1-1
- BGM 制御を見る → 1-6
[/選択]

## 1-6: BGM の停止とフェード

[場面転換]
[背景: title.png]

**ナレーター** (narrator/normal, 中央):
BGM は `[BGM停止: フェード=N]` でフェードアウトできます。

[BGM停止: フェード=1500]

**ナレーター** (narrator/normal, 中央):
1.5 秒かけて止まりました。

[待機: 600]

[BGM: bgm.ogg, フェード=1000]

**ナレーター** (narrator/normal, 中央):
そしてフェードインで再開。

[SE: chime.wav, フェード=200]

**ナレーター** (narrator/normal, 中央):
SE もフェードイン指定が可能です。

[フラグ: saw_bgm_control = true]

[選択]
- メニューに戻る → 1-1
- フラグの状態を見る → 1-7
[/選択]

## 1-7: フラグと条件分岐

[場面転換]
[背景: title.png]

**ナレーター** (narrator/normal, 中央):
ここまでに見た章を、フラグで覚えています。

[条件: saw_characters]
**ナレーター** (narrator/normal, 中央):
立ち絵の章は、もう見ましたね。
[/条件]

[条件: saw_animate]
**ナレーター** (narrator/normal, 中央):
立ち絵アニメも体験済みです。
[/条件]

[条件: saw_effects]
**ナレーター** (narrator/normal, 中央):
画面効果の章も、ばっちりです。
[/条件]

[条件: saw_borderless]
**ナレーター** (narrator/normal, 中央):
枠なし演出も体験済み、と。
[/条件]

[条件: saw_bgm_control]
**ナレーター** (narrator/normal, 中央):
BGM 制御も把握しました。
[/条件]

**ナレーター** (narrator/normal, 中央):
このように、`[条件]` ブロックでフラグごとに表示を出し分けられます。
ネストもできます。

[選択]
- メニューに戻る → 1-1
- エンディングへ → 1-9
[/選択]

## 1-9: つづく

[場面転換]
[背景: title.png]

**ナレーター** (narrator/normal, 中央):
ご覧いただき、ありがとうございました。

> ……つづく。

[BGM停止: フェード=2000]
[暗転]
