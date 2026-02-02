import json

# Read the data files
with open('section1_direct.json', 'r', encoding='utf-8') as f:
    section1 = json.load(f)

with open('section2_creative.json', 'r', encoding='utf-8') as f:
    section2 = json.load(f)

# Create the HTML with embedded data
html_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Живой опыт — Addiction & Creation</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            -webkit-font-smoothing: antialiased;
            background: #000;
            color: #1d1d1f;
            line-height: 1.6;
        }
        .main-wrapper {
            background: #fafafa;
            max-width: 1200px;
            margin: 0 auto;
            box-shadow: 0 0 100px rgba(0, 0, 0, 0.5);
        }
        .container { max-width: 1000px; margin: 0 auto; padding: 0 40px; }
        header {
            padding: 80px 0 60px;
            text-align: center;
            border-bottom: 1px solid #d2d2d7;
            background: #fff;
            position: relative;
        }
        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 200px;
            height: 3px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #667eea 100%);
            border-radius: 0 0 2px 2px;
        }
        .logo {
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            color: #86868b;
            margin-bottom: 12px;
        }
        header h1 {
            font-size: 56px;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: #1d1d1f;
            margin-bottom: 8px;
            line-height: 1.1;
        }
        .subtitle-en {
            font-size: 24px;
            font-weight: 400;
            letter-spacing: 0.01em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }
        .tagline {
            font-size: 17px;
            font-weight: 400;
            color: #6e6e73;
            font-style: italic;
            letter-spacing: 0.01em;
        }
        nav {
            display: flex;
            justify-content: center;
            gap: 8px;
            padding: 40px 0;
            position: sticky;
            top: 0;
            background: rgba(250, 250, 250, 0.95);
            backdrop-filter: saturate(180%) blur(20px);
            z-index: 100;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        }
        .nav-btn {
            padding: 8px 20px;
            font-size: 14px;
            font-weight: 500;
            color: #1d1d1f;
            background: transparent;
            border: 1px solid #d2d2d7;
            border-radius: 980px;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        .nav-btn:hover {
            background: #f5f5f7;
            border-color: #1d1d1f;
        }
        .nav-btn.active {
            background: #1d1d1f;
            color: #fff;
            border-color: #1d1d1f;
        }
        .section-info {
            text-align: center;
            padding: 20px 0 40px;
            font-size: 15px;
            color: #86868b;
            font-weight: 400;
        }
        .posts-grid {
            display: grid;
            gap: 0;
            margin-bottom: 80px;
        }
        .post-card {
            background: #fff;
            padding: 40px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }
        .post-card::before {
            content: '';
            position: absolute;
            bottom: 0;
            left: 40px;
            right: 40px;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, #667eea 20%, #764ba2 40%, #f093fb 60%, #4facfe 80%, transparent 100%);
            opacity: 0.3;
            transition: opacity 0.3s ease;
        }
        .post-card:hover::before { opacity: 0.6; }
        .post-card::after {
            content: '→';
            position: absolute;
            right: 40px;
            top: 40px;
            font-size: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            opacity: 0;
            transition: all 0.2s ease;
        }
        .post-card:hover {
            background: #f5f5f7;
            transform: translateX(4px);
        }
        .post-card:hover::after {
            opacity: 1;
            transform: translateX(4px);
        }
        .post-card:last-child::before { display: none; }
        .post-meta {
            display: flex;
            gap: 16px;
            align-items: center;
            margin-bottom: 16px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .post-source {
            color: #1d1d1f;
            font-weight: 600;
            position: relative;
            padding-left: 12px;
        }
        .post-source::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        .post-date { color: #86868b; font-weight: 400; }
        .post-title {
            font-size: 24px;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 12px;
            line-height: 1.3;
            letter-spacing: -0.01em;
            padding-right: 40px;
        }
        .post-annotation {
            font-size: 15px;
            line-height: 1.6;
            color: #6e6e73;
            font-weight: 400;
        }
        .modal {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(20px);
            z-index: 1000;
            overflow-y: auto;
            animation: fadeIn 0.2s ease;
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .modal-content {
            background: #fff;
            max-width: 800px;
            margin: 60px auto;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
            animation: slideUp 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .modal-content::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #667eea 100%);
        }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .modal-header {
            padding: 40px 40px 0;
            border-bottom: 1px solid #f5f5f7;
        }
        .close-modal {
            float: right;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            color: #86868b;
            font-size: 24px;
            border-radius: 50%;
            transition: all 0.2s ease;
            margin: -8px -8px 0 0;
        }
        .close-modal:hover { background: #f5f5f7; color: #1d1d1f; }
        .modal-meta {
            display: flex;
            gap: 16px;
            align-items: center;
            padding: 20px 0;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .modal-source {
            color: #1d1d1f;
            font-weight: 600;
            position: relative;
            padding-left: 12px;
        }
        .modal-source::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        .modal-date { color: #86868b; }
        .modal-title {
            font-size: 40px;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 20px;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }
        .modal-annotation {
            font-size: 17px;
            line-height: 1.7;
            color: #6e6e73;
            padding: 30px 40px;
            background: #f5f5f7;
            font-weight: 400;
            border-left: 3px solid transparent;
            border-image: linear-gradient(180deg, #667eea, #764ba2, #f093fb) 1;
        }
        .modal-text {
            padding: 40px;
            font-size: 17px;
            line-height: 1.8;
            color: #1d1d1f;
            white-space: pre-wrap;
            font-weight: 400;
        }
        footer {
            text-align: center;
            padding: 60px 0;
            color: #86868b;
            font-size: 13px;
            border-top: 1px solid #d2d2d7;
            background: #fff;
        }
        @media (max-width: 1200px) { .main-wrapper { max-width: 100%; } }
        @media (max-width: 768px) {
            .container { padding: 0 24px; }
            header h1 { font-size: 40px; }
            .subtitle-en { font-size: 20px; }
            .post-card { padding: 24px; }
            .post-card::before { left: 24px; right: 24px; }
            .post-card::after { right: 24px; top: 24px; }
            .post-title { font-size: 20px; }
            .modal-content { margin: 20px; border-radius: 12px; }
            .modal-header { padding: 24px 24px 0; }
            .modal-title { font-size: 28px; }
            .modal-annotation { padding: 20px 24px; }
            .modal-text { padding: 24px; }
            nav { padding: 20px 0; }
        }
    </style>
</head>
<body>
    <div class="main-wrapper">
        <header>
            <div class="container">
                <div class="logo">Живой опыт</div>
                <h1>Addiction & Creation</h1>
                <div class="subtitle-en">Personal Journey</div>
                <div class="tagline">I choose something else</div>
            </div>
        </header>
        <nav>
            <button class="nav-btn active" onclick="switchSection(1)">Зависимость и 12 шагов</button>
            <button class="nav-btn" onclick="switchSection(2)">Творческие лайфсториз</button>
        </nav>
        <div class="container">
            <div class="section-info" id="sectionInfo"></div>
            <div class="posts-grid" id="postsGrid"></div>
        </div>
        <footer>
            <div class="container"><p>© 2025 Живой опыт. Все права защищены.</p></div>
        </footer>
    </div>
    <div class="modal" id="modal" onclick="handleModalClick(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <span class="close-modal" onclick="closeModal()">×</span>
                <div id="modalHeader"></div>
            </div>
            <div id="modalBody"></div>
        </div>
    </div>
    <script>
        // Данные встроены непосредственно в код
        const section1Posts = ''' + json.dumps(section1, ensure_ascii=False, indent=2) + ''';

        const section2Posts = ''' + json.dumps(section2, ensure_ascii=False, indent=2) + ''';

        let currentSection = 1;

        function switchSection(sectionNum) {
            currentSection = sectionNum;
            document.querySelectorAll('.nav-btn').forEach((btn, idx) => {
                btn.classList.toggle('active', idx + 1 === sectionNum);
            });
            renderPosts();
        }

        function renderPosts() {
            const posts = currentSection === 1 ? section1Posts : section2Posts;
            const grid = document.getElementById('postsGrid');
            const info = document.getElementById('sectionInfo');
            info.textContent = posts.length + ' ' + getPluralForm(posts.length, 'пост', 'поста', 'постов');
            grid.innerHTML = posts.map((post, index) => `
                <div class="post-card" onclick="openPost(${index})">
                    <div class="post-meta">
                        <span class="post-source">${escapeHtml(post.source)}</span>
                        <span class="post-date">${escapeHtml(post.display_date)}</span>
                    </div>
                    <div class="post-title">${escapeHtml(post.final_title)}</div>
                    <div class="post-annotation">${escapeHtml(post.final_annotation)}</div>
                </div>
            `).join('');
        }

        function openPost(index) {
            const posts = currentSection === 1 ? section1Posts : section2Posts;
            const post = posts[index];
            const modal = document.getElementById('modal');
            const header = document.getElementById('modalHeader');
            const body = document.getElementById('modalBody');
            header.innerHTML = `
                <div class="modal-meta">
                    <span class="modal-source">${escapeHtml(post.source)}</span>
                    <span class="modal-date">${escapeHtml(post.display_date)}</span>
                </div>
                <div class="modal-title">${escapeHtml(post.final_title)}</div>
            `;
            body.innerHTML = `
                <div class="modal-annotation">${escapeHtml(post.final_annotation)}</div>
                <div class="modal-text">${escapeHtml(post.full_content)}</div>
            `;
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }

        function closeModal() {
            document.getElementById('modal').style.display = 'none';
            document.body.style.overflow = 'auto';
        }

        function handleModalClick(event) {
            if (event.target.id === 'modal') closeModal();
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text || '';
            return div.innerHTML;
        }

        function getPluralForm(number, one, two, five) {
            let n = Math.abs(number);
            n %= 100;
            if (n >= 5 && n <= 20) return five;
            n %= 10;
            if (n === 1) return one;
            if (n >= 2 && n <= 4) return two;
            return five;
        }

        // Инициализация при загрузке страницы
        document.addEventListener('DOMContentLoaded', () => {
            renderPosts();
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') closeModal();
            });
        });
    </script>
</body>
</html>'''

# Save as .txt for easy copying
with open('ПОЛНЫЙ_КОД_ДЛЯ_ТИЛЬДЫ.txt', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Создан файл ПОЛНЫЙ_КОД_ДЛЯ_ТИЛЬДЫ.txt")
print(f"📊 Секция 1: {len(section1)} постов")
print(f"📊 Секция 2: {len(section2)} постов")
print(f"📄 Размер файла: {len(html_content):,} символов")
