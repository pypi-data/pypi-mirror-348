import math
import os
import sys
import folium
import geopandas as gpd
import jenkspy
import numpy as np
import json
import openai

from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QColor, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout,
    QLineEdit, QWidget, QComboBox, QMessageBox, QGroupBox, QTabWidget,
    QSpinBox, QHBoxLayout, QTextEdit, QAction, QScrollArea, QSizePolicy, QDialog, QSplitter,
    QInputDialog, QRadioButton, QMenu
)

# ----------------------------
# 默认单变量色带
DEFAULT_RAMP_COLORS = {
    "Viridis": ["#440154", "#472D7B", "#395F86", "#278084", "#1F9E89", "#35B779", "#6CCE59", "#B6DE2B", "#FDE725"],
    "Plasma": ["#0D0887", "#5B02A3", "#9A179B", "#CD376A", "#D1605D", "#D98E4C", "#E2B357", "#F3E185", "#FDE725"],
    "Inferno": ["#000004", "#3B0C70", "#8C2981", "#DA4167", "#F1605D", "#FB8761", "#FBB06B", "#FAD96D", "#FEE588"],
    "Magma": ["#000004", "#1C1044", "#5B0C59", "#990C6D", "#D02659", "#F17145", "#FEBE2A", "#FDF705", "#FCF8FB"],
    "Cividis": ["#00204C", "#2C3E70", "#576D8C", "#7FA5A8", "#A5CFAD", "#C8F0AA", "#ECF8A1", "#FFF79E", "#FFF6B5"],
    "Ocean": ["#E8E6F2", "#B5D3E7", "#82C0DB", "#4FADD0"],
    "Rose": ["#E8E6F2", "#E5B4D9", "#E181BF", "#DE4FA6"]
}


# ----------------------------
# 工具函数
def get_expanded_colors(base_colors, target_count):
    if target_count <= len(base_colors):
        return base_colors[:target_count]
    else:
        expanded = []
        old_size = len(base_colors)
        for i in range(target_count):
            orig_idx = min(math.floor(i * old_size / target_count), old_size - 1)
            expanded.append(base_colors[orig_idx])
        return expanded


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '#' + ''.join(f'{c:02X}' for c in rgb)


def blend_colors(hex1, hex2):
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    blended = tuple((c1 + c2) // 2 for c1, c2 in zip(rgb1, rgb2))
    return rgb_to_hex(blended)



# ============ UI utility enhancements ============
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import QPropertyAnimation

def add_shadow(widget, blur=12, y_offset=3):
    """Add subtle shadow to any QWidget."""
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setXOffset(0)
    shadow.setYOffset(y_offset)
    shadow.setColor(QColor(111, 93, 171, 120))
    widget.setGraphicsEffect(shadow)

def flash_widget(widget):
    """Flash border red to indicate invalid input"""
    anim = QPropertyAnimation(widget, b"styleSheet", widget)
    anim.setDuration(300)
    anim.setLoopCount(2)
    anim.setStartValue("border: 2px solid #FF4D4F;")
    anim.setEndValue("border: 1px solid #c0c0c0;")
    anim.start(QPropertyAnimation.DeleteWhenStopped)



def create_color_icon(color, size=20):
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor(color))
    return pixmap


