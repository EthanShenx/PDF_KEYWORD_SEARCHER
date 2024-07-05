import fitz
import re
import os

def extract_text_from_pdf(pdf_path):
    text_lines = []
    with fitz.open(pdf_path) as document:
        for page_num in range(len(document)):
            page = document[page_num]
            text = page.get_text("text")
            text_lines.extend(text.splitlines())
    return text_lines

def find_matching_strings(text_lines, patterns):
    matches = {pattern: [] for pattern in patterns}
    for i, line in enumerate(text_lines):
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                matches[pattern].append((i, line))
    return matches

def search_in_pdfs(directory, patterns):
    results = {pattern: [] for pattern in patterns}
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            try:
                text_lines = extract_text_from_pdf(pdf_path)
                matches = find_matching_strings(text_lines, patterns)
                for pattern, found in matches.items():
                    for line_info in found:
                        results[pattern].append((filename, line_info[0], line_info[1]))
            except Exception as e:
                print(f"处理文件 {filename} 时出错：{e}")
    return results

def analyze_results(results, output_file_path, patterns):
    unique_queries_1 = set()
    unique_queries_2 = set()
    all_lines = ""

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("匹配成功的结果：\n")
        file.write("-------------------------------------\n")
        for pattern, matches in results.items():
            for filename, line_number, line_content in matches:
                file.write(f"查找项 '{pattern}' 在文件 '{filename}' 找到：'{line_content}' \n")

    with open(output_file_path, 'r', encoding='utf-8') as fileforsearch:
        for eachline in fileforsearch:
            all_lines += eachline.strip() + "\n"
        for query in patterns:
            if query in all_lines:
                unique_queries_1.add(str.upper(query))
            else:
                unique_queries_2.add(str.upper(query))

    print("----------------------------------------------")
    print("在给定的文章中至少找到一个匹配的查询：")
    print("数量:" + str(len(unique_queries_1)))
    print(unique_queries_1)
    print("----------------------------------------------")
    print("在这些文章中找不到任何查询：")
    print("数量:" + str(len(unique_queries_2)))
    print(unique_queries_2)
    print("-----------------------------------------------")
    print("所有查询的数量: " + str(len(patterns)))
