# Copyright 2024 Liu Siyao
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import urllib.parse
from typing import List

from rapidfuzz import fuzz

from pptx2md.types import ConversionConfig, ElementType, ParsedPresentation, SlideElement, SlideType, TextRun, VideoElement
from pptx2md.utils import rgb_to_hex


class Formatter:

    def __init__(self, config: ConversionConfig):
        os.makedirs(config.output_path.parent, exist_ok=True)
        self.ofile = open(config.output_path, 'w', encoding='utf8')
        self.config = config

    def output(self, presentation_data: ParsedPresentation):
        """输出解析后的演示文稿到文件"""
        self.put_header()
        
        for slide_idx, slide in enumerate(presentation_data.slides):
            if slide.type == SlideType.General:
                for element in slide.elements:
                    if element.type == ElementType.Title:
                        self.put_title(element.content, element.level)
                    elif element.type == ElementType.ListItem:
                        self.put_list(self.get_formatted_runs(element.content), element.level)
                    elif element.type == ElementType.Paragraph:
                        self.put_para(self.get_formatted_runs(element.content))
                    elif element.type == ElementType.Image:
                        self.put_image(element.path, element.width)
                    elif element.type == ElementType.Video:
                        self.put_video(element.path, element.width, element.mime_type, getattr(element, 'is_external', False))
                    elif element.type == ElementType.Table:
                        self.put_table(element.content)
            elif slide.type == SlideType.MultiColumn:
                # 处理多列幻灯片
                for element in slide.preface:
                    if element.type == ElementType.Title:
                        self.put_title(element.content, element.level)
                    elif element.type == ElementType.ListItem:
                        self.put_list(self.get_formatted_runs(element.content), element.level)
                    elif element.type == ElementType.Paragraph:
                        self.put_para(self.get_formatted_runs(element.content))
                    elif element.type == ElementType.Image:
                        self.put_image(element.path, element.width)
                    elif element.type == ElementType.Video:
                        self.put_video(element.path, element.width, element.mime_type, getattr(element, 'is_external', False))
                    elif element.type == ElementType.Table:
                        self.put_table(element.content)
                
                # 处理列
                for column in slide.columns:
                    for element in column:
                        if element.type == ElementType.Title:
                            self.put_title(element.content, element.level)
                        elif element.type == ElementType.ListItem:
                            self.put_list(self.get_formatted_runs(element.content), element.level)
                        elif element.type == ElementType.Paragraph:
                            self.put_para(self.get_formatted_runs(element.content))
                        elif element.type == ElementType.Image:
                            self.put_image(element.path, element.width)
                        elif element.type == ElementType.Video:
                            self.put_video(element.path, element.width, element.mime_type, getattr(element, 'is_external', False))
                        elif element.type == ElementType.Table:
                            self.put_table(element.content)
            
            # 添加幻灯片分隔符
            if self.config.enable_slides and slide_idx < len(presentation_data.slides) - 1:
                self.ofile.write('\n---\n\n')
            
            # 添加演讲者备注
            if not self.config.disable_notes and slide.notes:
                self.ofile.write('\n\n')
                for note in slide.notes:
                    self.ofile.write(f'> {note}\n\n')
        
        self.flush()
        self.close()

    def put_header(self):
        pass

    def put_title(self, text, level):
        pass

    def put_list(self, text, level):
        pass

    def put_list_header(self):
        self.put_para('')

    def put_list_footer(self):
        self.put_para('')

    def get_formatted_runs(self, runs: List[TextRun]):
        """格式化文本运行列表，处理加粗、斜体、颜色等样式"""
        if not runs:
            return ""
        
        # 合并相同样式的连续文本
        merged_runs = []
        current_run = runs[0]
        
        for i in range(1, len(runs)):
            next_run = runs[i]
            # 如果当前文本和下一个文本的样式相同，合并它们
            if (current_run.style.is_accent == next_run.style.is_accent and
                current_run.style.is_strong == next_run.style.is_strong and
                current_run.style.color_rgb == next_run.style.color_rgb and
                current_run.style.hyperlink == next_run.style.hyperlink):
                current_run.text += next_run.text
            else:
                merged_runs.append(current_run)
                current_run = next_run
        
        merged_runs.append(current_run)
        
        # 处理合并后的文本
        res = ""
        for run in merged_runs:
            text = run.text
            
            if not self.config.disable_escaping:
                text = self.get_escaped(text)
            
            if run.style.hyperlink:
                text = self.get_hyperlink(text, run.style.hyperlink)
            if run.style.is_accent:
                text = self.get_accent(text)
            elif run.style.is_strong:
                text = self.get_strong(text)
            if run.style.color_rgb and not self.config.disable_color:
                text = self.get_colored(text, run.style.color_rgb)
            
            res += text
        return res.strip()

    def put_para(self, text):
        pass

    def put_image(self, path, max_width):
        pass

    def put_video(self, path, max_width=None, mime_type=None, is_external=False):
        """输出视频元素，使用开闭标签格式"""
        # 处理外部链接视频
        if is_external:
            if max_width is None:
                self.ofile.write(f'<video controls src="{path}"></video>\n\n')
            else:
                self.ofile.write(f'<video controls src="{path}" style="max-width:{max_width}px;"></video>\n\n')
            return
        
        # 处理本地视频
        if max_width is None:
            self.ofile.write(f'<video controls src="{urllib.parse.quote(path)}"></video>\n\n')
        else:
            self.ofile.write(f'<video controls src="{urllib.parse.quote(path)}" style="max-width:{max_width}px;"></video>\n\n')

    def put_table(self, table):
        # 确保表格内容是正确的格式
        if not table or not isinstance(table, list):
            return
        
        # 处理表格内容，确保每个单元格都是字符串
        processed_table = []
        for row in table:
            processed_row = []
            for cell in row:
                # 如果单元格是列表（TextRun列表），转换为格式化文本
                if isinstance(cell, list):
                    cell_text = self.get_formatted_runs(cell)
                    processed_row.append(cell_text)
                # 如果单元格已经是字符串
                elif isinstance(cell, str):
                    processed_row.append(cell)
                # 其他情况，转换为字符串
                else:
                    processed_row.append(str(cell))
            processed_table.append(processed_row)
        
        # 使用处理后的表格内容
        gen_table_row = lambda row: '| ' + ' | '.join([c.replace('\n', '<br />') for c in row]) + ' |'
        
        if len(processed_table) == 0:
            return
        
        self.ofile.write(gen_table_row(processed_table[0]) + '\n')
        self.ofile.write(gen_table_row(['---'] * len(processed_table[0])) + '\n')
        
        for row in processed_table[1:]:
            self.ofile.write(gen_table_row(row) + '\n')
        
        self.ofile.write('\n')

    def get_accent(self, text):
        pass

    def get_strong(self, text):
        pass

    def get_colored(self, text, rgb):
        pass

    def get_hyperlink(self, text, url):
        pass

    def get_escaped(self, text):
        pass

    def write(self, text):
        self.ofile.write(text)

    def flush(self):
        self.ofile.flush()

    def close(self):
        self.ofile.close()


