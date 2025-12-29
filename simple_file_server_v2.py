#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
简单的文件下载服务器
使用方法:
python simple_file_server.py --port 8000

默认端口: 8000
"""

import http.server
import socketserver
import os
import sys
import io

# 全局配置 - 用户只需修改此行为自己的存储路径
STORAGE_DIR = r"/var/lib/kubernetes-storage/file_upload/file_container"

def main():
    # 默认配置
    PORT = 8000
    
    # 解析命令行参数
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "--port" and i+1 < len(sys.argv):
            PORT = int(sys.argv[i+1])
    
    # 文件存储目录已在全局配置
    # 确保存储目录存在
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
        print(f"已创建存储目录: {STORAGE_DIR}")
    else:
        print(f"使用现有存储目录: {STORAGE_DIR}")
    
    # 格式化文件大小
    def format_size(size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    print("=" * 50)
    print("文件服务服务器")
    print("=" * 50)
    print(f"服务端口: {PORT}")
    print(f"存储目录: {STORAGE_DIR}")
    print("=" * 50)
    
    # 自定义请求处理器
    class MyHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                # 显示主页面（包含下载和上传链接）
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                html = '''
                <!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>文件服务</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            max-width: 600px;
                            margin: 50px auto;
                            text-align: center;
                            background-color: #f0f0f0;
                        }
                        .container {
                            background: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }
                        h1 {
                            color: #333;
                        }
                        .btn {
                            display: inline-block;
                            background-color: #4CAF50;
                            color: white;
                            padding: 15px 30px;
                            text-decoration: none;
                            font-size: 18px;
                            border-radius: 5px;
                            margin: 10px;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            border: none;
                        }
                        .btn:hover {
                            background-color: #45a049;
                            transform: translateY(-2px);
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                        }
                        .btn:active {
                            transform: translateY(0);
                        }
                        .btn.secondary {
                            background-color: #2196F3;
                        }
                        .btn.secondary:hover {
                            background-color: #0b7dda;
                        }
                        .file-info {
                            color: #666;
                            font-size: 14px;
                            margin: 20px 0;
                        }
                        .theme-toggle {
                            position: absolute;
                            top: 20px;
                            right: 20px;
                            background: #333;
                            color: white;
                            border: none;
                            padding: 10px 15px;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 14px;
                        }
                        .theme-toggle:hover {
                            background: #555;
                        }
                        /* 深色主题样式 */
                        body.dark-theme {
                            background-color: #121212;
                            color: white;
                        }
                        body.dark-theme .container {
                            background: #1e1e1e;
                            color: white;
                        }
                        body.dark-theme h1 {
                            color: white;
                        }
                        body.dark-theme .file-info {
                            color: #ccc;
                        }
                        body.dark-theme .theme-toggle {
                            background: #ccc;
                            color: #333;
                        }
                        body {
                            font-family: Arial, sans-serif;
                            max-width: 600px;
                            margin: 50px auto;
                            text-align: center;
                            background-color: #f0f0f0;
                        }
                        .container {
                            background: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }
                        h1 {
                            color: #333;
                        }
                        .btn {
                            display: inline-block;
                            background-color: #4CAF50;
                            color: white;
                            padding: 15px 30px;
                            text-decoration: none;
                            font-size: 18px;
                            border-radius: 5px;
                            margin: 10px;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            border: none;
                        }
                        .btn:hover {
                            background-color: #45a049;
                            transform: translateY(-2px);
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                        }
                        .btn:active {
                            transform: translateY(0);
                        }
                        .btn.secondary {
                            background-color: #2196F3;
                        }
                        .btn.secondary:hover {
                            background-color: #0b7dda;
                        }
                        .file-info {
                            color: #666;
                            font-size: 14px;
                            margin: 20px 0;
                        }
                        .theme-toggle {
                            position: absolute;
                            top: 20px;
                            right: 20px;
                            background: #333;
                            color: white;
                            border: none;
                            padding: 10px 15px;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 14px;
                        }
                        .theme-toggle:hover {
                            background: #555;
                        }
                        /* 深色主题样式 */
                        body.dark-theme {
                            background-color: #121212;
                            color: white;
                        }
                        body.dark-theme .container {
                            background: #1e1e1e;
                            color: white;
                        }
                        body.dark-theme h1 {
                            color: white;
                        }
                        body.dark-theme .file-info {
                            color: #ccc;
                        }
                        body.dark-theme .theme-toggle {
                            background: #ccc;
                            color: #333;
                        }
                    </style>
                </head>
                <body>
                    <button class="theme-toggle" onclick="toggleTheme()">切换主题</button>
                    
                    <div class="container">
                        <h1>文件服务</h1>
                        <p>选择您需要的操作：</p>
                        <a href="/download_page" class="btn">下载文件</a>
                        <a href="/upload" class="btn secondary">上传文件</a>
                    </div>
                    
                    <script>
                        // 主题切换功能
                        function toggleTheme() {
                            document.body.classList.toggle('dark-theme');
                            // 保存主题设置
                            const isDark = document.body.classList.contains('dark-theme');
                            localStorage.setItem('darkTheme', isDark);
                        }
                        
                        // 恢复主题设置
                        if (localStorage.getItem('darkTheme') === 'true') {
                            document.body.classList.add('dark-theme');
                        }
                        
                        // 页面加载动画
                        window.addEventListener('load', function() {
                            const container = document.querySelector('.container');
                            container.style.opacity = '0';
                            container.style.transform = 'translateY(20px)';
                            
                            setTimeout(() => {
                                container.style.transition = 'all 0.5s ease';
                                container.style.opacity = '1';
                                container.style.transform = 'translateY(0)';
                            }, 100);
                        });
                    </script>
                </body>
                </html>
                '''
                
                self.wfile.write(html.encode('utf-8'))
                
            elif self.path == "/download_page":
                # 显示下载页面，列出所有文件
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                # 获取存储目录中的所有文件
                files = []
                for filename in os.listdir(STORAGE_DIR):
                    file_path = os.path.join(STORAGE_DIR, filename)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        files.append({
                            'name': filename,
                            'size': format_size(file_size)
                        })
                
                # 按文件名排序
                files.sort(key=lambda x: x['name'])
                
                # 生成文件列表HTML
                file_list_html = ''
                for file in files:
                    file_list_html += f'''<tr>
                        <td>{file['name']}</td>
                        <td>{file['size']}</td>
                        <td><a href="/download?file={file['name']}" class="btn-small">下载</a></td>
                    </tr>'''
                
                html = '''
                <!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>文件下载</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            max-width: 800px;
                            margin: 50px auto;
                            text-align: center;
                            background-color: #f0f0f0;
                        }
                        .container {
                            background: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }
                        h1 {
                            color: #333;
                            margin-bottom: 30px;
                        }
                        .btn {
                            display: inline-block;
                            background-color: #4CAF50;
                            color: white;
                            padding: 15px 30px;
                            text-decoration: none;
                            font-size: 18px;
                            border-radius: 5px;
                            margin: 10px;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            border: none;
                        }
                        .btn:hover {
                            background-color: #45a049;
                            transform: translateY(-2px);
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                        }
                        .btn:active {
                            transform: translateY(0);
                        }
                        .btn.secondary {
                            background-color: #6c757d;
                            padding: 10px 20px;
                            font-size: 16px;
                        }
                        .btn-small {
                            background-color: #4CAF50;
                            color: white;
                            padding: 8px 15px;
                            text-decoration: none;
                            font-size: 14px;
                            border-radius: 3px;
                        }
                        .btn-small:hover {
                            background-color: #45a049;
                        }
                        .theme-toggle {
                            position: absolute;
                            top: 20px;
                            right: 20px;
                            background: #333;
                            color: white;
                            border: none;
                            padding: 10px 15px;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 14px;
                        }
                        .theme-toggle:hover {
                            background: #555;
                        }
                        /* 文件列表样式 */
                        .file-list {
                            width: 100%;
                            border-collapse: collapse;
                            margin: 20px 0;
                        }
                        .file-list th,
                        .file-list td {
                            padding: 12px;
                            text-align: left;
                            border-bottom: 1px solid #ddd;
                        }
                        .file-list th {
                            background-color: #f2f2f2;
                            font-weight: bold;
                        }
                        .file-list tr:hover {
                            background-color: #f5f5f5;
                        }
                        /* 深色主题样式 */
                        body.dark-theme {
                            background-color: #121212;
                            color: white;
                        }
                        body.dark-theme .container {
                            background: #1e1e1e;
                            color: white;
                        }
                        body.dark-theme h1 {
                            color: white;
                        }
                        body.dark-theme .file-list th {
                            background-color: #2d2d2d;
                            color: white;
                        }
                        body.dark-theme .file-list td {
                            border-bottom: 1px solid #444;
                            color: white;
                        }
                        body.dark-theme .file-list tr:hover {
                            background-color: #2d2d2d;
                        }
                        body.dark-theme .theme-toggle {
                            background: #ccc;
                            color: #333;
                        }
                    </style>
                </head>
                <body>
                    <button class="theme-toggle" onclick="toggleTheme()">切换主题</button>
                    
                    <div class="container">
                        <h1>文件下载</h1>
                        <p>以下是可供下载的文件列表：</p>
                        
                        <table class="file-list">
                            <thead>
                                <tr>
                                    <th>文件名</th>
                                    <th>文件大小</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                {{file_list}}
                            </tbody>
                        </table>
                        
                        <a href="/" class="btn secondary">返回首页</a>
                    </div>
                    
                    <script>
                        // 主题切换功能
                        function toggleTheme() {
                            document.body.classList.toggle('dark-theme');
                            // 保存主题设置
                            const isDark = document.body.classList.contains('dark-theme');
                            localStorage.setItem('darkTheme', isDark);
                        }
                        
                        // 恢复主题设置
                        if (localStorage.getItem('darkTheme') === 'true') {
                            document.body.classList.add('dark-theme');
                        }
                        
                        // 页面加载动画
                        window.addEventListener('load', function() {
                            const container = document.querySelector('.container');
                            container.style.opacity = '0';
                            container.style.transform = 'translateY(20px)';
                            
                            setTimeout(() => {
                                container.style.transition = 'all 0.5s ease';
                                container.style.opacity = '1';
                                container.style.transform = 'translateY(0)';
                            }, 100);
                        });
                    </script>
                </body>
                </html>
                '''
                
                # 替换文件列表
                html = html.replace('{{file_list}}', file_list_html)
                
                self.wfile.write(html.encode('utf-8'))
                
            elif self.path.startswith("/download"):
                # 处理文件下载
                try:
                    # 解析文件名参数
                    import urllib.parse
                    parsed = urllib.parse.urlparse(self.path)
                    query = urllib.parse.parse_qs(parsed.query)
                    
                    if 'file' in query:
                        filename = query['file'][0]
                        file_path = os.path.join(STORAGE_DIR, filename)
                        
                        if os.path.isfile(file_path):
                            with open(file_path, 'rb') as f:
                                self.send_response(200)
                                self.send_header("Content-type", "application/octet-stream")
                                self.send_header("Content-Disposition", f"attachment; filename={filename}")
                                self.send_header("Content-Length", str(os.path.getsize(file_path)))
                                self.end_headers()
                                
                                # 分块发送文件
                                chunk_size = 8192
                                while True:
                                    chunk = f.read(chunk_size)
                                    if not chunk:
                                        break
                                    self.wfile.write(chunk)
                        else:
                            self.send_error(404, f"File not found: {filename}")
                    else:
                        self.send_error(400, "缺少file参数")
                except Exception as e:
                    self.send_error(500, f"Server Error: {e}")
                
            elif self.path == "/upload":
                # 显示上传页面
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
                html = '''
                <!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>文件上传</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            max-width: 600px;
                            margin: 50px auto;
                            text-align: center;
                            background-color: #f0f0f0;
                        }
                        .container {
                            background: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        }
                        h1 {
                            color: #333;
                        }
                        .btn {
                            display: inline-block;
                            background-color: #4CAF50;
                            color: white;
                            padding: 15px 30px;
                            text-decoration: none;
                            font-size: 18px;
                            border-radius: 5px;
                            margin: 10px;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            border: none;
                        }
                        .btn:hover {
                            background-color: #45a049;
                            transform: translateY(-2px);
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                        }
                        .btn:active {
                            transform: translateY(0);
                        }
                        .btn.secondary {
                            background-color: #6c757d;
                            padding: 10px 20px;
                            font-size: 16px;
                        }
                        .btn.secondary:hover {
                            background-color: #5a6268;
                        }
                        .btn:disabled {
                            background-color: #ccc;
                            cursor: not-allowed;
                            transform: none;
                            box-shadow: none;
                        }
                        .file-input {
                            margin: 20px 0;
                            padding: 10px;
                            border: 2px dashed #ccc;
                            border-radius: 5px;
                            background: #f8f9fa;
                        }
                        .file-input input[type="file"] {
                            margin: 10px 0;
                            font-size: 16px;
                        }
                        .success {
                            color: #28a745;
                            margin: 20px 0;
                            padding: 15px;
                            background: #d4edda;
                            border-radius: 5px;
                        }
                        .error {
                            color: #dc3545;
                            margin: 20px 0;
                            padding: 15px;
                            background: #f8d7da;
                            border-radius: 5px;
                        }
                        .theme-toggle {
                            position: absolute;
                            top: 20px;
                            right: 20px;
                            background: #333;
                            color: white;
                            border: none;
                            padding: 10px 15px;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 14px;
                        }
                        .theme-toggle:hover {
                            background: #555;
                        }
                        /* 进度条样式 */
                        .progress-container {
                            margin: 20px 0;
                            display: none;
                        }
                        .progress-bar {
                            width: 100%;
                            height: 20px;
                            background-color: #e0e0e0;
                            border-radius: 10px;
                            overflow: hidden;
                            margin: 10px 0;
                        }
                        .progress-fill {
                            height: 100%;
                            background-color: #4CAF50;
                            width: 0%;
                            transition: width 0.3s ease;
                            border-radius: 10px;
                        }
                        .progress-info {
                            font-size: 14px;
                            color: #666;
                            margin: 10px 0;
                            line-height: 1.5;
                        }
                        .progress-details {
                            display: flex;
                            justify-content: space-between;
                            margin-top: 10px;
                            font-size: 12px;
                            color: #888;
                        }
                        /* 深色主题样式 */
                        body.dark-theme {
                            background-color: #121212;
                            color: white;
                        }
                        body.dark-theme .container {
                            background: #1e1e1e;
                            color: white;
                        }
                        body.dark-theme h1 {
                            color: white;
                        }
                        body.dark-theme .file-input {
                            background: #2d2d2d;
                            border-color: #555;
                            color: white;
                        }
                        body.dark-theme .success {
                            background: #155724;
                            color: #d4edda;
                        }
                        body.dark-theme .error {
                            background: #721c24;
                            color: #f8d7da;
                        }
                        body.dark-theme .theme-toggle {
                            background: #ccc;
                            color: #333;
                        }
                        body.dark-theme .progress-bar {
                            background-color: #333;
                        }
                        body.dark-theme .progress-info {
                            color: #ccc;
                        }
                        body.dark-theme .progress-details {
                            color: #aaa;
                        }
                    </style>
                </head>
                <body>
                    <button class="theme-toggle" onclick="toggleTheme()">切换主题</button>
                    
                    <div class="container">
                        <h1>文件上传</h1>
                        <p>请选择要上传的文件：</p>
                        
                        <form id="uploadForm" enctype="multipart/form-data">
                            <div class="file-input">
                                <input type="file" id="fileInput" name="file" required multiple>
                            </div>
                            <button type="submit" class="btn" id="uploadBtn">上传文件</button>
                        </form>
                        
                        <!-- 进度条 -->
                        <div class="progress-container" id="progressContainer">
                            <div class="progress-info" id="progressInfo">准备上传...</div>
                            <div class="progress-bar">
                                <div class="progress-fill" id="progressFill"></div>
                            </div>
                            <div class="progress-details">
                                <span id="speed">网速: 0 B/s</span>
                                <span id="timeElapsed">已用时间: 00:00</span>
                                <span id="timeRemaining">剩余时间: --:--</span>
                            </div>
                        </div>
                        
                        <a href="/" class="btn secondary">返回首页</a>
                    </div>
                    
                    <script>
                        // 主题切换功能
                        function toggleTheme() {
                            document.body.classList.toggle('dark-theme');
                            // 保存主题设置
                            const isDark = document.body.classList.contains('dark-theme');
                            localStorage.setItem('darkTheme', isDark);
                        }
                        
                        // 恢复主题设置
                        if (localStorage.getItem('darkTheme') === 'true') {
                            document.body.classList.add('dark-theme');
                        }
                        
                        // 页面加载动画
                        window.addEventListener('load', function() {
                            const container = document.querySelector('.container');
                            container.style.opacity = '0';
                            container.style.transform = 'translateY(20px)';
                            
                            setTimeout(() => {
                                container.style.transition = 'all 0.5s ease';
                                container.style.opacity = '1';
                                container.style.transform = 'translateY(0)';
                            }, 100);
                        });
                        
                        // 文件上传进度功能
                        document.getElementById('uploadForm').addEventListener('submit', function(e) {
                            e.preventDefault();
                            
                            const fileInput = document.getElementById('fileInput');
                            const files = fileInput.files;
                            if (files.length === 0) {
                                alert('请选择要上传的文件');
                                return;
                            }
                            
                            // 显示进度条
                            const progressContainer = document.getElementById('progressContainer');
                            const progressFill = document.getElementById('progressFill');
                            const progressInfo = document.getElementById('progressInfo');
                            const speedElement = document.getElementById('speed');
                            const timeElapsedElement = document.getElementById('timeElapsed');
                            const timeRemainingElement = document.getElementById('timeRemaining');
                            const uploadBtn = document.getElementById('uploadBtn');
                            
                            progressContainer.style.display = 'block';
                            uploadBtn.disabled = true;
                            uploadBtn.textContent = '上传中...';
                            
                            // 创建FormData
                            const formData = new FormData();
                            for (let i = 0; i < files.length; i++) {
                                formData.append('file', files[i]);
                            }
                            
                            // 初始化进度跟踪变量
                            let startTime = Date.now();
                            let lastUpdateTime = startTime;
                            let lastLoaded = 0;
                            
                            // 创建XMLHttpRequest
                            const xhr = new XMLHttpRequest();
                            
                            // 监听进度事件
                            xhr.upload.addEventListener('progress', function(e) {
                                if (e.lengthComputable) {
                                    const now = Date.now();
                                    const elapsed = now - startTime;
                                    const sinceLastUpdate = now - lastUpdateTime;
                                    
                                    const loaded = e.loaded;
                                    const total = e.total;
                                    const percent = Math.round((loaded / total) * 100);
                                    
                                    // 计算网速
                                    const bytesSinceLastUpdate = loaded - lastLoaded;
                                    const speedBps = bytesSinceLastUpdate / (sinceLastUpdate / 1000);
                                    
                                    // 更新进度条
                                    progressFill.style.width = percent + '%';
                                    progressInfo.textContent = `上传进度: ${percent}% (${formatFileSize(loaded)} / ${formatFileSize(total)})`;
                                    
                                    // 更新网速
                                    speedElement.textContent = `网速: ${formatSpeed(speedBps)}`;
                                    
                                    // 更新已用时间
                                    timeElapsedElement.textContent = `已用时间: ${formatTime(elapsed)}`;
                                    
                                    // 计算并更新剩余时间
                                    if (percent > 0 && percent < 100) {
                                        const estimatedTotalTime = (elapsed / percent) * 100;
                                        const remainingTime = estimatedTotalTime - elapsed;
                                        timeRemainingElement.textContent = `剩余时间: ${formatTime(remainingTime)}`;
                                    } else {
                                        timeRemainingElement.textContent = `剩余时间: --:--`;
                                    }
                                    
                                    // 更新最后更新时间和已加载字节数
                                    lastUpdateTime = now;
                                    lastLoaded = loaded;
                                }
                            });
                            
                            // 上传完成事件
                            xhr.addEventListener('load', function() {
                                if (xhr.status === 200) {
                                    // 上传成功，显示结果
                                    document.open();
                                    document.write(xhr.responseText);
                                    document.close();
                                } else {
                                    progressInfo.textContent = `上传失败: ${xhr.statusText}`;
                                    uploadBtn.disabled = false;
                                    uploadBtn.textContent = '上传文件';
                                }
                            });
                            
                            // 上传错误事件
                            xhr.addEventListener('error', function() {
                                progressInfo.textContent = '上传失败: 网络错误';
                                uploadBtn.disabled = false;
                                uploadBtn.textContent = '上传文件';
                            });
                            
                            // 发送请求
                            xhr.open('POST', '/upload', true);
                            xhr.send(formData);
                        });
                        
                        // 格式化文件大小
                        function formatFileSize(bytes) {
                            if (bytes === 0) return '0 B';
                            const k = 1024;
                            const sizes = ['B', 'KB', 'MB', 'GB'];
                            const i = Math.floor(Math.log(bytes) / Math.log(k));
                            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
                        }
                        
                        // 格式化网速
                        function formatSpeed(bps) {
                            if (bps < 1024) return bps.toFixed(0) + ' B/s';
                            if (bps < 1024 * 1024) return (bps / 1024).toFixed(2) + ' KB/s';
                            return (bps / (1024 * 1024)).toFixed(2) + ' MB/s';
                        }
                        
                        // 格式化时间（毫秒转为 mm:ss）
                        function formatTime(ms) {
                            const totalSeconds = Math.floor(ms / 1000);
                            const minutes = Math.floor(totalSeconds / 60);
                            const seconds = totalSeconds % 60;
                            return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                        }
                    </script>
                </body>
                </html>
                '''
                
                self.wfile.write(html.encode('utf-8'))
            else:
                # 其他路径返回404
                self.send_error(404, "Not Found")
        
        def do_POST(self):
            # 处理文件上传
            if self.path == "/upload":
                try:
                    content_type = self.headers['Content-Type']
                    if not content_type.startswith('multipart/form-data'):
                        self.send_error(400, "Invalid content type")
                        return
                    
                    # 解析boundary
                    boundary = content_type.split('boundary=')[1].encode('utf-8')
                    
                    # 获取内容长度
                    content_length = int(self.headers['Content-Length'])
                    
                    # 读取所有内容
                    content = self.rfile.read(content_length)
                    
                    # 分割multipart内容
                    parts = content.split(b'--' + boundary)
                    
                    success_count = 0
                    
                    # 遍历所有部分
                    for part in parts[1:-1]:  # 跳过第一个空部分和最后一个结束部分
                        part = part.strip()
                        if not part:
                            continue
                        
                        # 查找头部和内容的分隔符
                        header_end = part.find(b'\r\n\r\n')
                        if header_end == -1:
                            continue
                        
                        # 解析头部
                        headers = part[:header_end].decode('utf-8')
                        
                        # 查找文件名
                        filename = None
                        if 'filename="' in headers:
                            filename_start = headers.find('filename="') + 10
                            filename_end = headers.find('"', filename_start)
                            filename = headers[filename_start:filename_end]
                            
                            # 只处理有文件名的部分（文件字段）
                            if filename:
                                filename = os.path.basename(filename)
                                # 获取文件内容
                                file_content = part[header_end + 4:]  # 跳过\r\n\r\n
                                # 构建保存路径
                                save_path = os.path.join(STORAGE_DIR, filename)
                                
                                # 保存文件
                                with open(save_path, 'wb') as f:
                                    f.write(file_content)
                                success_count += 1
                        
                    # 构建上传成功页面
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    
                    # 使用普通字符串并手动替换变量，避免CSS大括号与f-string冲突
                    html = '''
                    <!DOCTYPE html>
                    <html lang="zh-CN">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>上传成功</title>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                max-width: 600px;
                                margin: 50px auto;
                                text-align: center;
                                background-color: #f0f0f0;
                            }
                            .container {
                                background: white;
                                padding: 20px;
                                border-radius: 5px;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                            }
                            h1 {
                                color: #333;
                            }
                            .btn {
                                display: inline-block;
                                background-color: #4CAF50;
                                color: white;
                                padding: 10px 20px;
                                text-decoration: none;
                                font-size: 16px;
                                border-radius: 3px;
                                margin: 10px;
                                cursor: pointer;
                                border: none;
                            }
                            .btn:hover {
                                background-color: #45a049;
                            }
                            .btn.secondary {
                                background-color: #6c757d;
                            }
                            .success {
                                color: #28a745;
                                margin: 20px 0;
                                padding: 10px;
                                background: #d4edda;
                                border-radius: 3px;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>上传成功</h1>
                            <div class="success">
                                <p>成功上传 {{success_count}} 个文件</p>
                            </div>
                            <a href="/upload" class="btn">继续上传</a>
                            <a href="/" class="btn secondary">返回首页</a>
                        </div>
                    </body>
                    </html>
                    '''
                    
                    # 手动替换变量
                    html = html.replace('{{success_count}}', str(success_count))
                    
                    self.wfile.write(html.encode('utf-8'))
                    
                except Exception as e:
                    self.send_error(500, f"Server Error: {e}")
            else:
                self.send_error(404, "Not Found")
        
        # 启用请求日志
        def log_message(self, format, *args):
            import datetime
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{now}] {self.client_address[0]}:{self.client_address[1]} - {format % args}")
    
    # 启动服务器
    try:
        # 使用多线程服务器，支持并发连接
        with socketserver.ThreadingTCPServer(("", PORT), MyHandler) as httpd:
            print(f"服务器已启动，本地访问地址: http://127.0.0.1:{PORT}")
            print("服务器类型: 多线程 (ThreadingTCPServer)")
            print("最大并发连接数: 无限制 (系统资源限制)")
            print("请将此本地服务通过隧道工具暴露到公网")
            print("按 Ctrl+C 停止服务器")
            print("=" * 50)
            
            # 运行服务器
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"\n服务器启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
