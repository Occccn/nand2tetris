(LOOP)
@i 
M=0
//キーボードの値を取得する
@KBD
D=M
//キーボードが入力中ならblackへジャンプ
@BLACK
D;JGT

(WHITE)
//白くする処理
@SCREEN
M=0

//1ワード16pixelで32ワードで1行黒くできる。32*256回ループすれば良い？0から数えて8191行目がラスト
@i
D=M
@8190
D=D-A

//
//@iが8191になっていたら終了
@LOOP
D;JGT

//iの数を抽出
@i
D=M

//SCREENのアドレスにインクリメントした箇所を黒くする
@SCREEN
A=D+A
M=0

//iをインクリメント
@i
M=M+1
@WHITE
0;JMP
(BLACK)
@SCREEN
M=-1

//1ワード16pixelで32ワードで1行黒くできる。32*256回ループすれば良い？0から数えて8191行目がラスト
@i
D=M
@8190
D=D-A

//
//@iが8191になっていたら終了
@LOOP
D;JGT

//iの数を抽出
@i
D=M

//SCREENのアドレスにインクリメントした箇所を黒くする
@SCREEN
A=D+A
M=-1

//iをインクリメント
@i
M=M+1
@BLACK
0;JMP



(STOP)