class MarkdownFormatter(Formatter):
    # write outputs to markdown
    def __init__(self, config: ConversionConfig):
        super().__init__(config)
        self.esc_re1 = re.compile(r'([\\\*`!_\{\}\[\]\(\)#\+-\.])')
        self.esc_re2 = re.compile(r'(<[^>]+>)')
        self.list_level = 0

    def put_title(self, text, level):
        self.ofile.write('#' * level + ' ' + text + '\n\n')

    def put_list(self, text, level):
        self.ofile.write('  ' * (level - 1) + '* ' + text + '\n')

    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, max_width=None):
        if max_width is None:
            self.ofile.write(f'![image]({urllib.parse.quote(path)})\n\n')
        else:
            self.ofile.write(f'<img src="{urllib.parse.quote(path)}" style="max-width:{max_width}px;" />\n\n')

    def put_video(self, path, max_width=None, mime_type=None, is_external=False):
        """输出视频元素，使用开闭标签格式"""
        # 处理外部链接视频
        if is_external:
            if max_width is None:
                self.ofile.write(f'<video controls src="{path}"></video>\n\n')
            else:
                self.ofile.write(f'<video controls src="{path}" style="max-width:{max_width}px;"></video>\n\n')
            return
        
        # 处理本地视频
        if max_width is None:
            self.ofile.write(f'<video controls src="{urllib.parse.quote(path)}"></video>\n\n')
        else:
            self.ofile.write(f'<video controls src="{urllib.parse.quote(path)}" style="max-width:{max_width}px;"></video>\n\n')

    def get_accent(self, text):
        return '*' + text + '*'

    def get_strong(self, text):
        return '**' + text + '**'

    def get_colored(self, text, rgb):
        # 检查是否是白色或接近白色
        r, g, b = rgb
        if r > 240 and g > 240 and b > 240:  # 接近白色的颜色
            return text  # 不添加颜色样式
        return f'<span style="color:rgb{rgb};">{text}</span>'

    def get_hyperlink(self, text, url):
        return f'[{text}]({url})'

    def esc_repl(self, match):
        return '\\' + match.group(0)

    def get_escaped(self, text):
        if self.config.disable_escaping:
            return text
        return re.sub(r'([\\`\*_\{\}\[\]\(\)#\+\-\.!])', self.esc_repl, text)

    def put_table(self, table):
        # 确保表格内容是正确的格式
        if not table or not isinstance(table, list):
            return
            
        # 处理表格内容，确保每个单元格都是字符串
        processed_table = []
        for row in table:
            processed_row = []
            for cell in row:
                # 如果单元格是列表（TextRun列表），转换为格式化文本
                if isinstance(cell, list):
                    cell_text = self.get_formatted_runs(cell)
                    processed_row.append(cell_text)
                # 如果单元格已经是字符串
                elif isinstance(cell, str):
                    processed_row.append(cell)
                # 其他情况，转换为字符串
                else:
                    processed_row.append(str(cell))
            processed_table.append(processed_row)
        
        # 使用处理后的表格内容
        gen_table_row = lambda row: '| ' + ' | '.join([c.replace('\n', '<br />') for c in row]) + ' |'
        
        if len(processed_table) == 0:
            return
        
        self.ofile.write(gen_table_row(processed_table[0]) + '\n')
        self.ofile.write(gen_table_row(['---'] * len(processed_table[0])) + '\n')
        
        for row in processed_table[1:]:
            self.ofile.write(gen_table_row(row) + '\n')
        
        self.ofile.write('\n')


