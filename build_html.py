import pandas as pd
import json
import re
import os

file1 = 'C:/dashboard/퐁티_1_300.xls'
file2 = 'C:/dashboard/퐁티_301_600.xls'

try:
    df1 = pd.read_excel(file1, engine='xlrd')
    df2 = pd.read_excel(file2, engine='xlrd')
    df = pd.concat([df1, df2], ignore_index=True)
except Exception as e:
    print('Error reading excel:', e)
    df = pd.DataFrame()

if not df.empty:
    df.columns = df.columns.str.strip().str.replace('\n', '')
    if '논문명' in df.columns and '저자명' in df.columns:
        df = df.drop_duplicates(subset=['논문명', '저자명'], keep='first')
        
    df['발행연도'] = pd.to_numeric(df.get('발행연도'), errors='coerce').fillna(2000).astype(int)
    df['인용된 총 횟수'] = pd.to_numeric(df.get('인용된 총 횟수'), errors='coerce').fillna(0).astype(int)
    df['저자명'] = df.get('저자명', pd.Series()).fillna('미상')
    df['학술지명'] = df.get('학술지명', pd.Series()).fillna('미상')
    df['초록'] = df.get('초록', pd.Series()).fillna('')
    df['저자키워드'] = df.get('저자키워드', pd.Series()).fillna('')

    stopwords = ['연구', '분석', '고찰', '현상학', '메를로', '퐁티', '철학', '메를로퐁티', '의미', '현대', '문제', '대한', '통한', '중심', '이해', '방법론', '사유']
    def extract_keywords(text):
        if not text: return []
        words = []
        for match in re.finditer(r'[가-힣]{2,}', str(text)):
            w = match.group()
            if w not in stopwords:
                words.append(w)
        return words
    df['저자키워드_추출'] = df['저자키워드'].apply(extract_keywords)

    records = df[['발행연도', '논문명', '저자명', '학술지명', '인용된 총 횟수', '초록', '저자키워드_추출']].to_dict('records')
    json_data = json.dumps(records, ensure_ascii=False)
