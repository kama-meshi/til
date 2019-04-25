# :memo: SVNからGitへの移行

## Summary

SVNからGitへの移行時のメモ  
> SVNサーバは SubversionEdge(4.0.11-3908.134), Gitサーバは GitBucket

前提として移行先となるGitサーバは新設（SVNのリポジトリ等は存在しない）

## How to migrate

下記手順で移行可能

1. Gitサーバにリポジトリ作成
2. `git-svn` でSVNサーバからfetch
   - ディレクトリ構成によっては自動でbranchやtagが作成可能
   - 詳細は[下記](#SVNサーバからのfetch方法)参照
3. SVNでタグ用ファイルが存在していた場合はtag (git) を作成
   - SVNのtagsはGitのリモートブランチとして追加される。そのためGitのtagとして扱うには手動でタグ付けが必要
4. SVNでブランチ用ファイルが存在していた場合はbranch (git) を作成
   - SVNのbranchesはGitのリモートブランチとして追加される。そのためGitのbranchとして扱うには手動でブランチを切る必要がある
5. `2`でfetchしたワークツリーに`1`で作成したリモートリポジトリを追加
6. リポートリポジトリにpush

``` Shell
# SVNサーバからクローン (git svn init -> git svn fetchでも可)
git svn clone -s --prefix=svn/ $SVN_REPO_URL
# SVNのtagsをGitのtagにタグ付け
git tag SVN_TAG remotes/svn/tags/SVN_TAG
# SVNのbranchesからGitのbranchを作成
git checkout -b SVN_BRANCH svn/SVN_BRANCH
# リモートリポジトリ追加
git remote add origin $GIT_REPO_URL
# リモートリポジトリへpush
git push --set-upstream origin --all
git push --set-upstream origin --tags
```

### SVNサーバからのfetch方法

JSTの場合、オプション `--localtime` を付与しないとコミット時刻などがずれるため注意。  
SVNからの取り込み時 git-svn が自動でブランチやタグの情報を取り込んでくれるが、ディレクトリ構成によっては手動で指定することがあるので注意。
> SVNのブランチやタグ情報はGitのリモートブランチとして取り込まれるため **そのままPushしても反映されないため注意**

#### 移行SVNリポジトリが基本ディレクトリ構成の場合

`-s` オプションでブランチやタグも自動で取り込まれる

``` sh
$ ls -1 REPO
branches
trunk
tags
$ git svn clone --localtime --prefix=svn/ -s $SVN_URL
```

#### 移行SVNリポジトリが基本ディレクトリ構成でない場合

トランクやブランチ、タグをそれぞれオプションで指定することで取り込み可能

``` sh
$ find ROOT -d 2
ROOT/branches/REPO1_v1
ROOT/branches/REPO1_v2
ROOT/branches/REPO2_v1
ROOT/tags/REPO1_v1
ROOT/tags/REPO2_v1
ROOT/trunk/REPO1
ROOT/trunk/REPO2
$ : ブランチやタグのURLを個別に指定する。（ただし取り込まれる情報は他のリポジトリも含まれるため注意）
$ : 例えば下記コマンドでは "REPO1" のリポジトリをcloneしているが、ブランチやタグには "REPO2" の情報も含まれる（手動でGitブランチやGitタグにするときに選別する）
$ URL='https://example.com/svn/ROOT'
$ git svn clone --localtime --prefix=svn/ -t ${URL}/tags -b ${URL}/branches -T ${URL}/trunk/REPO1 ${URL}/trunk/REPO1
```

#### 移行SVNリポジトリがtrunk/branches/tagsを含まない場合

`-s` オプションを付けなければそのまま移行可能

``` sh
$ ls -1 REPO
src
lib
package.json
$ git svn clone --localtime --prefix=svn/ $SVN_URL
```

## Pushの際にエラーとなったとき

SVNリポジトリによってはGitサーバへのpush時にエラーとなることがある。  
その際に回避策として用いたコマンドを以下に記載。

``` sh
git gc
git config http.postBuffer 524288000
```