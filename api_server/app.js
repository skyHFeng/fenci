/* 入口文件 */

// 1.导入 express 模块
const express = require("express");

// 2.创建 web 服务器实例
const app = express();

// 5.导入并注册 跨域资源共享 的第三方中间件
const cors = require("cors");
app.use(cors());
//   注册 解析x-www-form-urlencoded格式表单数据 的内置中间件
app.use(express.urlencoded({ extended: false }));
//   封装并注册 响应信息 的自定义中间件
app.use((req, res, next) => {
    // 在 res 上挂载实现响应的 cc 函数
    // 参数err：可能是一个错误对象 或 描述状态信息的字符串
    // 参数status：当前操作的状态，默认值为 1，表示操作出现错误
    res.cc = function (err, status = 1) {
        res.send({
            status,
            // 判断 err 是否为 Error 实例。是，则 err 为一个错误对象
            message: err instanceof Error ? err.message : err
        })
    }
    next();
})

// 4.导入并注册 分词 路由模块
const fenciRouter = require("./router/fenci");
app.use("/api/segment", fenciRouter);

// 3.启动 web 服务器
app.listen(3006, () => {
    console.log("express server running at http://127.0.0.1:3006");
})