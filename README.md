# runJSFunctionByUrl
 模拟浏览器console的功能，输入一个URL，使用不同的输入批量执行js函数    
使用方法：    
（1）在URL框内输入对应的URL    
（2）勾选需要数量的输入，输入内容会按照集束炸弹模式（Cluster bomb）构建     
（3）调整自动生成的输入格式，每个输入框的输入使用$%$输入值1$%$、$%$输入值2$%$ 表示，插入形式与brupsuite爆破报文形式类似    
（4）调整js处理函数标签内自动生成的js代码，process函数名不能调整，输入值nowInputVal是已经使用输入格式进行格式化后的输入值    
（5）点击运行按钮，若一切正常，输出结果将会显示在 结果 标签处，否则结果处会显示None，这时候请检查js处理函数处的输入是否符合js语法    
PS：因未知BUG，会出现第一次点击运行结果全为None的情况，再次点击运行后就正常，若一直为None则证明js处理函数处的输入存在异常    
PS2：程序是一行一行读取输入的js处理函数的，故需要函数中的js语句一行书写完整，特别需要注意复制浏览器中json格式的变量值时可能存在无法读取的问题，例：  
错误写法：  
let jsonStr = {  
"a":1,  
"b":2  
};  
正确写法：  
let jsonStr = {"a":1, "b":2};    
PS3：经测试发现JS语句最后不加分号会提示：Uncaught SyntaxError: Invalid or unexpected token，在编写JS函数时需要注意分号问题   
PS4：代理和外部引用JS的开启均在设置页面，代理默认关闭，外部引用JS默认开启  
    
使用核心功能库：QtWebEngineWidgets    
使用图形库：pyQt5    
使用打包库：pyinstaller    
