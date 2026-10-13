# 広重『東海道五十三次』44作品：史実・評価中心の全面改稿（2.3.5）

現行アプリ収録の保永堂版44作品について、鑑賞解説をすべて書き直した。保永堂版全55図のうち、収録済み44点が対象。未収録11図は追加していない。

## 編集方針
- 美術館の作品解説で確認できる構図や評価、宿場の歴史、交通制度、商業、参詣、祭礼などを優先する。
- 伝承は史実と区別し「伝説」「伝承」と明示する。
- 旅人の心理、作者の狙い、未知の制作事情を推測しない。
- 保永堂版の成立年代と掲載個体の摺り・復刻年代を混同しない。
- 改稿対象は data/hizakurige.json の images.hiroshige-0 ～ hiroshige-43、計44項目。
- js/app.js の表示見出しを「作品の評価と歴史背景」に変更し、作品別の解説典拠へのリンクを付した。
- 歩行記録と読了記録の保存キー「aruku-nihon-kiko-v2」は変更しない。

## 主要な参照資料
MOA美術館『広重「東海道五十三次」 Digital Remix 作品解説』保永堂版全55図
https://www.moaart.or.jp/hiroshigedigital-remix1/

MOA美術館『歌川広重 東海道五十三次』
https://www.moaart.or.jp/event/hiroshiges-fifty-three-stages-of-the-tokaido/

文化遺産オンライン『東海道五十三次』
https://online.bunka.go.jp/heritages/detail/96789

## 変更しない範囲
『東海道中膝栗毛』58篇の本文・原作挿絵、地図・旅程・地点、おくのほそ道、js/storage.js の歩行記録・読了管理処理。
