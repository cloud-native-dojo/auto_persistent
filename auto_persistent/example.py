import persistentvals

p = persistentvals.PersistentVals("./test.dat")
p.foo = "Hello World" #二度目以降の実行ではこれは代入されない
print(p.foo)

#p.foo = 10
#print(p.foo) # 10
#例外として、最初の代入でも保存されている物と型が違う場合は代入される

p.foo = "こんにちは、世界" # 最後に代入された物が保存される

p.lists = [1,2,3,4,5,6,7,8,9,10]
print(p.lists)
p.lists = [10,9,8,7,6,5,4,3,2,1,0]
print(p.lists)
# リストの場合

p.print() #定義されている変数の一覧が出ます