class WikiFormatter(Formatter):
    # write outputs to wikitext
    def __init__(self, config: ConversionConfig):
        super().__init__(config)
        self.esc_re = re.compile(r'<([^>]+)>')
        self.list_level = 0

    def put_title(self, text, level):
        self.ofile.write('!' * level + ' ' + text + '\n\n')

    def put_list(self, text, level):
        self.ofile.write('*' * level + ' ' + text + '\n')

    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, max_width):
        if max_width is None:
            self.ofile.write(f'[img[{path}]]\n\n')
        else:
            self.ofile.write(f'[img width={max_width}[{path}]]\n\n')

    def put_video(self, path, max_width, mime_type, is_external=False):
        """输出视频元素，使用开闭标签格式"""
        # 处理外部链接视频
        if is_external:
            if max_width is None:
                self.ofile.write(f'<video controls src="{path}"></video>\n\n')
            else:
                self.ofile.write(f'<video controls src="{path}" style="max-width:{max_width}px;"></video>\n\n')
            return
        
        # 处理本地视频
        if max_width is None:
            self.ofile.write(f'<video controls src="{urllib.parse.quote(path)}"></video>\n\n')
        else:
            self.ofile.write(f'<video controls src="{urllib.parse.quote(path)}" style="max-width:{max_width}px;"></video>\n\n')

    def get_accent(self, text):
        return '//' + text + '//'

    def get_strong(self, text):
        return '\'\'' + text + '\'\''

    def get_colored(self, text, rgb):
        # 检查是否是白色或接近白色
        r, g, b = rgb
        if r > 240 and g > 240 and b > 240:  # 接近白色的颜色
            return text  # 不添加颜色样式
        return f'@@color:rgb{rgb};{text}@@'

    def get_hyperlink(self, text, url):
        return f'[[{url}|{text}]]'

    def esc_repl(self, match):
        return '\\' + match.group(0)

    def get_escaped(self, text):
        if self.config.disable_escaping:
            return text
        return re.sub(r'([\\`\*_\{\}\[\]\(\)#\+\-\.!])', self.esc_repl, text)

    def put_table(self, table):
        # 确保表格内容是正确的格式
        if not table or not isinstance(table, list):
            return
            
        # 处理表格内容，确保每个单元格都是字符串
        processed_table = []
        for row in table:
            processed_row = []
            for cell in row:
                # 如果单元格是列表（TextRun列表），转换为格式化文本
                if isinstance(cell, list):
                    cell_text = self.get_formatted_runs(cell)
                    processed_row.append(cell_text)
                # 如果单元格已经是字符串
                elif isinstance(cell, str):
                    processed_row.append(cell)
                # 其他情况，转换为字符串
                else:
                    processed_row.append(str(cell))
            processed_table.append(processed_row)
        
        # 使用处理后的表格内容
        self.ofile.write("|" + "|".join(["k" for _ in processed_table[0]]) + "|\n")
        
        for row in processed_table:
            self.ofile.write("|" + "|".join([c.replace('\n', '<br />') for c in row]) + "|\n")
        
        self.ofile.write('\n')


