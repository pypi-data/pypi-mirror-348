# %%
import os
import sys
import threading
import random
import tempfile
import json
import numpy as np

import geopandas as gpd
import fiona
import folium
from branca.element import Template, Figure
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject, pyqtSlot, QThread
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QProgressBar, QTreeWidget,
    QTreeWidgetItem, QSplitter, QMessageBox, QColorDialog, QCheckBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QColor


class MapWorker(QObject):
    """工作线程：读取 GDB，生成带动态图层控制的地图 HTML"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    status_update = pyqtSignal(str)

    # def __init__(self, gdb_files, shanghai2000_proj, layer_colors):
    #     super().__init__()
    #     self.gdb_files = gdb_files
    #     self.shanghai2000_proj = shanghai2000_proj
    #     self.layer_colors = layer_colors
    #     self.temp_html = None

    def __init__(self, gdb_files, cad_files, shanghai2000_proj, layer_colors):
            super().__init__()
            self.gdb_files = gdb_files
            self.cad_files = cad_files
            self.shanghai2000_proj = shanghai2000_proj
            self.layer_colors = layer_colors
            self.temp_html = None
    def process(self):
        try:
            # 准备临时文件
            fd, self.temp_html = tempfile.mkstemp(suffix='.html')
            os.close(fd)

            # 先收集所有图层的 GeoJSON 数据和样式
            all_layers = []
            center_x_sum = 0
            center_y_sum = 0
            cnt = 0

            for gdb_path in self.gdb_files:
                base = os.path.basename(gdb_path)
                self.status_update.emit(f"扫描文件: {base}")
                try:
                    layers = fiona.listlayers(gdb_path)
                    for layer_name in layers:
                        display_name = f"{base} - {layer_name}"
                        try:
                            gdf = gpd.read_file(gdb_path, layer=layer_name)
                            # Check if we have valid geometries before proceeding
                            if gdf.empty or 'geometry' not in gdf.columns or gdf.geometry.isna().all():
                                print(f"[Warning] Layer {display_name} has no valid geometries")
                                continue
                            
                            
                            gdf = gdf.set_crs(self.shanghai2000_proj, allow_override=True)
                            gdf_wgs84 = gdf.to_crs(epsg=4326)
                            # 2. 现在再打印转换后的信息
                            print(f"After to_crs: {len(gdf_wgs84)} 条记录，几何类型分布：")
                            print(gdf_wgs84.geometry.geom_type.value_counts())
                            # 设置 CRS 并转换到 WGS84
                            # if gdf.crs is None:
                            gdf = gdf.set_crs(self.shanghai2000_proj, allow_override=True)    
                            gdf_wgs84 = gdf.to_crs(epsg=4326)
                            
                        # # 仅把 datetime64[ns] 属性列转成字符串
                        #     for col, dtype in gdf_wgs84.dtypes.items():
                        #         if np.issubdtype(dtype, np.datetime64):
                        #             # 用 ISO 8601 格式，也避免后续解析歧义
                        #             gdf_wgs84[col] = gdf_wgs84[col].dt.strftime("%Y-%m-%dT%H:%M:%S")
                            # 在生成 folium GeoJson 之前加入
                            try:
                                for col in gdf_wgs84.columns:
                                    if gdf_wgs84[col].dtype.name.startswith("datetime"):
                                        gdf_wgs84[col] = gdf_wgs84[col].astype(str)
                            except Exception as e:
                                print(f"[Warning] 转换图层 {display_name} 失败：{e}")        

                            # 计算中心点以平均
                            if 'geometry' in gdf_wgs84 and not gdf_wgs84.empty:
                                geom = gdf_wgs84.geometry.union_all().centroid
                                center_x_sum += geom.x
                                center_y_sum += geom.y
                                cnt += 1

                            # 准备 geojson 与颜色
                            geojson = gdf_wgs84.__geo_interface__
                            # geojson = json.loads(gdf_wgs84.to_json())      # to_json 会自动把 datetime 序列化为 ISO 字符串
                            color   = self.layer_colors.get((gdb_path, layer_name),
                                f'#{random.randint(0, 0xFFFFFF):06x}')
                            all_layers.append((display_name, geojson, color))
                        except Exception as e:
                            print(f"[Warning] 处理图层 {display_name} 失败：{e}")
                except Exception as e:
                    print(f"[Warning] 列出图层失败 {gdb_path}：{e}")

            
            for cad_path in self.cad_files:
                base_name = os.path.basename(cad_path)
                self.status_update.emit(f"处理CAD文件: {base_name}")
                try:
                    try:
                        # 先尝试列出CAD中的图层
                        cad_layers = fiona.listlayers(cad_path)
                        has_layers = len(cad_layers) > 0
                    except:
                        has_layers = False
                    if has_layers:
                        # 如果CAD有多个图层，分别处理
                        for layer_name in cad_layers:
                            display_name = f"CAD:{base_name} - {layer_name}"
                            try:
                                gdf = gpd.read_file(cad_path, layer=layer_name)
                                if gdf.empty or 'geometry' not in gdf.columns or gdf.geometry.isna().all():
                                    print(f"[Warning] CAD层 {display_name} 没有有效几何对象")
                                    continue    
                                # 设置坐标系统并转换
                                gdf = gdf.set_crs(self.shanghai2000_proj, allow_override=True)
                                gdf_wgs84 = gdf.to_crs(epsg=4326)                            
                                # 区分处理不同几何类型
                                print(f"CAD图层 {layer_name} 包含的几何类型:")
                                print(gdf_wgs84.geometry.geom_type.value_counts())
                                
                                # 计算中心点
                                if not gdf_wgs84.empty:
                                    geom = gdf_wgs84.geometry.union_all().centroid
                                    center_x_sum += geom.x
                                    center_y_sum += geom.y
                                    cnt += 1                            
                                # 处理封闭图形 - 特别标记Polygon类型
                                geojson = gdf_wgs84.__geo_interface__
                                color = self.layer_colors.get((cad_path, layer_name),
                                                            f'#{random.randint(0,0xFFFFFF):06x}')
                                all_layers.append((display_name, geojson, color))
                            except Exception as e:
                                print(f"[Warning] 处理CAD图层 {display_name} 失败: {e}")                                                
                    else:
                        # 如果CAD没有明确的图层或无法读取图层，作为整体处理
                        display_name = f"CAD:{base_name}"                             
                        try:
                            gdf = gpd.read_file(cad_path)
                            if gdf.empty or 'geometry' not in gdf.columns or gdf.geometry.isna().all():
                                print(f"[Warning] CAD文件 {display_name} 没有有效几何对象")
                                continue
                            
                            # 设置坐标系统并转换  
                            gdf = gdf.set_crs(self.shanghai2000_proj, allow_override=True)
                            gdf_wgs84 = gdf.to_crs(epsg=4326)
                            
                            # 输出几何类型信息以便调试
                            print(f"CAD文件 {base_name} 包含的几何类型:")
                            print(gdf_wgs84.geometry.geom_type.value_counts())
                            
                            # 计算中心点
                            if not gdf_wgs84.empty:
                                geom = gdf_wgs84.geometry.union_all().centroid
                                center_x_sum += geom.x
                                center_y_sum += geom.y
                                cnt += 1             

                            # 准备GeoJSON
                            geojson = gdf_wgs84.__geo_interface__
                            color = self.layer_colors.get((cad_path, None),
                                                        f'#{random.randint(0,0xFFFFFF):06x}')
                            all_layers.append((display_name, geojson, color))  
                            
                        except Exception as e:
                            print(f"[Warning] 处理CAD文件 {display_name} 失败: {e}")
                                                                   
                except Exception as e:
                    print(f"[Warning] 处理 CAD {name} 失败：{e}")
            
            if not all_layers:
                self.error.emit("未找到任何可用图层")
                return

            # 计算平均中心
            if cnt > 0:
                center = [center_y_sum / cnt, center_x_sum / cnt]
            else:
                center = [31.23, 121.47]  # fallback to Shanghai

            # 创建 Folium 地图
            m = folium.Map(location=center, zoom_start=12, control_scale=True)
            folium.TileLayer('OpenStreetMap').add_to(m)
            folium.TileLayer('Stamen Terrain').add_to(m)
            folium.TileLayer('Cartodb Positron').add_to(m)

            # 由于Template没有get_name方法，我们手动为地图命名
            map_var = "mapObj_" + str(random.randint(10000, 99999))

            # 构造一段注入脚本，将所有图层以 L.geoJson 形式加入并挂到 window.layerMap
            # 如果只想显示某个字段（比如备注字段 comment 或 备注），你可以在 onEachFeature 中写： var tooltip = props['备注'] || '';
            layer_js = []
            
            # // 修改 layer_js 中的样式处理部分，在 style 函数中添加对几何类型的判断:

            for i, (name, gj, clr) in enumerate(all_layers):
                var = f"layer_{i}"
                gj_str = json.dumps(gj, ensure_ascii=False)
                layer_js.append(f"""
                var {var} = L.geoJson({gj_str}, {{
                    style: function(feature) {{
                        // 判断是否为面状几何，需要填充
                        var isPolygon = feature.geometry && 
                            (feature.geometry.type === 'Polygon' || 
                            feature.geometry.type === 'MultiPolygon');
                        
                        // 面状要素和线状要素使用不同的样式
                        if (isPolygon) {{
                            return {{
                                color: '{clr}',
                                fillColor: '{clr}',
                                weight: 1.5,
                                fillOpacity: 0.5,
                                opacity: 0.8
                            }};
                        }} else {{
                            return {{
                                color: '{clr}',
                                weight: 2,
                                opacity: 0.9,
                                fillOpacity: 0.1
                            }};
                        }}
                    }},
                    pointToLayer: function (feature, latlng) {{
                        // 点状要素渲染为圆形标记
                        return L.circleMarker(latlng, {{
                            radius: 5,
                            fillColor: '{clr}',
                            color: '#000',
                            weight: 1,
                            opacity: 1,
                            fillOpacity: 0.8
                        }});
                    }},
                    onEachFeature: function(feature, layer) {{
                        var props = feature.properties;
                        var tooltip = "";
                        if (props) {{
                            // 将所有属性拼成一段 tooltip 字符串
                            for (var key in props) {{
                                if (props.hasOwnProperty(key) && props[key] !== null && props[key] !== undefined) {{
                                    tooltip += "<b>" + key + "</b>: " + props[key] + "<br>";
                                }}
                            }}
                        }}
                        if (tooltip) {{
                            layer.bindTooltip(tooltip, {{
                                sticky: true,
                                direction: "top"
                            }});
                        }}
                    }}
                }}).addTo({map_var});
                window.layerMap['{name}'] = {var};
                """)
            # for i, (name, gj, clr) in enumerate(all_layers):
            #     var = f"layer_{i}"
            #     gj_str = json.dumps(gj, ensure_ascii=False)
            #     layer_js.append(f"""
            #     var {var} = L.geoJson({gj_str}, {{
            #         style: function(feature) {{
            #             return {{color: '{clr}', fillColor: '{clr}', weight: 1.5, fillOpacity: 0.6}};
            #         }},
            #         onEachFeature: function(feature, layer) {{
            #             var props = feature.properties;
            #             var tooltip = "";
            #             if (props) {{
            #                 // 将所有属性拼成一段 tooltip 字符串，也可以只显示部分字段
            #                 for (var key in props) {{
            #                     if (props.hasOwnProperty(key)) {{
            #                         tooltip += "<b>" + key + "</b>: " + props[key] + "<br>";
            #                     }}
            #                 }}
            #             }}
            #             layer.bindTooltip(tooltip, {{
            #                 sticky: true,
            #                 direction: "top"
            #             }});
            #         }}
            #     }}).addTo({map_var});
            #     window.layerMap['{name}'] = {var};
            #     """)


            # 重新设计HTML，确保地图的变量名是我们控制的
            html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"/>
    <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"></script>
    <style>
        html, body, #map {
            width: 100%%;
            height: 100%%;
            margin: 0;
            padding: 0;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // 初始化地图
        var %s = L.map('map').setView([%f, %f], 12);
        
        // 基础地图图层
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(%s);
        
        // 图层控制
        window.layerMap = {};
        window.mapVarName = "%s";
        
        // 添加所有图层
        %s
        
        // 添加图层控制器
        L.control.layers(null, window.layerMap).addTo(%s);
    </script>