else:
    json_data = '[]'

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Merleau-Ponty Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body {{
            background-color: #1e1e24;
            color: #ffffff;
            font-family: 'Malgun Gothic', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        h1 {{ color: #a47af0; text-align: center; margin-bottom: 5px; }}
        h4 {{ color: #d0bfff; text-align: center; margin-top: 0; margin-bottom: 30px; font-weight: normal; }}
        .tab-buttons {{ display: flex; border-bottom: 2px solid #3F0099; margin-bottom: 20px; }}
        .tab-btn {{
            background-color: transparent; border: none; color: #a47af0;
            padding: 10px 20px; font-size: 16px; cursor: pointer; transition: 0.3s;
        }}
        .tab-btn:hover {{ background-color: rgba(63, 0, 153, 0.3); }}
        .tab-btn.active {{ background-color: #3F0099; color: #fff; font-weight: bold; border-radius: 5px 5px 0 0; }}
        .tab-content {{ display: none; background-color: #2b2b36; padding: 20px; border-radius: 0 5px 5px 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
        .tab-content.active {{ display: block; }}
        .chart-container {{ width: 100%; height: 500px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #3F0099; }}
        th {{ background-color: #3F0099; color: white; cursor: pointer; }}
        th:hover {{ background-color: #5511b8; }}
        tr:hover {{ background-color: rgba(63, 0, 153, 0.2); }}
        .search-box {{ width: 100%; padding: 10px; box-sizing: border-box; background-color: #1e1e24; border: 1px solid #3F0099; color: white; border-radius: 5px; margin-bottom: 10px; }}
        .search-box:focus {{ outline: none; border-color: #a47af0; }}
        .abstract-details {{ display: none; background-color: #1e1e24; padding: 15px; margin-top: 5px; border-left: 3px solid #a47af0; font-size: 0.9em; line-height: 1.5; }}
        .row-item {{ cursor: pointer; }}
    </style>
</head>
<body>

    <h1>📊 모리스 메를로-퐁티 연구 대시보드</h1>
    <h4>한국연구재단(KCI) 데이터를 바탕으로 한 졸업 논문 예비탐색 네비게이션 (Static Version)</h4>

    <div class="tab-buttons">
        <button class="tab-btn active" onclick="openTab(event, 'tab1')">📊 Total Insight</button>
        <button class="tab-btn" onclick="openTab(event, 'tab2')">🧭 Concept Map</button>
        <button class="tab-btn" onclick="openTab(event, 'tab3')">📚 Library</button>
    </div>

    <div id="tab1" class="tab-content active">
        <h2 style="color:#a47af0;">Total Insight</h2>
        <div id="trend-chart" class="chart-container"></div>
    </div>

    <div id="tab2" class="tab-content">
        <h2 style="color:#a47af0;">Concept Map</h2>
        <div id="bar-chart" class="chart-container"></div>
    </div>

    <div id="tab3" class="tab-content">
        <h2 style="color:#a47af0;">Research Library</h2>
        <input type="text" id="search-input" class="search-box" placeholder="🔎 논문명이나 저자명을 검색하세요...">
        <table id="data-table">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">발행연도 ↕</th>
                    <th onclick="sortTable(1)">논문명 ↕</th>
                    <th onclick="sortTable(2)">저자명 ↕</th>
                    <th onclick="sortTable(3)">학술지명 ↕</th>
                    <th onclick="sortTable(4)">인용 수 ↕</th>
                </tr>
            </thead>
            <tbody id="table-body">
            </tbody>
        </table>
    </div>

    <script>
        // 파이썬으로 처리된 엑셀 데이터가 여기에 JSON 형태로 직접 박힙니다.
        const rawData = {json_data};

        function openTab(evt, tabName) {{
            let i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {{ tabcontent[i].style.display = "none"; tabcontent[i].className = tabcontent[i].className.replace(" active", ""); }}
            tablinks = document.getElementsByClassName("tab-btn");
            for (i = 0; i < tablinks.length; i++) {{ tablinks[i].className = tablinks[i].className.replace(" active", ""); }}
            document.getElementById(tabName).style.display = "block";
            document.getElementById(tabName).className += " active";
            evt.currentTarget.className += " active";
            
            if (tabName === 'tab1') renderTrendChart();
            if (tabName === 'tab2') renderBarChart();
        }}

        const plotlyLayoutTemplate = {{
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            font: {{ color: '#ffffff', family: 'Malgun Gothic' }},
            margin: {{ t: 40, b: 40, l: 40, r: 40 }}
        }};

        // 1. Total Insight 렌더링
        function renderTrendChart() {{
            const yearMap = {{}};
            rawData.forEach(d => {{
                if (!yearMap[d.발행연도]) yearMap[d.발행연도] = {{ count: 0, citation: 0 }};
                yearMap[d.발행연도].count += 1;
                yearMap[d.발행연도].citation += d['인용된 총 횟수'];
            }});
            const years = Object.keys(yearMap).sort((a,b) => a-b);
            const counts = years.map(y => yearMap[y].count);
            const citations = years.map(y => yearMap[y].citation);

            const trace1 = {{
                x: years, y: counts, name: '발행된 논문 수', type: 'bar', marker: {{ color: '#8A2BE2' }}
            }};
            const trace2 = {{
                x: years, y: citations, name: '총 피인용 수', type: 'scatter', mode: 'lines+markers', yaxis: 'y2', line: {{ color: '#FF4B4B', width: 3 }}
            }};

            const layout = {{
                ...plotlyLayoutTemplate,
                title: '연도별 발행 및 피인용 수 추이',
                xaxis: {{ title: '발행 연도', showgrid: false }},
                yaxis: {{ title: '발행 건수', showgrid: true, gridcolor: '#444' }},
                yaxis2: {{ title: '피인용 수', overlaying: 'y', side: 'right', showgrid: false }},
                hovermode: 'x unified',
                legend: {{ orientation: 'h', y: 1.1 }}
            }};

            Plotly.newPlot('trend-chart', [trace1, trace2], layout, {{responsive: true}});
        }}

        // 2. Concept Map 렌더링
        function renderBarChart() {{
            const wordCount = {{}};
            rawData.forEach(d => {{
                d['저자키워드_추출'].forEach(w => {{
                    wordCount[w] = (wordCount[w] || 0) + 1;
                }});
            }});
            const sortedWords = Object.keys(wordCount).map(w => ({{word: w, count: wordCount[w]}})).sort((a,b) => b.count - a.count).slice(0, 15);
            // Reverse for horizontal bar chart
            sortedWords.reverse();
            
            const trace = {{
                y: sortedWords.map(d => d.word),
                x: sortedWords.map(d => d.count),
                type: 'bar',
                orientation: 'h',
                marker: {{ color: '#a47af0' }},
                text: sortedWords.map(d => String(d.count)),
                textposition: 'auto'
            }};

            const layout = {{
                ...plotlyLayoutTemplate,
                title: '상위 15개 핵심어 빈도',
                xaxis: {{ title: '빈도수', showgrid: true, gridcolor: '#444' }},
                yaxis: {{ title: '', showgrid: false }}
            }};

            Plotly.newPlot('bar-chart', [trace], layout, {{responsive: true}});
        }}

        // 3. Library Table 렌더링
        let sortCol = -1;
        let sortAsc = true;
        let currentData = [...rawData];

        function renderTable(data) {{
            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';
            data.forEach((d, index) => {{
                const tr = document.createElement('tr');
                tr.className = 'row-item';
                tr.onclick = () => toggleAbstract(index);
                
                tr.innerHTML = `
                    <td>${{d.발행연도}}</td>
                    <td>${{d.논문명}}</td>
                    <td>${{d.저자명}}</td>
                    <td>${{d.학술지명}}</td>
                    <td>${{d['인용된 총 횟수']}}</td>
                `;
                tbody.appendChild(tr);

                const trDetails = document.createElement('tr');
                const tdDetails = document.createElement('td');
                tdDetails.colSpan = 5;
                tdDetails.style.padding = "0";
                tdDetails.style.border = "none";
                
                const detailDiv = document.createElement('div');
                detailDiv.className = 'abstract-details';
                detailDiv.id = 'abstract-' + index;
                detailDiv.innerHTML = `<strong>초록:</strong><br>${{d.초록 ? d.초록 : '초록 정보가 없습니다.'}}<br><br><strong>추출 키워드:</strong> ${{d['저자키워드_추출'].join(', ')}}`;
                
                tdDetails.appendChild(detailDiv);
                trDetails.appendChild(tdDetails);
                tbody.appendChild(trDetails);
            }});
        }}

        function toggleAbstract(index) {{
            const div = document.getElementById('abstract-' + index);
            div.style.display = div.style.display === 'block' ? 'none' : 'block';
        }}

        function sortTable(colIdx) {{
            const keys = ['발행연도', '논문명', '저자명', '학술지명', '인용된 총 횟수'];
            const key = keys[colIdx];
            
            if (sortCol === colIdx) sortAsc = !sortAsc;
            else {{ sortCol = colIdx; sortAsc = true; }}
            
            currentData.sort((a, b) => {{
                let valA = a[key]; let valB = b[key];
                if (typeof valA === 'string') valA = valA.toLowerCase();
                if (typeof valB === 'string') valB = valB.toLowerCase();
                if (valA < valB) return sortAsc ? -1 : 1;
                if (valA > valB) return sortAsc ? 1 : -1;
                return 0;
            }});
            renderTable(currentData);
        }}

        document.getElementById('search-input').addEventListener('input', function(e) {{
            const term = e.target.value.toLowerCase();
            currentData = rawData.filter(d => 
                d.논문명.toLowerCase().includes(term) || d.저자명.toLowerCase().includes(term)
            );
            renderTable(currentData);
        }});

        // 초기화
        currentData.sort((a,b) => b['인용된 총 횟수'] - a['인용된 총 횟수']); // 기본: 인용수 내림차순
        renderTable(currentData);
        renderTrendChart();
    </script>
</body>
</html>"""

with open('C:/dashboard/pure_js_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