class MadokoFormatter(Formatter):
    # write outputs to madoko markdown
    def __init__(self, config: ConversionConfig):
        super().__init__(config)
        self.ofile.write('[TOC]\n\n')
        self.esc_re1 = re.compile(r'([\\\*`!_\{\}\[\]\(\)#\+-\.])')
        self.esc_re2 = re.compile(r'(<[^>]+>)')
        self.list_level = 0
        self.in_table = False

    def put_title(self, text, level):
        self.ofile.write('#' * level + ' ' + text + '\n\n')

    def put_list(self, text, level):
        self.ofile.write('  ' * (level - 1) + '* ' + text + '\n')

    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, max_width):
        if max_width is None:
            self.ofile.write(f'~ Figure: ![image]({urllib.parse.quote(path)})\n\n')
        else:
            self.ofile.write(f'~ Figure: <img src="{urllib.parse.quote(path)}" style="max-width:{max_width}px;" />\n\n')

    def put_video(self, path, max_width, mime_type, is_external=False):
        """输出视频元素，使用开闭标签格式"""
        # 处理外部链接视频
        if is_external:
            if max_width is None:
                self.ofile.write(f'~ Figure: <video controls src="{path}"></video>\n\n')
            else:
                self.ofile.write(f'~ Figure: <video controls src="{path}" style="max-width:{max_width}px;"></video>\n\n')
            return
        
        # 处理本地视频
        if max_width is None:
            self.ofile.write(f'~ Figure: <video controls src="{urllib.parse.quote(path)}"></video>\n\n')
        else:
            self.ofile.write(f'~ Figure: <video controls src="{urllib.parse.quote(path)}" style="max-width:{max_width}px;"></video>\n\n')

    def get_accent(self, text):
        return '*' + text + '*'

    def get_strong(self, text):
        return '**' + text + '**'

    def get_colored(self, text, rgb):
        # 检查是否是白色或接近白色
        r, g, b = rgb
        if r > 240 and g > 240 and b > 240:  # 接近白色的颜色
            return text  # 不添加颜色样式
        return f'<span style="color:rgb{rgb};">{text}</span>'

    def get_hyperlink(self, text, url):
        return f'[{text}]({url})'

    def esc_repl(self, match):
        return '\\' + match.group(0)

    def get_escaped(self, text):
        if self.config.disable_escaping:
            return text
        return re.sub(r'([\\`\*_\{\}\[\]\(\)#\+\-\.!])', self.esc_repl, text)

    def put_table(self, table):
        # 确保表格内容是正确的格式
        if not table or not isinstance(table, list):
            return
            
        # 处理表格内容，确保每个单元格都是字符串
        processed_table = []
        for row in table:
            processed_row = []
            for cell in row:
                # 如果单元格是列表（TextRun列表），转换为格式化文本
                if isinstance(cell, list):
                    cell_text = self.get_formatted_runs(cell)
                    processed_row.append(cell_text)
                # 如果单元格已经是字符串
                elif isinstance(cell, str):
                    processed_row.append(cell)
                # 其他情况，转换为字符串
                else:
                    processed_row.append(str(cell))
            processed_table.append(processed_row)
        
        # 使用处理后的表格内容
        self.ofile.write('~ Table\n')
        
        for row in processed_table:
            self.ofile.write('|' + '|'.join([c.replace('\n', '<br />') for c in row]) + '|\n')
        
        self.ofile.write('~\n\n')