</body>
</html>
""" % (
                map_var, center[0], center[1], 
                map_var, map_var,
                "\n        ".join(layer_js),
                map_var
            )

            # 保存 HTML
            with open(self.temp_html, 'w', encoding='utf-8') as f:
                f.write(html_template)
            self.finished.emit(self.temp_html)

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            self.error.emit(f"地图生成失败：{e}")


class GDBMapViewer(QMainWindow):
    """主窗口：目录选择、图层列表、地图展示"""
    request_ui_update = pyqtSignal(str, str, str)  # gdb_path, layer_name, new_color

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GDB 内嵌地图可视化 (显隐+调色)")
        self.resize(1400, 900)

        # 上海2000 投影定义
        self.shanghai2000_proj = (
            "+proj=tmerc +lat_0=31.2353 +lon_0=121.4644 "
            "+k=1 +x_0=-265 +y_0=-10 +ellps=GRS80 +units=m +no_defs"
        )

        # 存储
        self.gdb_data = {}     # { gdb_path: ['layer1', 'layer2', ...] }
        self.layer_colors = {} # { (gdb_path, layer_name): '#rrggbb' }

        # UI：左侧面板
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["文件/图层", "操作"])
        self.tree.setColumnWidth(0, 300)

        btn_layout = QHBoxLayout()
        self.btn_select = QPushButton("选择 GDB 目录")
        self.btn_select.clicked.connect(self.select_gdb_directory)
        self.btn_clear = QPushButton("清除所有")
        self.btn_clear.clicked.connect(self.clear_all)
        self.btn_generate = QPushButton("生成/刷新 地图")
        self.btn_generate.clicked.connect(self.generate_map)
        btn_layout.addWidget(self.btn_select)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_generate)
        
        # 1）在 GDBMapViewer.__init__ 中，新增一个 CAD 按钮和存储列表
        self.cad_files = []  # 存放用户选的 CAD 文件
        self.btn_import_cad = QPushButton("导入 CAD 文件")
        self.btn_import_cad.clicked.connect(self.import_cad_files)
        btn_layout.addWidget(self.btn_import_cad)


        left_layout = QVBoxLayout()
        left_layout.addLayout(btn_layout)
        left_layout.addWidget(self.tree)
        self.lbl_status = QLabel("准备就绪")
        left_layout.addWidget(self.lbl_status)
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        left_layout.addWidget(self.progress)

        left = QWidget()
        left.setLayout(left_layout)

        # UI：右侧地图
        self.web = QWebEngineView()
        self._load_placeholder()

        right = QWidget()
        right.setLayout(QVBoxLayout())
        right.layout().addWidget(self.web)

        # 布局
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([400, 1000])
        self.setCentralWidget(splitter)

        # 线程相关
        self.worker_thread = None
        self.worker = None

        # Signal
        self.request_ui_update.connect(self._update_button_color)

    # 2）实现 import_cad_files 方法
    def import_cad_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "选择 CAD 文件", ".", "CAD 文件 (*.dxf *.dwg)"
        )
        if not paths:
            return
        for p in paths:
            if p not in self.cad_files:
                self.cad_files.append(p)
                # 在树视图中添加一个顶级节点展示
                top = QTreeWidgetItem(self.tree, [os.path.basename(p), "CAD"])
                top.setData(0, Qt.UserRole, ("CAD", p))
                top.setExpanded(True)
        self.lbl_status.setText(f"已导入 {len(self.cad_files)} 个 CAD 文件")
        
    def _load_placeholder(self):
        self.web.setHtml("""
