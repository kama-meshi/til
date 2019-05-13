# :memo: What is grib2

## Summary

- 気象情報を含むバイナリデータ
  - 国際気象通報式 FM92 GRIB 二進形式格子点資料気象通報式
（第２版）
  - 緯度経度を示す格子情報と気象情報を示すデータ情報が定義される

## データ形式について

第0 ~ 8節まで定義されておりそれぞれ下記の通り。

節|節名|概要
---|---|---
第0節|指示節|GRIB2形式であるという定義が記載
第1節|識別節|データの時刻情報
第2節|地域使用節|（不使用）
第3節|格子定義節|緯度経度情報を表す
第4節|プロダクト定義節|データの定義情報（なんのデータか）
第5節|資料表現節|データ圧縮の定義情報（このデータはどのように圧縮されているか）
第6節|ビットマップ節|このデータが格子の全データを持たない場合、どの点を利用するかという定義情報<br>格子全データを含む場合は「適用なし」となる
第7節|資料節|実際のデータが格納されている<br>格納順は第3節の格子の順になる
第8節|終端節|終了コード `7777` を格納

## データの取り扱い方法

wgrib2やecCodesなどのライブラリが有名なよう。

### wgrib2

アメリカ海洋大気庁 (NOAA) が開発しているライブラリ。
気象業務支援センターからもデコーダー (grib2_dec) が手に入る？
> wgrib2: https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/
> grib2_dec: http://www.eqh.dpri.kyoto-u.ac.jp/~masumi/sac/grib2.htm

#### wgrib2をMacで使う

ソースからコンパイルする (MacPortsで公開されていたようだが2019/04現在は`404`だった)  
Xcode付随のgccではコンパイルできないため、別途gccをインストールする必要あり。
（gccのバージョンが新しくなっているためmakefileなどの修正も必要）
> https://bovineaerospace.wordpress.com/2017/08/20/how-to-install-wgrib2-in-osx/


```
$ brew install gcc
$ alias gcc=/usr/local/bin/gcc-8
$ curl -o wgrib2.tgz https://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz
$ tar xzvf wgrib2.tgz
$ cd grib2
$ vim makefile
  : 以下をコメントアウトしフルパスに変更（/usr/local/bin/を付与）
  # export CC=gcc
  # export FC=gfortran
  : 以下をコメントアウト
  # export LDFLAGS="-L${lib}" && cd "${pngdir}" && export CPPFLAGS="${wCPPFLAGS}" && ${MAKE} -f scripts/makefile.darwin
  : --fast-mathを-ffast-math書き換え
  wCPPFLAGS+=-Wall -Wmissing-prototypes -Wold-style-definition -Werror=format-security --fast-math -O3
$ tar -xvf libpng-1.2.57.tar.gz
$ cd libpng-1.2.57/scripts/
$ vim makefile.darwin
  : CC=ccを以下に変更
  CC=/usr/local/bin/gcc
$ cd ../../
$ tar -cf libpng-1.2.57.tar libpng-1.2.57
$ gzip libpng-1.2.57.tar
$ export CC=/usr/local/bin/gcc-8
$ export CXX=/usr/local/bin/g++-8
$ export F77=/usr/local/bin/gfortran
$ export CFLAGS="-O2 -m64"
$ export CXXFLAGS="-O2 -m64"
$ export FFLAGS="-O2 -m64"
$ make
```

### ecCodes

ECMWF (ヨーロッパ中期予報センター) のecCodesも開発が盛んで利用しやすそう。  
Betaだがpythonインターフェイスなども用意されていた。
> ecCodes: https://confluence.ecmwf.int/display/ECC/ecCodes+Home
> eccodes-python: https://github.com/ecmwf/eccodes-python

#### DockerでecCodesを利用する

Debian系向けにパッケージが公開されているのでapt-getでecCodesが取得でき環境構築しやすい。  
dockerでインストールすると特に楽。

``` sh
$ sudo apt-get update
$ sudo apt-get install libeccodes0
$ pip install eccodes-python
$ python -m eccodes selfcheck
Found: ecCodes v2.7.0.
Your system is ready.
```