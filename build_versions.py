"""두 버전 명함을 만든다.

index.html 은 '프코잉글리시' 원본이다. 이 스크립트는
  1) index.html 안의 사이트 주소를 BASE 로 맞추고
  2) 브랜드만 'Sally English' 로 바꾼 sally/index.html 을 만든다.
디자인을 고칠 때는 index.html 만 고친 뒤 `python3 build_versions.py` 를 실행하면 된다.
(QR코드 그림은 assets/qr.svg, assets/qr-sally.svg 로 따로 만들어 둔다.)
"""
import re
from pathlib import Path

BASE = "https://pcoenglish.vercel.app"  # 배포 주소 (끝에 / 없이)

root = Path(__file__).parent
src = (root / "index.html").read_text(encoding="utf-8")

# 1) 원본(프코잉글리시)의 절대 주소를 BASE 로 통일
src = re.sub(r"https://[^\"' ]+?(?=/assets/og\.jpg)", BASE, src)
src = re.sub(r'(og:url" content=")[^"]*', rf"\g<1>{BASE}/", src)
src = re.sub(r"(const URL_CARD = ')[^']*", rf"\g<1>{BASE}/", src)
(root / "index.html").write_text(src, encoding="utf-8")

# 2) Sally English 버전
s = src
pairs = [
    ("<title>정세빈 원장 | 프코잉글리시</title>", "<title>정세빈 원장 | Sally English</title>"),
    ('content="프코잉글리시 정세빈 원장', 'content="Sally English 정세빈 원장'),
    ("정세빈 원장 · 프코잉글리시", "정세빈 원장 · Sally English"),
    (f'og:url" content="{BASE}/"', f'og:url" content="{BASE}/sally/"'),
    ("/assets/og.jpg", "/assets/og-sally.jpg"),
    ('alt="프코잉글리시 로고"', 'alt="Sally English 로고"'),
    ("<b>프코잉글리시</b><span>Teacher Sally</span>", '<b>Sally English</b><span class="ko">샐리 잉글리시</span>'),
    ("assets/qr.svg", "assets/qr-sally.svg"),
    ("PCO ENGLISH · TEACHER SALLY", "SALLY ENGLISH · TEACHER SALLY"),
    (f"const URL_CARD = '{BASE}/'", f"const URL_CARD = '{BASE}/sally/'"),
    ("'ORG:프코잉글리시'", "'ORG:Sally English'"),
]
for a, b in pairs:
    if a not in s:
        raise SystemExit(f"찾을 수 없음: {a}")
    s = s.replace(a, b)

# 하위 폴더이므로 상대 경로 assets/ → ../assets/
s = re.sub(r'(src|href)="assets/', r'\1="../assets/', s)
s = s.replace("url(assets/", "url(../assets/")

out = root / "sally" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(s, encoding="utf-8")
print("완료:", out)