<!DOCTYPE html><html><head><meta charset="utf-8">
<title>请生成地图</title><style>
body {display:flex;justify-content:center;align-items:center;
height:100vh;color:#666;font-family:sans-serif;}
</style></head><body>
<h2>请选择 GDB 目录，然后点击 "生成/刷新 地图"</h2>
</body></html>
""")

    def select_gdb_directory(self):
        d = QFileDialog.getExistingDirectory(self, "选择包含 .gdb 文件夹的目录", ".")
        if not d:
            return
        added = 0
        for name in os.listdir(d):
            full_path = os.path.join(d, name)
            if os.path.isdir(full_path) and name.lower().endswith(".gdb"):
                # 规范化路径以便正确比较
                norm_path = os.path.normpath(full_path)
                if norm_path not in self.gdb_data:
                    self._add_gdb(norm_path)
                    added += 1
        self.lbl_status.setText(f"新增 {added} 个 GDB 文件" if added else "未找到新 .gdb 文件")

    def _add_gdb(self, gdb_path):
        base = os.path.basename(gdb_path)
        top = QTreeWidgetItem(self.tree, [base, ""])
        self.gdb_data[gdb_path] = []

        try:
            layers = fiona.listlayers(gdb_path)
            for lyr in layers:
                self.gdb_data[gdb_path].append(lyr)
                key = (gdb_path, lyr)
                if key not in self.layer_colors:
                    self.layer_colors[key] = f'#{random.randint(0,0xFFFFFF):06x}'

                item = QTreeWidgetItem(top, [lyr, ""])
                item.setData(0, Qt.UserRole, key)

                # 可见性复选框
                cb = QCheckBox()
                cb.setChecked(True)
                cb.stateChanged.connect(lambda s, k=key: self.toggle_visibility(k, s == Qt.Checked))

                # 调色按钮
                btn = QPushButton("调色")
                btn.setToolTip(f"图层 {lyr} 颜色")
                btn.clicked.connect(lambda _, k=key: self.change_color(k))
                self._apply_btn_style(btn, self.layer_colors[key])

                # 合并到容器
                w = QWidget()
                hl = QHBoxLayout(w)
                hl.setContentsMargins(0,0,0,0)
                hl.addWidget(cb)
                hl.addWidget(btn)
                hl.addStretch()

                self.tree.setItemWidget(item, 1, w)
        except Exception as e:
            print(f"[Error] 读取 {gdb_path} 图层失败：{e}")

        top.setExpanded(True)

    def _apply_btn_style(self, btn, hexclr):
        # 按钮背景 + 文本对比色
        btn.setStyleSheet(f"""
            QPushButton {{ background-color: {hexclr}; color: {"white" if self._contrast(hexclr)<0.5 else "black"}; 
                              border:1px solid #888; padding:2px 6px; }}
        """)

    def _contrast(self, hexclr):
        c = QColor(hexclr)
        # 简单亮度
        lum = (0.299*c.red() + 0.587*c.green() + 0.114*c.blue())/255
        return lum

    def change_color(self, key):
        path, lyr = key
        curr = QColor(self.layer_colors[key])
        c = QColorDialog.getColor(curr, self, f"选择 {lyr} 颜色")
        if not c.isValid():
            return
        newhex = c.name()
        self.layer_colors[key] = newhex
        # 更新按钮外观
        self.request_ui_update.emit(path, lyr, newhex)
        # JS 实时更新
        disp = f"{os.path.basename(path)} - {lyr}"
        js = f"""
            if (window.layerMap && window.layerMap['{disp}']) {{
                window.layerMap['{disp}'].setStyle(function() {{
                    return {{color:'{newhex}', fillColor:'{newhex}', weight:1.5, fillOpacity:0.6}};
                }});
            }}
        """
        self.web.page().runJavaScript(js)

    @pyqtSlot(str, str, str)
    def _update_button_color(self, gdb_path, layer_name, newhex):
        # 在树中找到对应按钮并更新样式
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            top = root.child(i)
            path = top.text(0)
            if os.path.basename(gdb_path) == path:
                for j in range(top.childCount()):
                    itm = top.child(j)
                    key = itm.data(0, Qt.UserRole)
                    if key and key == (gdb_path, layer_name):
                        w = self.tree.itemWidget(itm, 1)
                        if w:
                            buttons = w.findChildren(QPushButton)
                            if buttons:
                                self._apply_btn_style(buttons[0], newhex)
                        return

    def toggle_visibility(self, key, visible):
        path, lyr = key
        disp = f"{os.path.basename(path)} - {lyr}"
        # 使用通用的JavaScript来处理图层可见性
        js = f"""
            if (window.layerMap && window.layerMap['{disp}']) {{
                if ({str(visible).lower()}) {{
                    if (window.mapVarName && window[window.mapVarName]) {{
                        window[window.mapVarName].addLayer(window.layerMap['{disp}']);
                    }}
                }} else {{
                    if (window.mapVarName && window[window.mapVarName]) {{
                        window[window.mapVarName].removeLayer(window.layerMap['{disp}']);
                    }}
                }}
            }}
        """
        self.web.page().runJavaScript(js)

    def clear_all(self):
        if self.worker_thread and self.worker_thread.isRunning():
            QMessageBox.warning(self, "请稍候", "地图正在生成，不能清除")
            return
        self.gdb_data.clear()
        self.layer_colors.clear()
        self.tree.clear()
        self._load_placeholder()
        self.lbl_status.setText("已清除所有")

    def generate_map(self):
        files = list(self.gdb_data.keys())
        if not files:
            QMessageBox.information(self, "提示", "请先选择 GDB 目录")
            return
        if self.worker_thread and self.worker_thread.isRunning():
            QMessageBox.warning(self, "处理中", "请等待当前生成完成")
            return

        # UI 锁定
        self.btn_select.setEnabled(False)
        self.btn_clear.setEnabled(False)
        self.btn_generate.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.lbl_status.setText("正在生成地图...")

        # 启动线程
        self.worker_thread = QThread()
        # self.worker = MapWorker(files, self.shanghai2000_proj, dict(self.layer_colors))
        self.worker = MapWorker(
            gdb_files=list(self.gdb_data.keys()),
            cad_files=list(self.cad_files),
            shanghai2000_proj=self.shanghai2000_proj,
            layer_colors=dict(self.layer_colors),
        )
        self.worker.moveToThread(self.worker_thread)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
        self.worker.status_update.connect(lambda s: self.lbl_status.setText(s))
        self.worker_thread.started.connect(self.worker.process)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.error.connect(self.worker_thread.quit)
        self.worker_thread.start()

    @pyqtSlot(str)
    def _on_finished(self, html):
        if os.path.exists(html):
            self.web.load(QUrl.fromLocalFile(html))
            self.lbl_status.setText("地图生成完成")
        else:
            self._on_error("输出文件不存在")
        self._reset_ui()

    @pyqtSlot(str)
    def _on_error(self, msg):
        QMessageBox.critical(self, "错误", msg)
        self.lbl_status.setText("生成失败")
        self._load_placeholder()
        self._reset_ui()

    def _reset_ui(self):
        self.btn_select.setEnabled(True)
        self.btn_clear.setEnabled(True)
        self.btn_generate.setEnabled(True)
        self.progress.setVisible(False)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

    def closeEvent(self, e):
        # 清理临时文件
        if self.worker and hasattr(self.worker, 'temp_html') and self.worker.temp_html:
            try:
                if os.path.exists(self.worker.temp_html):
                    os.remove(self.worker.temp_html)
            except Exception as ex:
                print(f"清理临时文件失败: {ex}")
        super().closeEvent(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = GDBMapViewer()
    viewer.show()
    sys.exit(app.exec_())
# %%