def create_bivariate_legend_html(breaks1, breaks2, color_matrix, var1_name="Variable 1", var2_name="Variable 2",
                                 legend_title="Bivariate Legend"):
    n_classes = len(breaks1) - 1
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 50px; left: 50px;
        z-index:9999;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 5px;
        border: 2px solid grey;
        font-size: 10px;
    ">
      <h4 style="margin:2px; padding:0; text-align:center;">{legend_title}</h4>
      <p style="margin:2px; padding:0; text-align:center;">{var1_name} vs. {var2_name}</p>
      <table style="border-collapse: collapse; margin:0 auto;">
        <tr>
          <td></td>"""
    for j in range(n_classes):
        legend_html += f"<th style='border:1px solid #999; padding:2px;'>{breaks2[j]:.2f} - {breaks2[j + 1]:.2f}</th>"
    legend_html += "</tr>"
    for i in range(n_classes):
        legend_html += f"<tr><th style='border:1px solid #999; padding:2px;'>{breaks1[i]:.2f} - {breaks1[i + 1]:.2f}</th>"
        for j in range(n_classes):
            color = color_matrix[i][j]
            legend_html += f"<td style='background:{color}; width:20px; height:20px; border:1px solid #999;'></td>"
        legend_html += "</tr>"
    legend_html += """
      </table>
    </div>
    """
    return legend_html


# ----------------------------
# 帮助文档对话框
class HelpDialog(QDialog):
    def __init__(self, language="en", parent=None):
        super().__init__(parent)
        title = "Help" if language.lower() == "en" else "帮助"
        self.setWindowTitle(title)
        self.resize(700, 600)
        self.setMinimumSize(800, 400)
        layout = QVBoxLayout(self)

        self.help_text = QTextEdit()
        self.help_text.setReadOnly(True)
        self.help_text.setText(self.get_help_text(language))
        layout.addWidget(self.help_text)

        btn_layout = QHBoxLayout()
        close_btn_text = "Close" if language.lower() == "en" else "关闭"
        close_button = QPushButton(close_btn_text)
        close_button.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(close_button)
        layout.addLayout(btn_layout)

    def get_help_text(self, language):
        if language.lower() == "en":
            help_doc = (
                "=== Help Documentation ===\n\n"
                "Overview:\n"
                "This interactive bivariate map tool allows you to import spatial data in GeoJSON format, select two variables "
                "for bivariate analysis, compute breakpoints using natural breaks (Jenks) or manual input, generate a bivariate "
                "color matrix, and create an interactive map with tooltips and an embedded legend. Additionally, it provides an LLM-assisted "
                "mode to guide you through operations with natural language instructions.\n\n"
                "Features:\n"
                "1. Data Import: Load GeoJSON files and automatically transform coordinate systems if necessary.\n"
                "2. Variable Selection: Choose two variables for visualization from the available fields.\n"
                "3. Breakpoint Calculation: Use Jenks natural breaks or manual input to classify data.\n"
                "4. Color Matrix Generation: Create a bivariate color matrix based on predefined or custom color ramps.\n"
                "5. Map Generation and Preview: Generate an interactive map with tooltips and a legend using Folium.\n"
                "6. LLM-assisted Mode: Enable a natural language interface for step-by-step guidance.\n"
                "7. Map Analysis: Analyze the generated map from different perspectives.\n\n"
                "Usage Instructions:\n"
                "- In the 'Data Selection' tab, load your GeoJSON file.\n"
                "- In the 'Settings' tab, choose variables, configure breakpoints, and set up the color matrix.\n"
                "- In the 'Map Generation' tab, preview and save your map.\n"
                "- To use the LLM-assisted mode, click the 'LLMs' button to enable it and follow the instructions.\n\n"
                "Copyright Zhe Wang , Zuo Zhang , Rui Zhang  and Yukun Jiang "
            )
        else:
            help_doc = (
                "=== 帮助文档 ===\n\n"
                "概述：\n"
                "本工具是一款交互式双变量地图可视化应用，支持导入 GeoJSON 格式的空间数据，选择两个变量进行双变量分析，"
                "通过自然断点（Jenks 算法）或手动输入方式计算分类断点，生成双变量配色矩阵，并利用 Folium 生成包含工具提示和图例的交互式地图。"
                "此外，还提供了 LLM 辅助模式，通过自然语言指导用户逐步完成各项操作。\n\n"
                "功能介绍：\n"
                "1. 数据导入：支持上传 GeoJSON 文件，并在必要时自动转换坐标系。\n"
                "2. 变量选择：从数据字段中选择用于可视化的两个变量。\n"
                "3. 断点计算：采用自然断点或手动输入方式对数据进行分类。\n"
                "4. 配色矩阵生成：基于预设或自定义的色带生成双变量配色矩阵。\n"
                "5. 地图生成与预览：使用 Folium 生成交互式地图，内嵌工具提示和图例。\n"
                "6. LLM 辅助模式：通过自然语言交互指导用户完成各项操作步骤。\n"
                "7. 地图分析：支持从不同视角对生成的地图进行分析。\n\n"
                "使用说明：\n"
                "- 在“数据选择”标签页中上传 GeoJSON 文件。\n"
                "- 在“设置”标签页中进行变量选择、断点配置及配色矩阵设置。\n"
                "- 在“地图生成”标签页中预览及保存地图。\n"
                "- 通过菜单中的“帮助”按钮查看本帮助文档；点击“LLMs”按钮开启自然语言操作指导模式。\n\n"
                "版权所有 王哲, 张祚、张瑞和江驭鲲"
            )
        return help_doc


# ----------------------------
# 地图预览窗口
class MapPreviewDialog(QDialog):
    def __init__(self, map_file, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Map Preview"))
        self.resize(700, 600)
        layout = QVBoxLayout(self)
        self.view = QWebEngineView(self)
        self.view.load(QUrl.fromLocalFile(os.path.abspath(map_file)))
        layout.addWidget(self.view)
        self.analysis_button = QPushButton(self.tr("Analyze Map"))
        add_shadow(self.analysis_button)
        self.analysis_button.clicked.connect(self.show_map_analysis)
        layout.addWidget(self.analysis_button)

    def show_map_analysis(self):
        if self.parent():
            self.parent().show_map_analysis()


# ----------------------------
# 地图分析窗口
class MapAnalysisDialog(QDialog):
    def __init__(self, gdf, map_file, parent=None):
        super().__init__(parent)
        self.gdf = gdf
        self.map_file = map_file
        self.parent_window = parent
        self.trans = parent.translations[parent.current_language]

        self.setWindowTitle(self.trans.get("map_analysis_title", "Map Analysis"))
        add_shadow(self, blur=24, y_offset=4)
        self.resize(850, 750)
        self.setStyleSheet("""QDialog { background-color: #F3F4F6; border-radius: 12px; }
QGroupBox { font-weight: 600; border: 1px solid #E5E7EB; border-radius: 8px; margin-top: 16px; background-color: #FFFFFF; padding-top: 6px; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 6px; font-size: 15px; }
QLabel { font-size: 15px; color: #111827; }
QLineEdit, QTextEdit { font-size: 14px; padding: 6px 8px; border: 1px solid #D1D5DB; border-radius: 6px; background-color: #FFFFFF; }
QLineEdit:focus, QTextEdit:focus { border: 1px solid #6F5DAB; }
QRadioButton { font-size: 14px; padding: 4px 2px; }
QPushButton { background-color: #6F5DAB; color: #FFFFFF; border: none; padding: 8px 18px; font-size: 14px; border-radius: 6px; }
QPushButton:hover { background-color: #5E4F91; }
QPushButton:disabled { background-color: #E5E7EB; color: #9CA3AF; }""")

        layout = QVBoxLayout(self)
        self.style_group = QGroupBox(self.trans.get("analysis_style", "Analysis Style"))
        style_layout = QHBoxLayout()
        self.radio_geographer = QRadioButton(self.trans.get("Geographer", "Geographer"))
        self.radio_cultural = QRadioButton(self.trans.get("Cultural Historian", "Cultural Historian"))
        self.radio_comprehensive = QRadioButton(
            self.trans.get("Comprehensive Perspective", "Comprehensive Perspective"))
        self.radio_comprehensive.setChecked(True)
        style_layout.addWidget(self.radio_geographer)
        style_layout.addWidget(self.radio_cultural)
        style_layout.addWidget(self.radio_comprehensive)
        self.style_group.setLayout(style_layout)
        layout.addWidget(self.style_group)

        self.analysis_display = QTextEdit()
        self.analysis_display.setReadOnly(True)
        layout.addWidget(self.analysis_display)

        input_layout = QHBoxLayout()
        self.analysis_input = QLineEdit()
        self.analysis_input.setPlaceholderText(
            self.trans.get("analysis_question_placeholder", "Enter your analysis question..."))
        self.analysis_submit = QPushButton(self.trans.get("analysis_submit", "Submit"))
        self.analysis_submit.clicked.connect(self.process_analysis)
        input_layout.addWidget(self.analysis_input)
        input_layout.addWidget(self.analysis_submit)
        layout.addLayout(input_layout)

        self.analysis_display.append(
            self.trans.get("analysis_ready_text", "System is ready for analysis. Please enter your question."))

    def generate_metadata_summary(self):
        num_features = len(self.gdf)
        fields = list(self.gdf.columns)
        non_geom_fields = [field for field in fields if field != "geometry"]
        try:
            attributes_summary = self.gdf[non_geom_fields].describe(include="all").to_string()
        except Exception as e:
            attributes_summary = f"Failed to compute attribute summary: {e}"
        try:
            bounds = self.gdf.total_bounds
            extent = f"X: {bounds[0]:.2f} ~ {bounds[2]:.2f}, Y: {bounds[1]:.2f} ~ {bounds[3]:.2f}"
        except Exception:
            extent = self.trans.get("Unknown", "Unknown")
        try:
            geom_types = self.gdf.geom_type.unique()
            geom_types_str = ", ".join(geom_types)
        except Exception:
            geom_types_str = self.trans.get("Unknown", "Unknown")
        try:
            centroid = self.gdf.unary_union.centroid
            centroid_str = f"({centroid.y:.2f}, {centroid.x:.2f})"
        except Exception:
            centroid_str = self.trans.get("Unknown", "Unknown")
        summary = (
            f"Feature count: {num_features}\n"
            f"Fields (excluding geometry): {', '.join(non_geom_fields)}\n\n"
            f"Attribute Summary:\n{attributes_summary}\n\n"
            f"Geographic extent: {extent}\n"
            f"Geometry types: {geom_types_str}\n"
            f"Centroid: {centroid_str}"
        )
        return summary

    def process_analysis(self):
        user_query = self.analysis_input.text().strip()
        if not user_query:
            QMessageBox.warning(self, self.trans.get("analysis_warning", "Warning"),
                                self.trans.get("analysis_no_question", "Please enter your analysis question."))
            return

        if self.radio_geographer.isChecked():
            style_prompt = self.trans.get("analysis_geographer_prompt",
                                          "Analyze the map from a geographer's perspective, focusing on spatial distribution, natural environment, and regional patterns.")
        elif self.radio_cultural.isChecked():
            style_prompt = self.trans.get("analysis_cultural_prompt",
                                          "Analyze the map from a cultural historian's perspective, emphasizing cultural heritage, historical context, and social influences.")
        else:
            style_prompt = self.trans.get("analysis_comprehensive_prompt",
                                          "Provide a comprehensive analysis combining data, spatial distribution, and cultural-historical insights.")

        metadata = self.generate_metadata_summary()
        depth_hint = self.trans.get("analysis_depth_hint",
                                    "Note: This is a bivariate cartogram. Please consider the interplay of the two variables, classification breaks, and color schemes in your analysis.")
        analysis_detail_req = self.trans.get("analysis_detail_request",
                                             "Please provide a detailed and comprehensive analysis.")
        prompt = (
            f"【Metadata】\n{metadata}\n\n"
            f"【Background】\n{depth_hint}\n\n"
            f"【Style Prompt】\n{style_prompt}\n\n"
            f"【User Question】\n{user_query}\n\n"
            f"{analysis_detail_req}"
        )
        self.analysis_display.append(self.trans.get("analysis_user", "User: ") + user_query)
        self.analysis_display.append(self.trans.get("analysis_waiting", "Analyzing, please wait..."))

        try:
            openai.api_key = self.parent_window.llm_api_key_input.text().strip()
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            analysis_result = response.choices[0].message.content.strip()
            self.analysis_display.append(self.trans.get("analysis_result", "Analysis Result: ") + analysis_result)
        except Exception as e:
            self.analysis_display.append(self.trans.get("analysis_failed", "Failed to get analysis: ") + str(e))
        self.analysis_input.clear()


# ----------------------------
# 主界面类
from PyQt5.QtWidgets import QScrollArea
def _wrap_in_scroll(widget):
    scroll = QScrollArea()
    scroll.setWidget(widget)
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QScrollArea.NoFrame)
    return scroll


class BivariateMapApp(QMainWindow):
    state_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.current_language = "en"
        self.use_llm_mode = False
        self.llm_state = None
        self.selected_vars = {}
        self.selected_color_scheme1 = ""
        self.selected_color_scheme2 = ""
        self.selected_tooltip = {}
        self.shared_state = {
            "file_loaded": False,
            "fields": [],
            "var1": None,
            "var2": None,
            "breaks1": None,
            "breaks2": None,
            "color_scheme1": None,
            "color_scheme2": None,
            "tooltip": None
        }
        self.translations = {
            'en': {
                'window_title': 'VisGeo-LMS',
                'map_analysis_title': 'Map Analysis',
                'tab_data_selection': 'Data Selection',
                'tab_settings': 'Parameter settings',
                'tab_map_generation': 'Map Generation',
                'tab_llm': 'LLM Dialogue',
                'choose_geojson_file': 'Select GeoJSON File',
                'no_file_selected': 'No file selected',
                'variable_selection_group': 'Variable Selection',
                'select_variable_1': 'Select Variable 1:',
                'select_variable_2': 'Select Variable 2:',
                'break_settings_group': 'Break Settings',
                'select_break_method': 'Select Break Method:',
                'manual_input': 'Manual Input',
                'natural_breaks': 'Natural Breaks',
                'calculate_natural_breaks': 'Calculate Natural Breaks',
                'select_number_of_classes': 'Select Number of Classes (2-10):',
                'variable1_breaks': 'Variable 1 Breaks (comma-separated):',
                'variable2_breaks': 'Variable 2 Breaks (comma-separated):',
                'color_matrix_settings_group': 'Color Matrix Settings',
                'variable1_color_ramp': 'Variable 1 Color Ramp:',
                'variable2_color_ramp': 'Variable 2 Color Ramp:',
                'enter_custom_colors_var1': 'Enter custom colors for Variable 1 (comma-separated)',
                'enter_custom_colors_var2': 'Enter custom colors for Variable 2 (comma-separated)',
                'preview_color_matrix': 'Preview Color Matrix',
                'color_matrix_input_label': 'Color Matrix Input (each row corresponds to a category of Variable 1):',
                'color_matrix_preview_label': 'Color Matrix Preview:',
                'tooltip_settings_group': 'Interactive Tooltip Settings',
                'tooltip_instructions': 'Select fields to display and customize labels (up to 3):',
                'field_label': 'Field {num}:',
                'label_label': 'Label:',
                'generate_map': 'Generate Map',
                'save_map': 'Save Map',
                'file_read_error': 'Failed to read file',
                'insufficient_columns': 'Data must have at least two columns!',
                'break_calculation_failed': 'Break calculation failed: {error}',
                'breaks_calculated': 'Natural breaks calculated and filled!',
                'legend_title': 'Bivariate Legend',
                'llm_api_key': 'Enter your OpenAI API key:',
                'llm_mode_on': 'LLM Panel Shown',
                'llm_mode_off': 'LLM Panel Hidden',
                'upload_code_prompt': 'Uploading tool code to LLM...',
                'llm_empty_warning': 'Please enter a command',
                'llm_conversation_error': 'LLM call failed: {error}',
                'llm_command_executed': 'Command executed: {action}',
                'tool_intro': 'This tool generates bivariate maps using GeoJSON data. Step-by-step process:\n'
                              "1. Upload a GeoJSON file.\n"
                              "2. List the fields in the file.\n"
                              "3. Specify two variables for visualization.\n"
                              "4. Choose the break method (natural breaks or manual) and confirm breaks.\n"
                              "5. Choose default color schemes for both variables.\n"
                              "6. Set up to three tooltip fields and labels.\n"
                              "7. Preview and, if desired, save the map.\n",
                'upload_geojson': 'Upload GeoJSON File',
                'confirmation_title': 'Confirmation',
                'natural_breaks_confirm': 'The current number of classes is {0}. Do you want to use this value to calculate natural breaks?',
                'analyze_map': 'Analyze Map',
                'enter_api_key_prompt': 'Please enter a valid OpenAI API key:',
                'llm_api_not_ready': 'Please enable LLM mode and enter a valid API key before analyzing the map.',
                "analysis_style": "Analysis Style",
                "Geographer": "Geographer",
                "Cultural Historian": "Cultural Historian",
                "Comprehensive Perspective": "Comprehensive Perspective",
                "analysis_question_placeholder": "Enter your analysis question...",
                "analysis_submit": "Submit",
                "analysis_ready_text": "System is ready for analysis. Please enter your question.",
                "analysis_warning": "Warning",
                "analysis_no_question": "Please enter your analysis question.",
                "analysis_geographer_prompt": "Analyze the map from a geographer's perspective, focusing on spatial distribution, natural environment, and regional patterns.",
                "analysis_cultural_prompt": "Analyze the map from a cultural historian's perspective, emphasizing cultural heritage, historical context, and social influences.",
                "analysis_comprehensive_prompt": "Provide a comprehensive analysis combining data, spatial distribution, and cultural-historical insights.",
                "analysis_depth_hint": "Note: This is a bivariate cartogram. Please consider the interplay of the two variables, classification breaks, and color schemes.",
                "analysis_detail_request": "Please provide a detailed and comprehensive analysis.",
                "analysis_user": "User: ",
                "analysis_waiting": "Analyzing, please wait...",
                "analysis_result": "Analysis Result: ",
                "analysis_failed": "Failed to get analysis: "
            },
            'zh': {
                'window_title': 'VisGeo-LMS',
                'map_analysis_title': '地图分析',
                'tab_data_selection': '数据选择',
                'tab_settings': '参数设置',
                'tab_map_generation': '地图生成',
                'tab_llm': '对话式指导',
                'choose_geojson_file': '选择 GeoJSON 文件',
                'no_file_selected': '未选择文件',
                'variable_selection_group': '变量选择',
                'select_variable_1': '选择变量 1：',
                'select_variable_2': '选择变量 2：',
                'break_settings_group': '断点设置',
                'select_break_method': '选择断点方式：',
                'manual_input': '手动输入',
                'natural_breaks': '自然间断点法',
                'calculate_natural_breaks': '计算自然断点',
                'select_number_of_classes': '选择类别数量（2-10）：',
                'variable1_breaks': '变量 1 断点（逗号分隔）：',
                'variable2_breaks': '变量 2 断点（逗号分隔）：',
                'color_matrix_settings_group': '配色矩阵设置',
                'variable1_color_ramp': '变量1 色带选择：',
                'variable2_color_ramp': '变量2 色带选择：',
                'enter_custom_colors_var1': '请输入变量1的自定义颜色（逗号分隔）',
                'enter_custom_colors_var2': '请输入变量2的自定义颜色（逗号分隔）',
                'preview_color_matrix': '预览配色矩阵',
                'color_matrix_input_label': '配色矩阵输入（每行对应变量 1 的类别）：',
                'color_matrix_preview_label': '配色矩阵预览：',
                'tooltip_settings_group': '交互式提示标签设置',
                'tooltip_instructions': '选择要展示的字段并自定义标签（最多3个）：',
                'field_label': '字段{num}：',
                'label_label': '标签：',
                'generate_map': '生成地图',
                'save_map': '保存地图',
                'file_read_error': '无法读取文件',
                'insufficient_columns': '数据中至少需要两个列！',
                'break_calculation_failed': '断点计算失败：{error}',
                'breaks_calculated': '自然断点已计算并填充！',
                'legend_title': '双变量图例',
                'llm_api_key': '请输入你的 OpenAI API 密钥：',
                'llm_mode_on': '已显示对话面板',
                'llm_mode_off': '已隐藏对话面板',
                'upload_code_prompt': '正在向大语言模型上传工具代码...',
                'llm_empty_warning': '请输入指令',
                'llm_conversation_error': '调用大语言模型失败：{error}',
                'llm_command_executed': '指令已执行: {action}',
                'tool_intro': '本工具用于基于 GeoJSON 数据生成双变量地图。使用流程：\n'
                              "1. 上传 GeoJSON 文件；\n"
                              "2. 识别文件中的字段；\n"
                              "3. 选择用于可视化的两个变量；\n"
                              "4. 选择断点方式（自然或手动）并确认断点；\n"
                              "5. 为两个变量选择默认配色方案；\n"
                              "6. 设定图例显示的字段及对应标签；\n"
                              "7. 预览并保存地图。\n",
                'upload_geojson': '上传 GeoJSON 文件',
                'confirmation_title': '确认',
                'natural_breaks_confirm': '当前类别数为{0}。是否使用该值计算自然断点？',
                'analyze_map': '分析地图',
                'enter_api_key_prompt': '请先输入有效的 OpenAI API 密钥：',
                'llm_api_not_ready': '请先启用LLM模式并输入有效的 API 密钥，再进行地图分析',
                "analysis_style": "分析风格",
                "Geographer": "地理学家视角",
                "Cultural Historian": "人文历史学家视角",
                "Comprehensive Perspective": "综合视角",
                "analysis_question_placeholder": "请输入您的分析问题...",
                "analysis_submit": "提交",
                "analysis_ready_text": "系统已就绪，请输入您的分析问题。",
                "analysis_warning": "警告",
                "analysis_no_question": "请输入您的分析问题。",
                "analysis_geographer_prompt": "请从地理学家视角分析该地图，侧重于空间分布、自然环境及区域模式。",
                "analysis_cultural_prompt": "请从人文历史学家视角分析该地图，关注区域文化传承、历史背景和社会影响。",
                "analysis_comprehensive_prompt": "请提供一份综合性的分析，结合数据、空间分布及文化历史视角。",
                "analysis_depth_hint": "提示：这是一幅双变量变形地图，请综合考虑变量之间的相互作用、断点划分和配色设计。",
                "analysis_detail_request": "请提供详细而全面的分析。",
                "analysis_user": "用户：",
                "analysis_waiting": "正在分析，请稍候……",
                "analysis_result": "分析结果：",
                "analysis_failed": "分析失败："
            }
        }
        self.setWindowTitle(self.translations[self.current_language]['window_title'])
        # 默认状态仅显示传统模式，故不预留 LLM 空间
        self.resize(1000, 900)  # 允许调整大小
        icon_path = os.path.join(r"D:\Jupyter\遗产灾害", "icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        # 菜单：语言、LLM切换及帮助按钮
        menubar = self.menuBar()
        language_menu = QMenu("English", self)
        english_action = QAction("English", self)
        english_action.triggered.connect(lambda: self.change_language("en"))
        language_menu.addAction(english_action)
        chinese_action = QAction("Chinese", self)
        chinese_action.triggered.connect(lambda: self.change_language("zh"))
        language_menu.addAction(chinese_action)
        menubar.addMenu(language_menu)
        self.llm_toggle_action = QAction("LLMs", self)
        self.llm_toggle_action.setCheckable(True)
        self.llm_toggle_action.triggered.connect(self.toggle_llm_panel)
        menubar.addAction(self.llm_toggle_action)
        help_action = QAction("Help" if self.current_language.lower() == "en" else "帮助", self)
        help_action.triggered.connect(self.show_help_dialog)
        menubar.addAction(help_action)

        self.file_path = None
        self.gdf = None
        self.map_html = "InterCartoMap.html"
        # 传统模式界面（所有标签页）
        self.traditional_tabs = QTabWidget()
        self.traditional_tabs.addTab(_wrap_in_scroll(self.create_data_selection_tab()),
                                     self.translations[self.current_language]['tab_data_selection'])
        self.traditional_tabs.addTab(_wrap_in_scroll(self.create_settings_tab()),
                                     self.translations[self.current_language]['tab_settings'])
        self.traditional_tabs.addTab(_wrap_in_scroll(self.create_map_generation_tab()),
                                     self.translations[self.current_language]['tab_map_generation'])
        # 默认状态下将传统模式设置为中央控件
        self.setCentralWidget(self.traditional_tabs)
        # LLM 模块，在需要时再创建
        self.llm_panel = self.create_llm_tab()
        self.state_changed.connect(lambda state: self.update_field_options(state.get("fields", [])))
        self.update_ui_text()
        self.setStyleSheet(self.get_stylesheet())

    # 当用户开启 LLM 模式时，构造 QSplitter，将传统模式和 LLM 模块并排显示；
    # 关闭时，则切换回单独显示传统模式（不预留空白）
    def toggle_llm_panel(self):
        if not self.use_llm_mode:
            # 创建一个新的 QSplitter，将传统模式和 LLM 模块添加进去
            splitter = QSplitter(Qt.Horizontal)
            splitter.addWidget(self.traditional_tabs)
            # 为 LLM 模块设置一个最小宽度，比如200像素
            self.llm_panel.setMinimumWidth(200)
            splitter.addWidget(self.llm_panel)
            # 将新的 splitter 设置为中央控件
            self.setCentralWidget(splitter)
            self.use_llm_mode = True
            self.llm_toggle_action.setText("Hide LLMs")
            if self.llm_api_key_input.text().strip():
                self.llm_display.append(self.translations[self.current_language]['upload_code_prompt'])
                self.upload_code_to_llm()
            else:
                self.llm_display.append("No API key provided. Skipping code upload.")
        else:
            # 关闭 LLM 模式，直接将传统模式设置为中央控件
            self.setCentralWidget(self.traditional_tabs)
            self.use_llm_mode = False
            self.llm_toggle_action.setText("LLMs")

    def show_help_dialog(self):
        help_dialog = HelpDialog(language=self.current_language, parent=self)
        help_dialog.exec_()

    # ----------------------------
    # 以下各方法均保持和之前类似，实现数据选择、设置、地图生成及 LLM 对话等功能
    def advance_llm_state(self, new_state, data=None):
        self.llm_state = new_state
        if self.current_language.lower() == "en":
            next_step_prompts = {
                "fields_listed": f"[Tip] File uploaded. Available fields: {', '.join(data) if isinstance(data, list) else data}. Next step: Please specify the two variables for visualization, e.g. 'Material cultural heritage, Intangible cultural heritage'.",
                "variables_selected": "[Tip] Next step: Please specify the break method, choose either 'natural breaks' or 'manual'.",
                "manual_break": "[Tip] Next step: Please enter manual break points, numbers separated by commas, e.g. '10,20,30,40'.",
                "breaks_set": "[Tip] Next step: Please choose default color schemes for both variables.",
                "color_set": "[Tip] Next step: Please enter tooltip fields and corresponding labels, e.g. 'field1, field2, field3; label1, label2, label3'.",
                "tooltip_set": "[Tip] Next step: Please specify whether to preview the map, enter 'yes' or 'no'.",
                "preview": "[Tip] Next step: If you are satisfied with the preview, please enter a command to save the map.",
                "final": "[Tip] Process finished.",
                "natural_break_classes": "[Tip] Next step: Please enter the number of classes (2-10) for natural break calculation."
            }
        else:
            next_step_prompts = {
                "fields_listed": f"【提示】文件已上传。可用字段：{', '.join(data) if isinstance(data, list) else data}。请选择用于可视化的两个变量。",
                "variables_selected": "【提示】下一步：请输入断点生成方式，取值为 natural breaks（自然间断点法）或 manual（手动断点）。",
                "manual_break": "【提示】下一步：请输入手动断点，数字以逗号分隔，例如：10,20,30,40。",
                "breaks_set": "【提示】下一步：请选择两个变量的默认配色方案，格式为：color1, color2。可选方案有：" + ", ".join(
                    list(DEFAULT_RAMP_COLORS.keys())),
                "color_set": "【提示】下一步：请输入图例提示字段及对应标签，例如：field1, field2, field3; label1, label2, label3。",
                "tooltip_set": "【提示】下一步：请输入是否预览地图，输入 yes 或 no。",
                "preview": "【提示】下一步：如果预览满意，请输入保存地图的命令。",
                "final": "【提示】流程结束。",
                "natural_break_classes": "【提示】下一步：请输入自然断点计算的类别数（2-10）："
            }
        tip = next_step_prompts.get(new_state, "")
        if new_state == "variables_selected" and data is not None:
            tip = f"{tip} (Variables updated: {data})"
        if self.use_llm_mode and tip:
            self.llm_display.append("LLM: " + tip)

    def update_field_options(self, new_fields):
        current_var1 = self.var1_combo.currentText()
        current_var2 = self.var2_combo.currentText()
        current_fields = []
        model = self.var1_combo.model()
        if model:
            for row in range(model.rowCount()):
                item = model.item(row)
                current_fields.append(item.text())
        if current_fields == new_fields:
            return
        self.var1_combo.blockSignals(True)
        self.var2_combo.blockSignals(True)
        for combo, _ in self.tooltip_selectors:
            combo.blockSignals(True)
        self.var1_combo.clear()
        self.var2_combo.clear()
        self.var1_combo.addItems(new_fields)
        self.var2_combo.addItems(new_fields)
        for combo, _ in self.tooltip_selectors:
            combo.clear()
            combo.addItem("")
            combo.addItems(new_fields)
        if current_var1 in new_fields:
            self.var1_combo.setCurrentText(current_var1)
        if current_var2 in new_fields:
            self.var2_combo.setCurrentText(current_var2)
        self.var1_combo.blockSignals(False)
        self.var2_combo.blockSignals(False)
        for combo, _ in self.tooltip_selectors:
            combo.blockSignals(False)

    def update_traditional_ui_from_shared_state(self):
        if self.shared_state.get("var1"):
            self.var1_combo.setCurrentText(self.shared_state["var1"])
        if self.shared_state.get("var2"):
            self.var2_combo.setCurrentText(self.shared_state["var2"])
        if self.shared_state.get("breaks1"):
            self.break_input_1.setText(",".join(map(str, self.shared_state["breaks1"])))
        if self.shared_state.get("breaks2"):
            self.break_input_2.setText(",".join(map(str, self.shared_state["breaks2"])))
        if self.shared_state.get("color_scheme1"):
            self.ramp1_combo.setCurrentText(self.shared_state["color_scheme1"])
        if self.shared_state.get("color_scheme2"):
            self.ramp2_combo.setCurrentText(self.shared_state["color_scheme2"])
        if self.shared_state.get("tooltip"):
            tooltip = self.shared_state["tooltip"]
            fields = tooltip.get("fields", [])
            labels = tooltip.get("labels", [])
            for i, (combo, line_edit) in enumerate(self.tooltip_selectors):
                if i < len(fields):
                    combo.setCurrentText(fields[i])
                if i < len(labels):
                    line_edit.setText(labels[i])

    def on_variable_changed(self):
        self.shared_state["var1"] = self.var1_combo.currentText()
        self.shared_state["var2"] = self.var2_combo.currentText()
        self.state_changed.emit(self.shared_state)
        self.advance_llm_state("variables_selected",
                               {"var1": self.shared_state["var1"], "var2": self.shared_state["var2"]})

    def toggle_break_method(self):
        current_method = self.break_method_combo.currentText()
        if current_method == self.translations[self.current_language]['natural_breaks']:
            self.break_input_1.setEnabled(False)
            self.break_input_2.setEnabled(False)
            self.calculate_button.setEnabled(True)
        else:
            self.break_input_1.setEnabled(True)
            self.break_input_2.setEnabled(True)
            self.calculate_button.setEnabled(False)

    def create_data_selection_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.file_group = QGroupBox()
        file_layout = QVBoxLayout()
        self.file_label = QLabel(self.translations[self.current_language]['no_file_selected'])
        self.file_button = QPushButton(self.translations[self.current_language]['choose_geojson_file'])
        add_shadow(self.file_button)
        self.file_button.clicked.connect(self.load_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_button)
        self.file_group.setLayout(file_layout)
        self.file_group.setMaximumHeight(100)
        self.var_group = QGroupBox(self.translations[self.current_language]['variable_selection_group'])
        var_layout = QVBoxLayout()
        self.var1_label = QLabel(self.translations[self.current_language]['select_variable_1'])
        self.var1_combo = QComboBox()
        self.var1_combo.currentTextChanged.connect(self.on_variable_changed)
        self.var2_label = QLabel(self.translations[self.current_language]['select_variable_2'])
        self.var2_combo = QComboBox()
        self.var2_combo.currentTextChanged.connect(self.on_variable_changed)
        var_layout.addWidget(self.var1_label)
        var_layout.addWidget(self.var1_combo)
        var_layout.addWidget(self.var2_label)
        var_layout.addWidget(self.var2_combo)
        self.var_group.setLayout(var_layout)
        self.var_group.setMaximumHeight(150)
        layout.addWidget(self.file_group)
        layout.addWidget(self.var_group)
        tab.setLayout(layout)
        return tab

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.break_group = QGroupBox(self.translations[self.current_language]['break_settings_group'])
        break_layout = QVBoxLayout()
        self.break_method_label = QLabel(self.translations[self.current_language]['select_break_method'])
        self.break_method_combo = QComboBox()
        self.break_method_combo.addItems([self.translations[self.current_language]['manual_input'],
                                          self.translations[self.current_language]['natural_breaks']])
        self.break_method_combo.currentIndexChanged.connect(self.toggle_break_method)
        self.calculate_button = QPushButton(self.translations[self.current_language]['calculate_natural_breaks'])
        add_shadow(self.calculate_button)
        self.calculate_button.clicked.connect(self.calculate_breaks)
        self.calculate_button.setEnabled(False)
        hlayout_count = QHBoxLayout()
        self.count_label = QLabel(self.translations[self.current_language]['select_number_of_classes'])
        self.break_count_spin = QSpinBox()
        self.break_count_spin.setRange(2, 10)
        self.break_count_spin.setValue(4)
        self.break_count_spin.valueChanged.connect(self.update_color_matrix_size)
        hlayout_count.addWidget(self.count_label)
        hlayout_count.addWidget(self.break_count_spin)
        self.break_input1_label = QLabel(self.translations[self.current_language]['variable1_breaks'])
        self.break_input_1 = QLineEdit()
        self.break_input2_label = QLabel(self.translations[self.current_language]['variable2_breaks'])
        self.break_input_2 = QLineEdit()
        break_layout.addWidget(self.break_method_label)
        break_layout.addWidget(self.break_method_combo)
        break_layout.addLayout(hlayout_count)
        break_layout.addWidget(self.calculate_button)
        break_layout.addWidget(self.break_input1_label)
        break_layout.addWidget(self.break_input_1)
        break_layout.addWidget(self.break_input2_label)
        break_layout.addWidget(self.break_input_2)
        self.break_group.setLayout(break_layout)
        layout.addWidget(self.break_group)
        self.color_group = QGroupBox(self.translations[self.current_language]['color_matrix_settings_group'])
        color_layout = QVBoxLayout()
        hlayout_ramp = QHBoxLayout()
        self.ramp1_label = QLabel(self.translations[self.current_language]['variable1_color_ramp'])
        self.ramp1_combo = QComboBox()
        model1 = QStandardItemModel()
        for ramp_name, colors in DEFAULT_RAMP_COLORS.items():
            item = QStandardItem(ramp_name)
            item.setIcon(QIcon(create_color_icon(colors[0])))
            model1.appendRow(item)
        custom_item = QStandardItem("Custom" if self.current_language.lower() == "en" else "自定义")
        model1.appendRow(custom_item)
        self.ramp1_combo.setModel(model1)
        self.ramp1_combo.currentTextChanged.connect(lambda text: self.toggle_custom_input(text, 1))
        hlayout_ramp.addWidget(self.ramp1_label)
        hlayout_ramp.addWidget(self.ramp1_combo)
        self.custom_ramp1_input = QLineEdit()
        self.custom_ramp1_input.setVisible(False)
        hlayout_ramp.addWidget(self.custom_ramp1_input)
        self.ramp2_label = QLabel(self.translations[self.current_language]['variable2_color_ramp'])
        self.ramp2_combo = QComboBox()
        model2 = QStandardItemModel()
        for ramp_name, colors in DEFAULT_RAMP_COLORS.items():
            item = QStandardItem(ramp_name)
            item.setIcon(QIcon(create_color_icon(colors[0])))
            model2.appendRow(item)
        custom_item2 = QStandardItem("Custom" if self.current_language.lower() == "en" else "自定义")
        model2.appendRow(custom_item2)
        self.ramp2_combo.setModel(model2)
        self.ramp2_combo.currentTextChanged.connect(lambda text: self.toggle_custom_input(text, 2))
        hlayout_ramp.addWidget(self.ramp2_label)
        hlayout_ramp.addWidget(self.ramp2_combo)
        self.custom_ramp2_input = QLineEdit()
        self.custom_ramp2_input.setVisible(False)
        hlayout_ramp.addWidget(self.custom_ramp2_input)
        color_layout.addLayout(hlayout_ramp)
        self.preview_button = QPushButton(self.translations[self.current_language]['preview_color_matrix'])
        add_shadow(self.preview_button)
        self.preview_button.clicked.connect(self.generate_color_matrix)
        color_layout.addWidget(self.preview_button)
        self.color_matrix_input_label = QLabel(self.translations[self.current_language]['color_matrix_input_label'])
        self.color_matrix_input = QTextEdit()
        color_layout.addWidget(self.color_matrix_input_label)
        color_layout.addWidget(self.color_matrix_input)
        self.color_matrix_preview_label = QLabel(self.translations[self.current_language]['color_matrix_preview_label'])
        color_layout.addWidget(self.color_matrix_preview_label)
        self.color_preview = QLabel()
        self.color_preview.setTextFormat(Qt.RichText)
        self.color_preview.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.color_preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.preview_scroll = QScrollArea()
        self.preview_scroll.setWidgetResizable(True)
        self.preview_scroll.setWidget(self.color_preview)
        color_layout.addWidget(self.preview_scroll)
        self.color_group.setLayout(color_layout)
        layout.addWidget(self.color_group)
        self.tooltip_group = QGroupBox(self.translations[self.current_language]['tooltip_settings_group'])
        tooltip_layout = QVBoxLayout()
        self.tooltip_instructions = QLabel(self.translations[self.current_language]['tooltip_instructions'])
        tooltip_layout.addWidget(self.tooltip_instructions)
        self.tooltip_selectors = []
        self.tooltip_field_labels = []
        self.tooltip_label_labels = []
        for i in range(3):
            hlayout = QHBoxLayout()
            field_label = QLabel(self.translations[self.current_language]['field_label'].format(num=i + 1))
            combo = QComboBox()
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("")
            hlayout.addWidget(field_label)
            hlayout.addWidget(combo)
            label_label = QLabel(self.translations[self.current_language]['label_label'])
            hlayout.addWidget(label_label)
            hlayout.addWidget(line_edit)
            tooltip_layout.addLayout(hlayout)
            self.tooltip_selectors.append((combo, line_edit))
            self.tooltip_field_labels.append(field_label)
            self.tooltip_label_labels.append(label_label)
        self.tooltip_group.setLayout(tooltip_layout)
        layout.addWidget(self.tooltip_group)
        for combo, edit in self.tooltip_selectors:
            combo.currentIndexChanged.connect(self.update_tooltip_state)
            edit.textChanged.connect(self.update_tooltip_state)
        tab.setLayout(layout)
        return tab

    def create_map_generation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.generate_button = QPushButton(self.translations[self.current_language]['generate_map'])
        add_shadow(self.generate_button)
        self.generate_button.clicked.connect(self.generate_map)
        self.save_button = QPushButton(self.translations[self.current_language]['save_map'])
        add_shadow(self.save_button)
        self.save_button.clicked.connect(self.save_map)
        self.save_button.setEnabled(False)
        self.map_preview = QWebEngineView()
        layout.addWidget(self.generate_button)
        layout.addWidget(self.map_preview)
        layout.addWidget(self.save_button)
        self.analyze_map_button = QPushButton(self.translations[self.current_language]['analyze_map'])
        add_shadow(self.analyze_map_button)
        self.analyze_map_button.clicked.connect(self.show_map_analysis)
        layout.addWidget(self.analyze_map_button)
        tab.setLayout(layout)
        return tab

    def show_map_analysis(self):
        api_key = self.llm_api_key_input.text().strip()
        if not api_key:
            from PyQt5.QtWidgets import QInputDialog
            default_prompt = "请先输入有效的 OpenAI API 密钥："
            prompt_text = self.translations[self.current_language].get('enter_api_key_prompt', default_prompt)
            api_key_input, ok = QInputDialog.getText(
                self,
                self.translations[self.current_language]['llm_api_key'],
                prompt_text
            )
            if ok and api_key_input.strip():
                self.llm_api_key_input.setText(api_key_input.strip())
            else:
                QMessageBox.information(
                    self,
                    self.translations[self.current_language]['window_title'],
                    self.translations[self.current_language].get('llm_api_not_ready',
                                                                 "请先启用LLM模式并输入有效的 API 密钥，再进行地图分析")
                )
                return
        analysis_dialog = MapAnalysisDialog(self.gdf, self.map_html, self)
        analysis_dialog.show()

    def create_llm_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.llm_api_key_label = QLabel(self.translations[self.current_language]['llm_api_key'])
        self.llm_api_key_input = QLineEdit()
        self.llm_api_key_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.llm_api_key_label)
        layout.addWidget(self.llm_api_key_input)
        self.llm_upload_button = QPushButton(self.translations[self.current_language]['upload_geojson'])
        add_shadow(self.llm_upload_button)
        self.llm_upload_button.clicked.connect(self.llm_upload_file)
        layout.addWidget(self.llm_upload_button)
        self.tool_instructions_display = QTextEdit()
        self.tool_instructions_display.setReadOnly(True)
        self.tool_instructions_display.setPlainText(self.translations[self.current_language]['tool_intro'])
        layout.addWidget(self.tool_instructions_display)
        self.llm_display = QTextEdit()
        self.llm_display.setReadOnly(True)
        layout.addWidget(self.llm_display)
        h_layout = QHBoxLayout()
        self.llm_input = QLineEdit()
        self.llm_input.setPlaceholderText("Enter your command or question...")
        self.llm_submit = QPushButton("Submit")
        add_shadow(self.llm_submit)
        self.llm_submit.clicked.connect(self.process_llm_conversation)
        h_layout.addWidget(self.llm_input)
        h_layout.addWidget(self.llm_submit)
        layout.addLayout(h_layout)
        tab.setLayout(layout)
        return tab

    def update_tooltip_state(self):
        tooltip_fields = []
        tooltip_labels = []
        for combo, edit in self.tooltip_selectors:
            field = combo.currentText()
            if field:
                tooltip_fields.append(field)
                label = edit.text().strip()
                if not label:
                    label = field
                tooltip_labels.append(label)
        if len(tooltip_fields) != 3:
            return
        tooltip_settings = {"fields": tooltip_fields, "labels": tooltip_labels}
        self.shared_state["tooltip"] = tooltip_settings
        self.state_changed.emit(self.shared_state)
        if self.use_llm_mode:
            self.advance_llm_state("tooltip_set", tooltip_settings)

    # 改进后的 toggle_llm_panel：默认状态下仅显示传统模式，当用户开启时动态构造 QSplitter 将传统模式和 LLM 模块并排显示
    def toggle_llm_panel(self):
        if not self.use_llm_mode:
            # 开启 LLM 模式：构造新的 QSplitter，将传统模式和 LLM 模块添加进去
            splitter = QSplitter(Qt.Horizontal)
            splitter.addWidget(self.traditional_tabs)
            self.llm_panel.setMinimumWidth(200)  # LLM 模块至少 200px
            splitter.addWidget(self.llm_panel)
            self.setCentralWidget(splitter)
            self.use_llm_mode = True
            self.llm_toggle_action.setText("Hide LLMs")
            if self.llm_api_key_input.text().strip():
                self.llm_display.append(self.translations[self.current_language]['upload_code_prompt'])
                self.upload_code_to_llm()
            else:
                self.llm_display.append("No API key provided. Skipping code upload.")
        else:
            # 关闭 LLM 模式：切换回仅显示传统模式
            self.setCentralWidget(self.traditional_tabs)
            self.use_llm_mode = False
            self.llm_toggle_action.setText("LLMs")

    def change_language(self, lang):
        self.current_language = lang
        self.trans = self.translations[self.current_language]
        self.update_ui_text()

    def update_ui_text(self):
        tr = self.translations[self.current_language]
        self.setWindowTitle(tr['window_title'])
        self.traditional_tabs.setTabText(0, tr['tab_data_selection'])
        self.traditional_tabs.setTabText(1, tr['tab_settings'])
        self.traditional_tabs.setTabText(2, tr['tab_map_generation'])
        self.file_label.setText(tr['no_file_selected'])
        self.file_button.setText(tr['choose_geojson_file'])
        self.var_group.setTitle(tr['variable_selection_group'])
        self.var1_label.setText(tr['select_variable_1'])
        self.var2_label.setText(tr['select_variable_2'])
        self.break_group.setTitle(tr['break_settings_group'])
        self.break_method_label.setText(tr['select_break_method'])
        self.break_method_combo.blockSignals(True)
        self.break_method_combo.clear()
        self.break_method_combo.addItems([tr['manual_input'], tr['natural_breaks']])
        self.break_method_combo.blockSignals(False)
        self.calculate_button.setText(tr['calculate_natural_breaks'])
        self.count_label.setText(tr['select_number_of_classes'])
        self.break_input1_label.setText(tr['variable1_breaks'])
        self.break_input2_label.setText(tr['variable2_breaks'])
        self.color_group.setTitle(tr['color_matrix_settings_group'])
        self.ramp1_label.setText(tr['variable1_color_ramp'])
        self.ramp2_label.setText(tr['variable2_color_ramp'])
        self.custom_ramp1_input.setPlaceholderText(tr['enter_custom_colors_var1'])
        self.custom_ramp2_input.setPlaceholderText(tr['enter_custom_colors_var2'])
        self.preview_button.setText(tr['preview_color_matrix'])
        self.color_matrix_input_label.setText(tr['color_matrix_input_label'])
        self.color_matrix_preview_label.setText(tr['color_matrix_preview_label'])
        self.tooltip_group.setTitle(tr['tooltip_settings_group'])
        self.tooltip_instructions.setText(tr['tooltip_instructions'])
        for i, (field_label, label_label) in enumerate(zip(self.tooltip_field_labels, self.tooltip_label_labels),
                                                       start=1):
            field_label.setText(tr['field_label'].format(num=i))
            label_label.setText(tr['label_label'])
        self.generate_button.setText(tr['generate_map'])
        self.save_button.setText(tr['save_map'])
        self.analyze_map_button.setText(tr['analyze_map'])
        self.llm_api_key_label.setText(tr['llm_api_key'])
        self.tool_instructions_display.setPlainText(tr['tool_intro'])
        self.llm_upload_button.setText(tr['upload_geojson'])

    def get_stylesheet(self):
        """Return global application stylesheet with improved spacing, rounded corners and soft colours."""
        return (
            "QMainWindow { background-color: #F9FAFB; }"
            "QGroupBox { font-weight: 600; border: 1px solid #E5E7EB; border-radius: 8px; margin-top: 12px; background-color: #FFFFFF; }"
            "QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }"
            "QLabel { font-size: 14px; color: #111827; }"
            "QLineEdit, QComboBox, QTextEdit, QSpinBox { font-size: 14px; padding: 6px 8px; border: 1px solid #D1D5DB; border-radius: 6px; background-color: #FFFFFF; }"
            "QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QSpinBox:focus { border: 1px solid #6F5DAB; }"
            "QPushButton { background-color: #6F5DAB; color: #FFFFFF; border: none; padding: 8px 18px; font-size: 14px; border-radius: 6px; }"
            "QPushButton:hover { background-color: #5E4F91; }"
            "QPushButton:disabled { background-color: #E5E7EB; color: #9CA3AF; }"
            "QTabWidget::pane { border: 1px solid #E5E7EB; background-color: #FFFFFF; border-radius: 6px; }"
            "QTabBar::tab { background: #F3F4F6; border: 1px solid #E5E7EB; padding: 10px 14px; border-top-left-radius: 6px; border-top-right-radius: 6px; min-width: 110px; }"
            "QTabBar::tab:selected { background: #FFFFFF; }"
            "QMenuBar { background-color: #6F5DAB; color: #FFFFFF; }"
            "QMenuBar::item { padding: 6px 12px; background-color: transparent; }"
            "QMenuBar::item:selected { background-color: #5E4F91; }"
            "QMenu { background-color: #FFFFFF; border: 1px solid #E5E7EB; }"
            "QMenu::item { padding: 6px 20px; }"
            "QMenu::item:selected { background-color: #F3F4F6; }"
        )


    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.translations[self.current_language]['choose_geojson_file'],
            "",
            "GeoJSON Files (*.geojson)"
        )
        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path)
            try:
                self.gdf = gpd.read_file(file_path)
                if self.gdf.crs and self.gdf.crs.to_epsg() != 4326:
                    self.gdf = self.gdf.to_crs(epsg=4326)
            except Exception as e:
                QMessageBox.critical(self, self.translations[self.current_language]['window_title'],
                                     f"{self.translations[self.current_language]['file_read_error']}: {e}")
                self.gdf = None
                return
            all_fields = list(self.gdf.columns)
            if len(all_fields) < 2:
                QMessageBox.warning(self, self.translations[self.current_language]['window_title'],
                                    self.translations[self.current_language]['insufficient_columns'])
                return
            self.update_field_options(all_fields)
            self.shared_state["fields"] = all_fields
            self.shared_state["file_loaded"] = True
            self.state_changed.emit(self.shared_state)
            self.advance_llm_state("fields_listed", all_fields)
        else:
            self.llm_display.append("No file selected.")

    def calculate_breaks(self):
        if self.break_method_combo.currentText() == self.translations[self.current_language][
            'natural_breaks'] and self.use_llm_mode:
            reply = QMessageBox.question(
                self,
                self.translations[self.current_language]['confirmation_title'],
                self.translations[self.current_language]['natural_breaks_confirm'].format(
                    self.break_count_spin.value()),
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        if self.use_llm_mode and self.selected_vars:
            var1 = self.selected_vars.get("var1", "")
            var2 = self.selected_vars.get("var2", "")
        else:
            var1 = self.var1_combo.currentText()
            var2 = self.var2_combo.currentText()
        n_classes = self.break_count_spin.value()
        if var1 and var2 and self.gdf is not None:
            try:
                breaks1 = jenkspy.jenks_breaks(self.gdf[var1].dropna().values, n_classes=n_classes)
                breaks2 = jenkspy.jenks_breaks(self.gdf[var2].dropna().values, n_classes=n_classes)
                self.break_input_1.setText(",".join(map(str, breaks1)))
                self.break_input_2.setText(",".join(map(str, breaks2)))
                self.breaks1 = breaks1
                self.breaks2 = breaks2
                self.generate_color_matrix()
                QMessageBox.information(self, self.translations[self.current_language]['window_title'],
                                        self.translations[self.current_language]['breaks_calculated'])
                self.shared_state["breaks1"] = breaks1
                self.shared_state["breaks2"] = breaks2
                self.state_changed.emit(self.shared_state)
                self.update_traditional_ui_from_shared_state()
                self.advance_llm_state("breaks_set", {"breaks1": breaks1, "breaks2": breaks2})
            except Exception as e:
                QMessageBox.critical(self, self.translations[self.current_language]['window_title'],
                                     self.translations[self.current_language]['break_calculation_failed'].format(
                                         error=e))

    def toggle_custom_input(self, text, var_index):
        if var_index == 1:
            self.custom_ramp1_input.setVisible(text in ["Custom", "自定义"])
        elif var_index == 2:
            self.custom_ramp2_input.setVisible(text in ["Custom", "自定义"])

    def update_color_matrix_size(self):
        self.color_matrix_input.clear()
        self.update_color_preview()

    def generate_color_matrix(self):
        n_classes = self.break_count_spin.value()
        if self.use_llm_mode and self.selected_color_scheme1 and self.selected_color_scheme2:
            scheme1 = self.selected_color_scheme1
            scheme2 = self.selected_color_scheme2
            base_colors1 = get_expanded_colors(DEFAULT_RAMP_COLORS.get(scheme1, []), n_classes)
            base_colors2 = get_expanded_colors(DEFAULT_RAMP_COLORS.get(scheme2, []), n_classes)
        else:
            if self.ramp1_combo.currentText() in ["Custom", "自定义"]:
                custom_colors1 = [c.strip() for c in self.custom_ramp1_input.text().split(",") if c.strip()]
                if len(custom_colors1) != n_classes:
                    QMessageBox.warning(self, self.translations[self.current_language]['window_title'],
                                        f"{self.translations[self.current_language]['variable1_color_ramp']} {n_classes}!")
                    return
                base_colors1 = custom_colors1
            else:
                ramp1_name = self.ramp1_combo.currentText()
                base_colors1 = get_expanded_colors(DEFAULT_RAMP_COLORS.get(ramp1_name, []), n_classes)
            if self.ramp2_combo.currentText() in ["Custom", "自定义"]:
                custom_colors2 = [c.strip() for c in self.custom_ramp2_input.text().split(",") if c.strip()]
                if len(custom_colors2) != n_classes:
                    QMessageBox.warning(self, self.translations[self.current_language]['window_title'],
                                        f"{self.translations[self.current_language]['variable2_color_ramp']} {n_classes}!")
                    return
                base_colors2 = custom_colors2
            else:
                ramp2_name = self.ramp2_combo.currentText()
                base_colors2 = get_expanded_colors(DEFAULT_RAMP_COLORS.get(ramp2_name, []), n_classes)
        bivariate_colors = []
        for i in range(n_classes):
            row_colors = []
            for j in range(n_classes):
                row_colors.append(blend_colors(base_colors1[i], base_colors2[j]))
            bivariate_colors.append(",".join(row_colors))
        matrix_text = "\n".join(bivariate_colors)
        self.color_matrix_input.setPlainText(matrix_text)
        self.update_color_preview()
        self.advance_llm_state("color_set", {"color_scheme1": self.ramp1_combo.currentText(),
                                             "color_scheme2": self.ramp2_combo.currentText()})

    def update_color_preview(self):
        matrix_lines = self.color_matrix_input.toPlainText().splitlines()
        html = "<table border='1' cellpadding='5' cellspacing='0'>"
        for row in matrix_lines:
            colors = [c.strip() for c in row.split(",")]
            html += "<tr>"
            for color in colors:
                if color:
                    html += f"<td style='background-color:{color}; width:30px; height:30px;'></td>"
                else:
                    html += "<td></td>"
            html += "</tr>"
        html += "</table>"
        self.color_preview.setText(html)

    def generate_map(self):
        if self.gdf is None or self.gdf.empty:
            QMessageBox.warning(self, self.translations[self.current_language]['window_title'],
                                self.translations[self.current_language]['no_file_selected'])
            return
        if not hasattr(self, 'breaks1') or not hasattr(self, 'breaks2'):
            QMessageBox.warning(self, self.translations[self.current_language]['window_title'],
                                self.translations[self.current_language]['break_calculation_failed'].format(
                                    error=self.tr("No breaks")))
            return
        n_classes = self.break_count_spin.value()
        if self.use_llm_mode and self.selected_vars:
            var1 = self.selected_vars.get("var1", "")
            var2 = self.selected_vars.get("var2", "")
        else:
            var1 = self.var1_combo.currentText()
            var2 = self.var2_combo.currentText()

        def classify(value, breaks):
            for i in range(len(breaks) - 1):
                if breaks[i] <= value < breaks[i + 1]:
                    return i
            return len(breaks) - 2

        self.gdf[f"{var1}_class"] = self.gdf[var1].apply(lambda x: classify(x, self.breaks1))
        self.gdf[f"{var2}_class"] = self.gdf[var2].apply(lambda x: classify(x, self.breaks2))
        colors_matrix = [[c.strip() for c in row.split(",")] for row in
                         self.color_matrix_input.toPlainText().splitlines() if row.strip()]

        def bivariate_color(row):
            index_var1 = int(row[f"{var1}_class"])
            index_var2 = int(row[f"{var2}_class"])
            try:
                return colors_matrix[index_var1][index_var2]
            except IndexError:
                return "#FFFFFF"

        self.gdf["fillColor"] = self.gdf.apply(bivariate_color, axis=1)
        centroid = self.gdf.geometry.centroid
        centroid_y, centroid_x = centroid.y.mean(), centroid.x.mean()
        tooltip_fields = [combo.currentText() for combo, _ in self.tooltip_selectors if combo.currentText()]
        tooltip_aliases = [edit.text().strip() if edit.text().strip() != "" else combo.currentText() for combo, edit in
                           self.tooltip_selectors if combo.currentText()]
        if len(tooltip_fields) != len(tooltip_aliases):
            tooltip_aliases = tooltip_fields.copy()
        m = folium.Map(location=[centroid_y, centroid_x], zoom_start=5)
        folium.GeoJson(
            data=self.gdf.__geo_interface__,
            style_function=lambda feature: {
                'fillColor': feature["properties"].get("fillColor", "#000000"),
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.7
            },
            tooltip=folium.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True
            )
        ).add_to(m)
        legend_html = create_bivariate_legend_html(
            breaks1=self.breaks1,
            breaks2=self.breaks2,
            color_matrix=colors_matrix,
            var1_name=var1,
            var2_name=var2,
            legend_title=self.translations[self.current_language]['legend_title']
        )
        m.get_root().html.add_child(folium.Element(legend_html))
        m.save(self.map_html)
        self.map_preview.load(QUrl.fromLocalFile(os.path.abspath(self.map_html)))
        if self.use_llm_mode:
            self.advance_llm_state("preview")
        QMessageBox.information(self, self.translations[self.current_language]['window_title'],
                                self.translations[self.current_language]['generate_map'] + " " + self.tr("completed"))
        self.save_button.setEnabled(True)

    def save_map(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            self.translations[self.current_language]['save_map'],
            "bivariate_map.html",
            "HTML Files (*.html)"
        )
        if save_path:
            try:
                import shutil
                shutil.copy(self.map_html, save_path)
                QMessageBox.information(self, self.translations[self.current_language]['window_title'],
                                        self.translations[self.current_language]['save_map'] + " " + save_path)
                self.advance_llm_state("final")
            except Exception as e:
                QMessageBox.critical(self, self.translations[self.current_language]['window_title'],
                                     self.translations[self.current_language]['break_calculation_failed'].format(
                                         error=e))

    def upload_code_to_llm(self):
        try:
            code_path = __file__
            with open(code_path, "r", encoding="utf-8") as f:
                code_content = f.read(1000)
            prompt = f"你是一个地理可视化工具的操作助手。请根据下面的代码摘要，简要说明该工具的主要功能（仅输出中文）：\n\n{code_content}\n\n"
            openai.api_key = self.llm_api_key_input.text().strip()
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0
            )
            intro = response.choices[0].message.content.strip()
            self.llm_display.append("Tool Info: " + intro)
        except Exception as e:
            self.llm_display.append("Failed to upload code: " + str(e))

    def llm_upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.translations[self.current_language]['choose_geojson_file'],
            "",
            "GeoJSON Files (*.geojson)"
        )
        if file_path:
            self.file_path = file_path
            try:
                self.gdf = gpd.read_file(file_path)
                if self.gdf.crs and self.gdf.crs.to_epsg() != 4326:
                    self.gdf = self.gdf.to_crs(epsg=4326)
                self.llm_display.append("File upload successful!")
                self.shared_state["fields"] = list(self.gdf.columns)
                self.shared_state["file_loaded"] = True
                self.update_field_options(self.shared_state["fields"])
                self.state_changed.emit(self.shared_state)
                self.advance_llm_state("fields_listed", self.shared_state["fields"])
            except Exception as e:
                self.llm_display.append("File upload failed: " + str(e))
        else:
            self.llm_display.append("No file selected.")

    def process_llm_conversation(self):
        user_text = self.llm_input.text().strip()
        if not user_text:
            QMessageBox.warning(self, self.translations[self.current_language]['window_title'],
                                self.translations[self.current_language]['llm_empty_warning'])
            return
        self.llm_display.append("User: " + user_text)
        if self.current_language.lower() == "en":
            next_step_prompts = {
                "fields_listed": "[Tip] Next step: Please specify the two variables for visualization, e.g. 'Material cultural heritage, Intangible cultural heritage'.",
                "variables_selected": "[Tip] Next step: Please specify the break method, choose either 'natural breaks' or 'manual'.",
                "manual_break": "[Tip] Next step: Please enter manual break points, numbers separated by commas, e.g. '10,20,30,40'.",
                "breaks_set": "[Tip] Next step: Please choose default color schemes for both variables.",
                "color_set": "[Tip] Next step: Please enter tooltip fields and corresponding labels, e.g. 'field1, field2, field3; label1, label2, label3'.",
                "tooltip_set": "[Tip] Next step: Please specify whether to preview the map, enter 'yes' or 'no'.",
                "preview": "[Tip] Next step: If you are satisfied with the preview, please enter a command to save the map.",
                "final": "[Tip] Process finished.",
                "natural_break_classes": "[Tip] Next step: Please enter the number of classes (2-10) for natural break calculation."
            }
        else:
            next_step_prompts = {
                "fields_listed": "【提示】下一步：请选择用于可视化的两个变量，例如：Material cultural heritage, Intangible cultural heritage。",
                "variables_selected": "【提示】下一步：请输入断点生成方式，取值为 natural breaks（自然间断点法）或 manual（手动断点）。",
                "manual_break": "【提示】下一步：请输入手动断点，数字以逗号分隔，例如：10,20,30,40。",
                "breaks_set": "【提示】下一步：请选择两个变量的默认配色方案，格式为：color1, color2。可选方案有：" + ", ".join(
                    list(DEFAULT_RAMP_COLORS.keys())),
                "color_set": "【提示】下一步：请输入图例提示字段及对应标签，例如：field1, field2, field3; label1, label2, label3。",
                "tooltip_set": "【提示】下一步：请输入是否预览地图，输入 yes 或 no。",
                "preview": "【提示】下一步：如果预览满意，请输入保存地图的命令。",
                "final": "【提示】流程结束。",
                "natural_break_classes": "【提示】下一步：请输入自然断点计算的类别数（2-10）："
            }
        try:
            openai.api_key = self.llm_api_key_input.text().strip()
            prompt = ""
            if self.llm_state == "fields_listed":
                actual_fields = list(self.gdf.columns)
                fields_str = ", ".join(actual_fields)
                prompt = (
                        "Please convert the following user input into a JSON command that selects two variables for visualization. "
                        "Ensure the variables exist in the following list: " + fields_str +
                        "\nReturn format:\n{ \"action\": \"select_variables\", \"parameters\": { \"var1\": \"<Variable 1>\", \"var2\": \"<Variable 2>\" } }\n"
                        "User input: " + user_text
                )
            elif self.llm_state == "variables_selected":
                prompt = (
                        "Please convert the following user input into a JSON command indicating the break method. The value should be 'natural breaks' or 'manual':\n"
                        '{ "action": "set_break_method", "parameters": { "break_method": "<natural breaks|manual>" } }\n'
                        "User input: " + user_text
                )
            elif self.llm_state == "natural_break_classes":
                try:
                    n_classes = int(user_text)
                    if n_classes < 2 or n_classes > 10:
                        self.llm_display.append("Invalid number, please input an integer between 2 and 10.")
                    else:
                        self.break_count_spin.setValue(n_classes)
                        self.llm_display.append(
                            "Number of classes set to: " + str(n_classes) + ". Now calculating natural breaks...")
                        self.calculate_breaks()
                        if hasattr(self, "breaks1") and hasattr(self, "breaks2"):
                            self.llm_state = "breaks_set"
                            self.llm_display.append(next_step_prompts["breaks_set"])
                        else:
                            self.llm_display.append(
                                "Natural break calculation failed. Please re-enter the number of classes.")
                except ValueError:
                    self.llm_display.append("Invalid input. Please enter an integer between 2 and 10.")
            elif self.llm_state == "manual_break":
                prompt = (
                        "Please convert the following user input into a JSON command to set manual breaks, numbers separated by commas:\n"
                        '{ "action": "set_breaks", "parameters": { "breaks1": "<break1,comma-separated>", "breaks2": "<break2,comma-separated>" } }\n'
                        "User input: " + user_text
                )
            elif self.llm_state == "breaks_set":
                available_schemes = ", ".join(list(DEFAULT_RAMP_COLORS.keys()))
                prompt = (
                        "Please convert the following user input into a JSON command to set default color schemes for the two variables. Separate the two options with a comma.\n"
                        '{ "action": "set_color_scheme", "parameters": { "color1": "<Scheme1>", "color2": "<Scheme2>" } }\n'
                        "Available options: " + available_schemes + "\nUser input: " + user_text
                )
            elif self.llm_state == "color_set":
                prompt = (
                        "Please convert the following user input into a JSON command to set tooltip fields and labels. Return format:\n"
                        '{ "action": "set_tooltip", "parameters": { "fields": ["<Field1>", "<Field2>", "<Field3>"], "labels": ["<Label1>", "<Label2>", "<Label3>"] } }\n'
                        "Available fields: " + ", ".join(list(self.gdf.columns)) + "\nUser input: " + user_text
                )
            elif self.llm_state == "tooltip_set":
                prompt = (
                        "Please convert the following user input into a JSON command indicating whether to preview the map (preview value should be 'yes' or 'no'):\n"
                        '{ "action": "preview_map", "parameters": { "preview": "<yes|no>" } }\n'
                        "User input: " + user_text
                )
            elif self.llm_state == "preview":
                prompt = (
                        "Please convert the following user input into a JSON command to save the map. Return format:\n"
                        '{ "action": "save_map", "parameters": {} }\n'
                        "User input: " + user_text
                )
            else:
                prompt = user_text
            if prompt:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                    temperature=0
                )
                answer = response.choices[0].message.content.strip()
                self.llm_display.append("LLM: " + answer)
                try:
                    command_dict = json.loads(answer)
                    action = command_dict.get("action")
                    if self.llm_state == "fields_listed" and action == "select_variables":
                        self.selected_vars = command_dict.get("parameters", {})
                        self.llm_display.append("Variables selected: " + str(self.selected_vars))
                        if "var1" in self.selected_vars and "var2" in self.selected_vars:
                            self.var1_combo.setCurrentText(self.selected_vars["var1"])
                            self.var2_combo.setCurrentText(self.selected_vars["var2"])
                            self.shared_state["var1"] = self.selected_vars["var1"]
                            self.shared_state["var2"] = self.selected_vars["var2"]
                            self.state_changed.emit(self.shared_state)
                        self.llm_state = "variables_selected"
                        self.llm_display.append(next_step_prompts["variables_selected"])
                    elif self.llm_state == "variables_selected" and action == "set_break_method":
                        method = command_dict.get("parameters", {}).get("break_method",
                                                                        "natural breaks").strip().lower()
                        self.llm_display.append("Break method set to: " + method)
                        if method == "natural breaks":
                            self.break_method_combo.setCurrentText(
                                self.translations[self.current_language]['natural_breaks'])
                            self.toggle_break_method()
                            self.llm_state = "natural_break_classes"
                            self.llm_display.append(next_step_prompts["natural_break_classes"])
                        else:
                            self.break_method_combo.setCurrentText(
                                self.translations[self.current_language]['manual_input'])
                            self.toggle_break_method()
                            self.llm_state = "manual_break"
                            self.llm_display.append(next_step_prompts["manual_break"])
                    elif self.llm_state == "manual_break" and action == "set_breaks":
                        params = command_dict.get("parameters", {})
                        try:
                            breaks1 = list(map(float, params.get("breaks1", "").split(",")))
                            breaks2 = list(map(float, params.get("breaks2", "").split(",")))
                            self.breaks1 = breaks1
                            self.breaks2 = breaks2
                            self.break_input_1.setText(",".join(map(str, breaks1)))
                            self.break_input_2.setText(",".join(map(str, breaks2)))
                            self.llm_display.append("Manual breaks set.")
                            self.llm_state = "breaks_set"
                            self.llm_display.append(next_step_prompts["breaks_set"])
                            self.shared_state["breaks1"] = breaks1
                            self.shared_state["breaks2"] = breaks2
                            self.state_changed.emit(self.shared_state)
                            self.update_traditional_ui_from_shared_state()
                        except Exception as ex:
                            self.llm_display.append("Break parsing failed. Please re-enter.")
                    elif self.llm_state == "breaks_set" and action == "set_color_scheme":
                        color1 = command_dict.get("parameters", {}).get("color1", "")
                        color2 = command_dict.get("parameters", {}).get("color2", "")
                        if color1 and color2:
                            self.selected_color_scheme1 = color1
                            self.selected_color_scheme2 = color2
                            self.llm_display.append(
                                "Color schemes set: Variable 1: " + color1 + ", Variable 2: " + color2)
                            self.generate_color_matrix()
                            self.llm_state = "color_set"
                            self.llm_display.append(next_step_prompts["color_set"])
                            self.shared_state["color_scheme1"] = color1
                            self.shared_state["color_scheme2"] = color2
                            self.state_changed.emit(self.shared_state)
                            self.update_traditional_ui_from_shared_state()
                        else:
                            self.llm_display.append("Color scheme parsing failed. Please re-enter.")
                    elif self.llm_state == "color_set" and action == "set_tooltip":
                        tooltip_params = command_dict.get("parameters", {})
                        tooltip_fields = tooltip_params.get("fields", [])
                        tooltip_labels = tooltip_params.get("labels", [])
                        if len(tooltip_labels) < len(tooltip_fields):
                            tooltip_labels = tooltip_labels + ["" for _ in
                                                               range(len(tooltip_fields) - len(tooltip_labels))]
                        tooltip_labels = [label.strip() if label.strip() != "" else field for field, label in
                                          zip(tooltip_fields, tooltip_labels)]
                        tooltip_params["labels"] = tooltip_labels
                        self.llm_display.append("Tooltip settings: " + str(tooltip_params))
                        self.selected_tooltip = tooltip_params
                        self.llm_state = "tooltip_set"
                        self.llm_display.append(next_step_prompts["tooltip_set"])
                        self.shared_state["tooltip"] = tooltip_params
                        self.state_changed.emit(self.shared_state)
                        self.update_traditional_ui_from_shared_state()
                    elif self.llm_state == "tooltip_set" and action == "preview_map":
                        preview = command_dict.get("parameters", {}).get("preview", "no")
                        if preview.lower() == "yes":
                            self.generate_map()
                            self.llm_display.append("Map previewed. If satisfied, please enter the save command.")
                            self.llm_state = "preview"
                            self.llm_display.append(next_step_prompts["preview"])
                        else:
                            self.llm_display.append("Preview canceled.")
                    elif self.llm_state == "preview" and action == "save_map":
                        self.save_map()
                        self.llm_display.append("Map saved successfully.")
                        self.llm_state = "final"
                        self.llm_display.append(next_step_prompts["final"])
                    else:
                        self.llm_display.append(
                            "Unrecognized command or state mismatch. Please check your instruction.")
                except Exception as parse_e:
                    self.llm_display.append("Failed to parse response: " + str(parse_e))
        except Exception as e:
            self.llm_display.append(self.translations[self.current_language]['llm_conversation_error'].format(error=e))
        self.llm_input.clear()


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r"D:\Jupyter\遗产灾害\icon.ico"))
    window = BivariateMapApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
