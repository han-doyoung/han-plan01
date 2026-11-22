"""화면 스타일 만들기: styles/app.css (Tailwind CSS v4 원본) → index.html 안의 <style id="app-css">

사용법
  python tools/build-css.py [tailwindcss 실행 파일 경로]

  · Tailwind 공식 단독 실행 파일(tailwindcss-windows-x64.exe, Node.js 불필요)을
    https://github.com/tailwindlabs/tailwindcss/releases 에서 받아 경로를 넘기거나,
    환경 변수 TAILWIND 에 경로를 넣으세요. (v4.1.11 에서 확인)
  · 결과 CSS는 index.html 안에 들어가므로 인터넷이 막힌 내부망에서도 그대로 보입니다.
"""
import io, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'styles', 'app.css')
HTML = os.path.join(ROOT, 'index.html')
START, END = '<style id="app-css">', '</style>'


def main():
    exe = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('TAILWIND', 'tailwindcss')
    html = io.open(HTML, encoding='utf-8').read()
    a = html.index(START) + len(START)
    b = html.index(END, a)
    # 이미 들어 있는 CSS를 빼고 검사해야 쓰지 않는 클래스가 쌓이지 않음
    scan = html[:a] + html[b:]
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, 'styles'))
        io.open(os.path.join(tmp, 'index.html'), 'w', encoding='utf-8').write(scan)
        src = io.open(SRC, encoding='utf-8').read()
        io.open(os.path.join(tmp, 'styles', 'app.css'), 'w', encoding='utf-8').write(src)
        out = os.path.join(tmp, 'out.css')
        subprocess.run([exe, '-i', os.path.join(tmp, 'styles', 'app.css'), '-o', out, '--minify'], check=True, cwd=tmp)
        css = io.open(out, encoding='utf-8').read().strip()
    css = re.sub(r'^/\*![^*]*\*/', '', css).strip()
    html = html[:a] + '\n' + css + '\n' + html[b:]
    tmpf = HTML + '.tmp'
    io.open(tmpf, 'w', encoding='utf-8', newline='\n').write(html)
    os.replace(tmpf, HTML)
    print(f'index.html 스타일 갱신: {len(css):,}자')


if __name__ == '__main__':
    main()
