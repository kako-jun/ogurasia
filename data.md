---
engine: name-name
chapter: 1
title: "オグラシア — マスターデータ"
hidden: true
---

## data: マスター

[パーティ hero]
名前: ゆうしゃ
レベル: 1
HP: 20
MP: 4
ATK: 5
DEF: 3
AGI: 4
習得: Lv4 ホイミ
習得: Lv7 メラ
[/パーティ]

[モンスター slime]
名前: スライム
HP: 10
ATK: 3
DEF: 1
AGI: 2
EXP: 2
GOLD: 1
[/モンスター]

[モンスター ghost]
名前: ゴースト
HP: 14
ATK: 5
DEF: 2
AGI: 6
EXP: 4
GOLD: 3
[/モンスター]

[アイテム やくそう]
名前: やくそう
種別: 回復
価格: 8
効果: heal 30
[/アイテム]

[アイテム せかいじゅのしずく]
名前: せかいじゅのしずく
種別: 回復
価格: 0
builtin: world_tree_drop
[/アイテム]

[アイテム キメラのつばさ]
名前: キメラのつばさ
種別: その他
価格: 25
builtin: wing_of_chimera
[/アイテム]

[呪文 ホイミ]
名前: ホイミ
MP: 4
対象: 味方単体
効果: heal 15..25
[/呪文]

[呪文 メラ]
名前: メラ
MP: 2
対象: 敵単体
系統: fire
効果: damage 8..14 type=fire
[/呪文]

[呪文 ザラキ]
名前: ザラキ
MP: 8
対象: 敵全体
builtin: zaraki
[/呪文]

[呪文 ルーラ]
名前: ルーラ
MP: 8
対象: マップ
builtin: ruula
[/呪文]
