# 設問3の解答

## 環境

Python 3.6.9
pytest == 6.2.3

## 追加の仮定

初めてN回連続でタイムアウトしたとき，その時刻を故障した時間とみなす．

サーバが故障と過負荷の両条件を満たす場合は，故障であり，過負荷状態ではないとみなす．

pingのログがm回に満たない場合，過負荷か否かの判断をしない．

直近m回の平均応答時間がtミリ秒を初めて超えたとき，その時間から過負荷状態になっているとみなす．

直近m回のうち一回でもタイムアウトをしたとき，そのサーバを過負荷状態であるとみなす．

## テストの内容

`surveilance_q3_01.csv`

1つのサーバが一回だけping応答に失敗する場合のログ．mを変化させることで過負荷の検知時刻が変化する．

`surveilance_q3_02.csv`

サーバ`10.20.30.1/16`が最大1回連続でpingに対してタイムアウトし，サーバ`10.20.30.1/16`が最大2回連続でpingに対しタイムアウトする場合のログ．mを変化させることで過負荷の検知時刻が変化する．また，m=1の場合，サーバ`10.20.30.1/16`は過負荷状態から復帰する．

`surveilance_q3_03.csv`

どのサーバもping応答に失敗しない場合のログ．過負荷の閾値を下げることで`192.168.1.2/24`も過負荷状態と判断される．

## テストの結果

12 passed
