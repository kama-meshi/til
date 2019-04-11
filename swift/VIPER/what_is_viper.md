# :memo: What is VIPER 🐍

## Summary

- iOS用に考えられたプロジェクトアーキテクチャ
  - MVCから発展させたアーキテクチャになっている
  - `View`, `Interactor`, `Presenter`, `Entity`, `Router` からなる

## VIPER

公式サイトは[こちら](https://cheesecakelabs.com/blog/ios-project-architecture-using-viper/) 🐍  
サイトに簡単なアーキテクチャが乗っている（以下図転載）

![VIPER](https://s3.amazonaws.com/ckl-website-static/wp-content/uploads/2016/04/Viper-Module-768x365.png "VIPER")

特にその特徴は **`Router`** 。  
`V, I, P, E` などはMVPなどの考えに近く、他アーキテクチャにも見られる考えだが、この要素はナビゲーションを司り、煩雑になりやすい画面遷移などを一元管理できるようになる。
> 📝 `ViewContoller` で画面遷移などを行う必要があるiOSに特化した考え？
