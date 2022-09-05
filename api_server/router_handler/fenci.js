/* 分词 路由处理函数模块 */

// 1.导入 fs 内置文件系统模块
const fs = require("fs"); 
//   导入 path 内置模块
const path = require("path");
//  导入 PythonShell 类
const { PythonShell } = require('python-shell');

// 2.定义 路由处理函数
// 2.1 在线分词
exports.onlineSegment = (req, res) => {
    // (1) 从请求体获取用户输入的句子
    const { input } = req.body;
    // (2) 实例化一个 PythonSell 对象
    const pyshell = new PythonShell(path.join(__dirname, "../wordseg/segment_online.py"));
    // (3) 利用 pyshell.send() 方法，将获取的句子编码后传给 Python 脚本
    pyshell.send(encodeURI(input));
    // (4) 利用 pyshell.on 方法，获取 Python 脚本的输出
    pyshell.on('message', (message) => {
        // 将输出解析为 json 格式
        const output = JSON.parse(message);
        // 返回响应体给客户端
        return res.json({
            status: 0,
            message: '分词成功',
            data: output.result
        })
    })

    // (5) 结束 Python 进程
    pyshell.end((err) => {
        if (err) throw err;
    })
}

// 2.2 文件分词
exports.fileSegment = (req, res) => {
    // 2.2.1 上传文件
    // 获取 上传文件 后缀名
    var arr = req.file.originalname.split('.');
    var suffix = arr[arr.length - 1];
    // 保存路径不变，修改文件名
    var oldFile = path.join(__dirname, '../uploads/') + req.file.filename;
    var newFile = path.join(__dirname, '../uploads/') + req.file.filename + '.' + suffix;
    fs.rename(oldFile, newFile, (err) => {
        if (err) return res.cc(err);
        // res.cc("文件上传成功！", 0);
    })

    // 2.2.2 进行分词
    // (1) 获取表单输入的 column
    const column = req.body.column;
    // (2) 实例化一个 PythonSell 对象
    const pyshell = new PythonShell(path.join(__dirname, "../wordseg/segment_file.py"));
    // (3) 利用 pyshell.send() 方法，将获取的 column 传给 Python 脚本
    pyshell.send(column);
    // (4) 利用 pyshell.on 方法，获取 Python 脚本的输出
    pyshell.on('message', (message) => {
        // 将输出解析为 json 格式
        const output = JSON.parse(message);
        // 返回响应体给客户端
        // ① 返回结果文件
        // return res.sendFile(output.result);
        // ② 返回 结果文件和可视化数据 的存储路径
        return res.json({
            status: 0,
            message: "分词成功",
            data: output
        })
    })
    // 5) 结束 Python 进程
    pyshell.end(function (err, code, signal) {
        if (err) throw err;
    });
}