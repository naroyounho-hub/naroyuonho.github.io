import os
from datetime import datetime

import requests
from playwright.sync_api import sync_playwright


def fetch_web3_html(keyword: str) -> str:
    url = "https://web3.career/"
    resp = requests.get(url, params={"search": keyword}, timeout=20)
    resp.raise_for_status()
    return resp.text


def fetch_berlin_html(keyword: str) -> str:
    url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(1500)
        html = page.content()
        browser.close()
    return html


def fetch_wework_html(keyword: str) -> str:
    url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(1500)
        html = page.content()
        browser.close()
    return html


def main():
    keyword = input("검색 키워드 (기본: python): ").strip() or "python"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs("pages", exist_ok=True)

    files = {}
    files["BerlinStartupJobs"] = f"pages/berlin_{keyword}_{stamp}.html"
    files["Web3Career"] = f"pages/web3_{keyword}_{stamp}.html"
    files["WeWorkRemotely"] = f"pages/wework_{keyword}_{stamp}.html"

    with open(files["BerlinStartupJobs"], "w", encoding="utf-8") as f:
        f.write(fetch_berlin_html(keyword))
    with open(files["Web3Career"], "w", encoding="utf-8") as f:
        f.write(fetch_web3_html(keyword))
    with open(files["WeWorkRemotely"], "w", encoding="utf-8") as f:
        f.write(fetch_wework_html(keyword))

    index = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Scraper HTML 결과</title>
    <style>
      body {{ font-family: Arial, sans-serif; margin: 40px; }}
      .card {{ padding: 16px; border: 1px solid #ddd; margin-bottom: 12px; }}
      a {{ text-decoration: none; }}
    </style>
  </head>
  <body>
    <h1>스크래퍼 HTML 결과</h1>
    <p>키워드: <strong>{keyword}</strong> / 생성 시각: {stamp}</p>
    <div class="card">
      <h2>BerlinStartupJobs</h2>
      <a href="{files['BerlinStartupJobs']}">HTML 열기</a>
    </div>
    <div class="card">
      <h2>Web3Career</h2>
      <a href="{files['Web3Career']}">HTML 열기</a>
    </div>
    <div class="card">
      <h2>WeWorkRemotely</h2>
      <a href="{files['WeWorkRemotely']}">HTML 열기</a>
    </div>
  </body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index)

    print("완료:")
    for name, path in files.items():
        print(f"- {name}: {path}")
    print("- index.html 생성됨")


if __name__ == "__main__":
    main()
