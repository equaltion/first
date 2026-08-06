# ui/webview_app.py
import webview
from pathlib import Path

def run_gui():
    # 前端入口文件
    html_path = Path(__file__).parent / "web" / "index.html"
    
    window = webview.create_window(
        title="txt-izer",
        url=str(html_path),
        width=800,
        height=600
    )
    webview.start()

if __name__ == "__main__":
    run_gui()