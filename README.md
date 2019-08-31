# DNAストレージシステム
## 自身が大学生時代に実装したシステム

## ソース
https://www.ebi.ac.uk/sites/ebi.ac.uk/files/groups/goldman/file2features_2.0.pdf

あらゆるコンピュータファイルをDNAデータへと変換して保存する。
本スクリプトはエンコード部分とデコード部分の一部のみ記載。
実験時はエンコード⇨MetaSimソフトでのDNAシーケンサーシミュレート⇨エラー訂正＋デコードを行った。

## 実行方法
python GoldmanMethod.py <変換したいファイル>
⇨引数に指定したファイルと同フォルダにハフマン符号化テキストファイルとDNAデータに変換した.fastaファイルが生成される。
