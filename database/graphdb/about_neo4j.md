# :memo: About Neo4j

## What is GraphDB (Neo4j)

グラフDBはグラフ（データ同士のつながりや関連）を扱うのに特化したDB。  
例えば `田中さん` と `友達` のデータを簡単に検索したりすることができる。
> 少し触った感じではRDBでは複雑になりがちなデータを簡単に検索できとても便利に感じた。  
> RDBでは「データ `rows`」しか扱えないのに対して、グラフDBでは「関連 `relationships`」も扱えるのが便利。

Cypherという問合せ言語を利用してデータを検索する（RDBでいうところのSQL）

Neo4jはJava製のグラフDB:memo:  
GUI画面にチュートリアルがついていたり、グラフを視覚的に確認できたりグラフDBに触ったことがなくとも手軽に試せた。

## How to install Neo4j

dockerを用いれば簡単にインストール、稼働可能

``` sh
$ docker pull neo4j
$ docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
neo4j               latest              e89d0c320043        2 weeks ago         203MB
$ docker run \
    --name testneo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \
    neo4j:latest
```

上記でnoe4j稼働後、ブラウザで `http://localhost:7474` でGUI画面が開く。
> ID/PW -> `neo4j`/`test` でログイン可能

### Neo4jを使ってみて

- Cypherは最初見たときはとっつきにくかったが実際に使ってみると直感的で理にかなっている構文に感じた
- リレーションの深さを検索できるのが便利！
  - 「もしかして友達かも？」みたいな機能（レコメンデーション）を簡単に実現できる