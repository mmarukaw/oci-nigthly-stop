# oci-nigthly-stop

夜間にOCIのインスタンスを停止します。
また、 ついでに Autonomous Database のライセンスモデルを BYOL に変更します。


## 停止対象のインスタンス

- コンピュート・インスタンス
- Autonomous Database
- Database (DBaaS)


## 前提条件
- oci python SDK
- Python 3 以上
- ocicli プロファイルが作成済みのこと `oci setup config` で作れます。


## 使い方

1. このリポジトリをクローンします

1. stop.py ファイルを開き、 # Specify your config file と書かれた箇所を環境に合わせて編集します。

1. 以下のコマンドで停止処理が実行されます
    `python3 stop.py`
    
1. ログなどは標準出力およびエラー出力に吐かれますので、必要に応じてログファイルにリダイレクトしてください。

1. Pythonのスケジューラーは使用していません。必要に応じて cron などで定期実行してください。

    (以下 毎日24時に実行する場合の設定例)
    `0 0 * * * cd /home/opc; python3 -u /home/opc/oci-nightly-stop/stop.py > /home/opc/log/stop_`date +\%Y\%m\%d-\%H\%M\%S`.log 2>&1`


## インスタンスを停止対象から除外したい場合

各インスタンスに、以下の Defined Tag を設定しておくことで、停止対象から除外することができます。

    - タグ・ネームスペース : control
    - タグ ： nightly_stop
    - タグの値 : false
    
エンドユーザー向けの設定方法のガイドは、https://github.com/mmarukaw/oci-nigthly-stop/blob/master/guide/howtoaddtags.md にありますので、こちらもご覧ください。
