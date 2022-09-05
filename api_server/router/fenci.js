/* 分词 路由模块 */

// 1.导入 express 模块
const express = require("express");
//   导入 path 内置模块
const path = require("path");
//   导入 路由处理函数 模块
const fenci_handler = require("../router_handler/fenci");
//   导入 解析form-data格式表单数据 的模块
const multer = require("multer");
//   创建 multer 实例对象，通过 dest 属性指定上传文件在服务器端的存放路径
const upload = multer({ dest: path.join(__dirname, '../uploads') });

// 2.创建 路由对象
const router = express.Router();

// 3.向 路由对象 挂载路由
// 3.1 在线分词
router.post("/online", fenci_handler.onlineSegment);
// 3.2 文件分词
router.post("/file", upload.single("information"), fenci_handler.fileSegment);

// 4.向外共享 路由对象
module.exports = router;