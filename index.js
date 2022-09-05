$(function () {
    // loading效果
    $(document).ajaxStart(function () {
        $("#loading").show();
    })
    $(document).ajaxStop(function () {
        $("#loading").hide();
    })

    // 1.在线分词
    $("#form1").on("submit", function (event) {
        event.preventDefault();
        // 快速获取表单中的数据
        var data = $(this).serialize();

        // 发起 POST 请求
        $.ajax({
            method: "POST",
            url: "http://127.0.0.1:3006/api/segment/online",
            data: data,
            success: function (res) {
                if (res.status !== 0) return alert("在线分词失败！");
                // 渲染 UI
                $("#result-online").empty().append(res.data)
            }
        })
    })

    // 2.文件分词
    $("#btn").on("click", function () {
        // 创建 FormData 对象，并写入表单数据
        var fd = new FormData(document.querySelector("#form2"));
        // 查看 FormData 对象
        // for (var pair of fd.entries()) {
        //     console.log(pair[0] + ', ' + pair[1]);
        // }

        // 发起 POST 请求
        $.ajax({
            method: "POST",
            url: "http://127.0.0.1:3006/api/segment/file",
            data: fd,
            // 不修改Content-Type属性，使用FormData默认的Content-Type值
            contentType: false,
            // 不对FormData中的数据进行url编码，而是将FormData数据原样发送到服务器
            processData: false,
            success: function (res) {
                if (res.status !== 0) return alert("文件分词失败！");
                console.log(res)
                // 渲染 UI
                var resultStr = '<li class="list-group-item">结果文件：' + res.data.result_file
                    + '<a class="badge" href="' + res.data.img_language 
                    + '" target="_blank" style="background-color: #5BC0DE">语言</a><a class="badge" href="' + res.data.img_fra_bd
                    + '" target="_blank" style="background-color: #5BC0DE">大数据框架</a><a class="badge" href="' + res.data.img_fra_ml
                    + '" target="_blank" style="background-color: #5BC0DE">机器学习框架</a><a class="badge" href="' + res.data.img_ai_nlp
                    + '" target="_blank" style="background-color: #5BC0DE">NLP</a><a class="badge" href="' + res.data.img_ai_cv
                    + '" target="_blank" style="background-color: #5BC0DE">CV</a><a class="badge" href="' + res.data.img_ai
                    + '" target="_blank" style="background-color: #5BC0DE">AI</a><a class="badge" href="' + res.data.img_top10
                    + '" target="_blank" style="background-color: #5BC0DE">Top10</a></li>';
                $("#result-list").empty().append(resultStr);
            }
        })
    })
})