

#需要把这些内容全部集成到一个弹窗中



from flask import Flask, render_template_string
import google.generativeai as genai
import time
import requests

app = Flask(__name__)

# 配置 Google Generative AI API 密钥
genai.configure(api_key="AIzaSyBK8KRfjpj0GCN0LdOUmzbDMukEWk7H_eA")
model = genai.GenerativeModel("gemini-1.5-flash")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python GET 请求与AI示例</title>
    <script>
        // 发送AI请求
        function sendAIRequest() {
            fetch('/get-ai-response')  // 调用后端的 /get-ai-response 路由
                .then(response => response.json())
                .then(data => {
                    // 解析 AI 返回的指令
                    let aiResponse = data.response;
                    alert("ai响应: " + aiResponse);
                    let params = aiResponse.split(";");
                    let url = "http://192.168.137.158/command?x_10";
                    
                    let timestamp = Date.now();  // 获取当前时间戳

                    // 遍历并构造 GET 请求 URL
                    params.forEach(param => {
    let [key, value] = param.split("-");
    url += `&${key}=${value}`;
});

                    url += `&time=${timestamp}`;
                    
                    // 发出 GET 请求
                    fetch(url)
                        .then(response => response.json())
                        .then(data => {
                            alert("服务器响应: " + data.response);
                        })
                        .catch(error => {
                            alert("Get请求失败: " + error);
                        });
                })
                .catch(error => {
                    alert("AI 请求失败: " + error);
                });
        }

        // 发送 GET 请求并显示服务器响应
        function sendRequest() {
            fetch('/send-request')  // 调用后端的 /send-request 路由
                .then(response => response.json())
                .then(data => {
                    alert("服务器响应: " + data.response);
                })
                .catch(error => {
                    alert("请求失败: " + error);
                });
        }
    </script>
</head>
<body>
    <h1>点击按钮发送请求</h1>
    <button onclick="sendRequest()">发送 GET 请求</button><br><br>
    <button onclick="sendAIRequest()">获取 AI 响应并发送指令</button>
</body>
</html>
"""

@app.route('/')
def index():
    # 渲染 HTML 模板
    return render_template_string(HTML_TEMPLATE)

@app.route('/send-request')
def send_request():
    # 获取当前时间戳
    timestamp = int(time.time())  # 获取秒级时间戳

    # 构造目标 URL，其中 time 参数设置为当前的时间戳
    url = f"http://192.168.137.158/command?x_10&time={timestamp}"
    
    try:
        # 发送 GET 请求
        response = requests.get(url)
        return {"response": response.text}, 200
    except Exception as e:
        return {"response": f"请求失败: {e}"}, 500

@app.route('/get-ai-response')
def get_ai_response():
    # 调用 AI 模型生成内容
    response = model.generate_content("""假设现在由你来控制一台机械臂，以下是操作说明：
E代表机械臂夹子，范围是10到100
Z 代表机械臂上臂，范围是90到180
Y 代表机械臂下臂，范围是50到180
H 代表机械臂整体转向，范围是0到180

指令格式是 一个字母后面加“-”和一个数字（一定要在范围中），每两条指令间用“;”隔离
如X90;Y90 意思是执行后 X 舵机转到 90度,Y 舵机转到 90度
下面设计一个动作""")
    return {"response": response.text}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)