class QuartoFormatter(Formatter):
    # write outputs to quarto markdown - reveal js
    def __init__(self, config: ConversionConfig):
        super().__init__(config)
        self.esc_re1 = re.compile(r'([\\\*`!_\{\}\[\]\(\)#\+-\.])')
        self.esc_re2 = re.compile(r'(<[^>]+>)')
        self.list_level = 0

    def output(self, presentation_data: ParsedPresentation):
        self.put_header()

        last_title = None

        def put_elements(elements: List[SlideElement]):
            nonlocal last_title

            last_element = None
            for element in elements:
                if last_element and last_element.type == ElementType.ListItem and element.type != ElementType.ListItem:
                    self.put_list_footer()

                match element.type:
                    case ElementType.Title:
                        element.content = element.content.strip()
                        if element.content:
                            if last_title and last_title.level == element.level and fuzz.ratio(
                                    last_title.content, element.content, score_cutoff=92):
                                # skip if the title is the same as the last one
                                # Allow for repeated slide titles - One or more - Add (cont.) to the title
                                if self.config.keep_similar_titles:
                                    self.put_title(f'{element.content} (cont.)', element.level)
                            else:
                                self.put_title(element.content, element.level)
                            last_title = element
                    case ElementType.ListItem:
                        if not (last_element and last_element.type == ElementType.ListItem):
                            self.put_list_header()
                        self.put_list(self.get_formatted_runs(element.content), element.level)
                    case ElementType.Paragraph:
                        self.put_para(self.get_formatted_runs(element.content))
                    case ElementType.Image:
                        self.put_image(element.path, element.width)
                    case ElementType.Video:
                        self.put_video(element.path, element.width, element.mime_type)
                    case ElementType.Table:
                        self.put_table([[self.get_formatted_runs(cell) for cell in row] for row in element.content])
                last_element = element

        for slide_idx, slide in enumerate(presentation_data.slides):
            if slide.type == SlideType.General:
                put_elements(slide.elements)
            elif slide.type == SlideType.MultiColumn:
                put_elements(slide.preface)
                if len(slide.columns) == 2:
                    width = '50%'
                elif len(slide.columns) == 3:
                    width = '33%'
                else:
                    raise ValueError(f'Unsupported number of columns: {len(slide.columns)}')

                self.put_para(':::: {.columns}')
                for column in slide.columns:
                    self.put_para(f'::: {{.column width="{width}"}}')
                    put_elements(column)
                    self.put_para(':::')
                self.put_para('::::')

            if not self.config.disable_notes and slide.notes:
                self.put_para("::: {.notes}")
                for note in slide.notes:
                    self.put_para(note)
                self.put_para(":::")

            if slide_idx < len(presentation_data.slides) - 1 and self.config.enable_slides:
                self.put_para("\n---\n")

        self.close()

    def put_header(self):
        self.ofile.write('---\n')
        self.ofile.write('title: "' + os.path.basename(self.config.pptx_path).split('.')[0] + '"\n')
        self.ofile.write('format:\n')
        self.ofile.write('  revealjs:\n')
        self.ofile.write('    slide-number: true\n')
        self.ofile.write('    chalkboard: true\n')
        self.ofile.write('    preview-links: auto\n')
        self.ofile.write('    logo: logo.png\n')
        self.ofile.write('    css: styles.css\n')
        self.ofile.write('    footer: "' + os.path.basename(self.config.pptx_path).split('.')[0] + '"\n')
        self.ofile.write('---\n\n')

    def put_title(self, text, level):
        self.ofile.write('#' * level + ' ' + text + '\n\n')

    def put_list(self, text, level):
        self.ofile.write('  ' * (level - 1) + '* ' + text + '\n')

    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, max_width=None):
        if max_width is None:
            self.ofile.write(f'![image]({urllib.parse.quote(path)})\n\n')
        else:
            self.ofile.write(f'<img src="{urllib.parse.quote(path)}" style="max-width:{max_width}px;" />\n\n')

    def put_video(self, path, max_width=None, mime_type=None, is_external=False):
        """输出视频元素，使用开闭标签格式"""
        # 处理外部链接视频
        if is_external:
            if max_width is None:
                self.ofile.write(f'<video controls src="{path}"></video>\n\n')
            else:
                self.ofile.write(f'<video controls src="{path}" style="max-width:{max_width}px;"></video>\n\n')
            return
        
        # 处理本地视频
        if max_width is None:
            self.ofile.write(f'<video controls src="{urllib.parse.quote(path)}"></video>\n\n')
        else:
            self.ofile.write(f'<video controls src="{urllib.parse.quote(path)}" style="max-width:{max_width}px;"></video>\n\n')

    def put_table(self, table):
        # 确保表格内容是正确的格式
        if not table or not isinstance(table, list):
            return
            
        # 处理表格内容，确保每个单元格都是字符串
        processed_table = []
        for row in table:
            processed_row = []
            for cell in row:
                # 如果单元格是列表（TextRun列表），转换为格式化文本
                if isinstance(cell, list):
                    cell_text = self.get_formatted_runs(cell)
                    processed_row.append(cell_text)
                # 如果单元格已经是字符串
                elif isinstance(cell, str):
                    processed_row.append(cell)
                # 其他情况，转换为字符串
                else:
                    processed_row.append(str(cell))
            processed_table.append(processed_row)
        
        # 使用处理后的表格内容
        gen_table_row = lambda row: '| ' + ' | '.join([c.replace('\n', '<br />') for c in row]) + ' |'
        
        if len(processed_table) == 0:
            return
        
        self.ofile.write(gen_table_row(processed_table[0]) + '\n')
        self.ofile.write(gen_table_row(['---'] * len(processed_table[0])) + '\n')
        
        for row in processed_table[1:]:
            self.ofile.write(gen_table_row(row) + '\n')
        
        self.ofile.write('\n')

    def get_accent(self, text):
        return ' _' + text + '_ '

    def get_strong(self, text):
        return ' __' + text + '__ '

    def get_colored(self, text, rgb):
        # 检查是否是白色或接近白色
        r, g, b = rgb
        if r > 240 and g > 240 and b > 240:  # 接近白色的颜色
            return text  # 不添加颜色样式
        return f'<span style="color:rgb{rgb};">{text}</span>'

    def get_hyperlink(self, text, url):
        return '[' + text + '](' + url + ')'

    def esc_repl(self, match):
        return '\\' + match.group(0)

    def get_escaped(self, text):
        text = re.sub(self.esc_re1, self.esc_repl, text)
        text = re.sub(self.esc_re2, self.esc_repl, text)
        return text
