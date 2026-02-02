#!/usr/bin/env python3
"""
Генератор сайта для чтения постов о зависимости, трезвости и 12 шагах
"""
import json
from pathlib import Path

def generate_html_site(posts_file, output_file):
    """Генерирует HTML сайт из JSON файла с постами"""

    # Загружаем посты
    with open(posts_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    # HTML шаблон
    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Зависимость, Трезвость и 12 Шагов - {len(posts)} постов</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.8;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .controls {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .search-box {{
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            margin-bottom: 20px;
            transition: all 0.3s;
        }}

        .search-box:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.2);
        }}

        .filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }}

        .filter-btn {{
            padding: 10px 20px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .filter-btn:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        .filter-btn.active {{
            background: #667eea;
            color: white;
        }}

        .stats {{
            color: #666;
            font-size: 14px;
            margin-top: 15px;
            text-align: center;
        }}

        .posts-grid {{
            display: grid;
            gap: 20px;
        }}

        .post-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s;
            cursor: pointer;
            border-left: 5px solid #667eea;
        }}

        .post-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }}

        .post-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .post-source {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .source-livejournal {{
            background: #ffeaa7;
            color: #d63031;
        }}

        .source-vivse, .source-vivsenepr {{
            background: #dfe6e9;
            color: #2d3436;
        }}

        .source-daily2025 {{
            background: #a29bfe;
            color: #6c5ce7;
        }}

        .source-olydaily {{
            background: #fab1a0;
            color: #e17055;
        }}

        .source-instagram {{
            background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
            color: white;
        }}

        .post-date {{
            color: #7f8c8d;
            font-size: 14px;
        }}

        .post-title {{
            font-size: 1.3em;
            color: #2c3e50;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        .post-annotation {{
            color: #7f8c8d;
            font-style: italic;
            font-size: 0.95em;
            margin-bottom: 10px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }}

        .post-preview {{
            color: #555;
            line-height: 1.6;
            margin-bottom: 15px;
        }}

        .read-more {{
            color: #667eea;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            transition: all 0.3s;
        }}

        .read-more:hover {{
            color: #764ba2;
            gap: 10px;
        }}

        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            overflow-y: auto;
            padding: 20px;
        }}

        .modal-content {{
            background: white;
            max-width: 900px;
            margin: 40px auto;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            position: relative;
        }}

        .close-modal {{
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 30px;
            color: #999;
            cursor: pointer;
            transition: all 0.3s;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
        }}

        .close-modal:hover {{
            color: #667eea;
            background: #f0f0f0;
            transform: rotate(90deg);
        }}

        .modal-post-content {{
            white-space: pre-wrap;
            line-height: 1.8;
            font-size: 16px;
        }}

        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #7f8c8d;
            font-size: 1.2em;
        }}

        .scroll-to-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #667eea;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: none;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 24px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            transition: all 0.3s;
            z-index: 999;
        }}

        .scroll-to-top:hover {{
            background: #764ba2;
            transform: translateY(-5px);
        }}

        .scroll-to-top.visible {{
            display: flex;
        }}

        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
            }}

            .modal-content {{
                padding: 20px;
                margin: 20px auto;
            }}

            .post-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Зависимость, Трезвость и 12 Шагов</h1>
            <p>Коллекция из {len(posts)} постов о выздоровлении и самопознании</p>
        </header>

        <div class="controls">
            <input
                type="text"
                class="search-box"
                id="searchBox"
                placeholder="Поиск по тексту, аннотациям и заголовкам постов..."
            >

            <div class="filters">
                <button class="filter-btn active" data-filter="all">Все источники</button>
                <button class="filter-btn" data-filter="Instagram">Instagram</button>
                <button class="filter-btn" data-filter="LiveJournal">LiveJournal</button>
                <button class="filter-btn" data-filter="Vi Vse Nepr">Vi Vse Nepr</button>
                <button class="filter-btn" data-filter="Daily2025">Daily2025</button>
                <button class="filter-btn" data-filter="OlyDaily">OlyDaily</button>
            </div>

            <div class="stats" id="stats">
                Показано постов: {len(posts)} из {len(posts)}
            </div>
        </div>

        <div class="posts-grid" id="postsGrid"></div>
    </div>

    <div class="modal" id="modal">
        <div class="modal-content">
            <span class="close-modal" id="closeModal">&times;</span>
            <div id="modalContent"></div>
        </div>
    </div>

    <div class="scroll-to-top" id="scrollToTop">↑</div>

    <script>
        const allPosts = {json.dumps(posts, ensure_ascii=False)};

        let currentFilter = 'all';
        let searchQuery = '';

        function filterPosts() {{
            return allPosts.filter(post => {{
                const matchesFilter = currentFilter === 'all' || post.source === currentFilter;
                const searchLower = searchQuery.toLowerCase();
                const matchesSearch = searchQuery === '' ||
                    post.title.toLowerCase().includes(searchLower) ||
                    (post.annotation && post.annotation.toLowerCase().includes(searchLower)) ||
                    post.full_content.toLowerCase().includes(searchLower);
                return matchesFilter && matchesSearch;
            }});
        }}

        function renderPosts() {{
            const filtered = filterPosts();
            const grid = document.getElementById('postsGrid');

            if (filtered.length === 0) {{
                grid.innerHTML = '<div class="no-results">Постов не найдено. Попробуйте изменить фильтры или поисковый запрос.</div>';
                return;
            }}

            grid.innerHTML = filtered.map((post, index) => {{
                const sourceClass = post.source.toLowerCase().replace(/ /g, '');
                const preview = post.preview || post.full_content.substring(0, 300);
                const safePreview = preview.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '...';

                const annotationHtml = post.annotation
                    ? `<div class="post-annotation">${{post.annotation}}</div>`
                    : '';

                return `
                    <div class="post-card" onclick="openPost(${{allPosts.indexOf(post)}})">
                        <div class="post-header">
                            <span class="post-source source-${{sourceClass}}">${{post.source}}</span>
                            <span class="post-date">${{post.date}}</span>
                        </div>
                        <div class="post-title">${{post.title}}</div>
                        ${{annotationHtml}}
                        <div class="post-preview">${{safePreview}}</div>
                        <a class="read-more">Читать полностью →</a>
                    </div>
                `;
            }}).join('');

            updateStats();
        }}

        function openPost(index) {{
            const post = allPosts[index];
            const modal = document.getElementById('modal');
            const modalContent = document.getElementById('modalContent');

            const sourceClass = post.source.toLowerCase().replace(/ /g, '');
            const annotationHtml = post.annotation
                ? `<div class="post-annotation" style="font-size: 1.1em; margin: 20px 0;">${{post.annotation}}</div>`
                : '';

            modalContent.innerHTML = `
                <div class="post-header">
                    <span class="post-source source-${{sourceClass}}">${{post.source}}</span>
                    <span class="post-date">${{post.date}}</span>
                </div>
                <div class="post-title" style="font-size: 2em; margin: 20px 0;">${{post.title}}</div>
                ${{annotationHtml}}
                <div class="modal-post-content">${{post.full_content.replace(/</g, '&lt;').replace(/>/g, '&gt;')}}</div>
            `;

            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }}

        function closeModal() {{
            const modal = document.getElementById('modal');
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }}

        function updateStats() {{
            const filtered = filterPosts();
            const stats = document.getElementById('stats');
            stats.textContent = `Показано постов: ${{filtered.length}} из ${{allPosts.length}}`;
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            renderPosts();

            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.addEventListener('click', (e) => {{
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    currentFilter = e.target.dataset.filter;
                    renderPosts();
                }});
            }});

            document.getElementById('searchBox').addEventListener('input', (e) => {{
                searchQuery = e.target.value;
                renderPosts();
            }});

            document.getElementById('closeModal').addEventListener('click', closeModal);
            document.getElementById('modal').addEventListener('click', (e) => {{
                if (e.target.id === 'modal') {{
                    closeModal();
                }}
            }});

            const scrollBtn = document.getElementById('scrollToTop');
            window.addEventListener('scroll', () => {{
                if (window.scrollY > 300) {{
                    scrollBtn.classList.add('visible');
                }} else {{
                    scrollBtn.classList.remove('visible');
                }}
            }});

            scrollBtn.addEventListener('click', () => {{
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }});

            document.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape') {{
                    closeModal();
                }}
            }});
        }});
    </script>
</body>
</html>'''

    # Сохраняем HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Создан файл {output_file} с {len(posts)} постами")

if __name__ == '__main__':
    # Сначала используем файл без аннотаций
    generate_html_site('all_addiction_posts_full.json', 'addiction_site.html')
    print("\nСайт создан! Откройте addiction_site.html в браузере.")
    print("Аннотации будут добавлены, когда агент закончит обработку.")
