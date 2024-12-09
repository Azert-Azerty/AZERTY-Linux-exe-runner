import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QFileDialog, QLabel, QTabWidget, QMessageBox)
import subprocess
import xml.etree.ElementTree as ET

def check_dependencies():
    """
    التحقق من وجود جميع المتطلبات الضرورية للتطبيق
    
    Returns:
        tuple: (bool, str) - حالة التحقق، ورسالة الخطأ إن وجدت
    """
    # قائمة المتطلبات للتحقق
    dependencies = [
        ('wine', 'Wine'),
        ('python3', 'Python 3'),
        ('pip', 'Pip'),
        ('update-desktop-database', 'Update Desktop Database')
    ]
    
    missing_deps = []
    
    for cmd, name in dependencies:
        if not shutil.which(cmd):
            missing_deps.append(name)
    
    # التحقق من وجود PyQt5
    try:
        import PyQt5
    except ImportError:
        missing_deps.append('PyQt5')
    
    # إذا كانت هناك متطلبات مفقودة
    if missing_deps:
        error_message = "المتطلبات التالية مفقودة:\n" + "\n".join(missing_deps)
        return False, error_message
    
    return True, ""

class WineExeRunner(QWidget):
    def __init__(self):
        super().__init__()
        
        # التحقق من المتطلبات قبل تشغيل التطبيق
        dependencies_ok, error_message = check_dependencies()
        if not dependencies_ok:
            # إنشاء مربع رسائل مع زر لفتح ملف المتطلبات
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("خطأ في المتطلبات")
            msg_box.setText(error_message)
            
            # إضافة زر لفتح ملف المتطلبات
            open_req_button = msg_box.addButton("فتح ملف المتطلبات", QMessageBox.ActionRole)
            cancel_button = msg_box.addButton(QMessageBox.Cancel)
            
            # تنفيذ مربع الرسائل
            msg_box.exec_()
            
            # التحقق من الزر الذي تم الضغط عليه
            if msg_box.clickedButton() == open_req_button:
                # فتح ملف المتطلبات
                requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
                
                # محاولة فتح الملف باستخدام الأمر الافتراضي للنظام
                try:
                    if sys.platform.startswith('darwin'):
                        subprocess.run(['open', requirements_path], check=True)
                    elif sys.platform.startswith('win'):
                        os.startfile(requirements_path)
                    else:  # linux
                        subprocess.run(['xdg-open', requirements_path], check=True)
                except Exception as e:
                    QMessageBox.warning(None, "خطأ", f"تعذر فتح ملف المتطلبات: {str(e)}")
            
            # إنهاء البرنامج
            sys.exit(1)
        
        self.initUI()
    
    def initUI(self):
        # تعيين العنوان والحجم
        self.setWindowTitle('AZERTY EXE Runner')
        self.setGeometry(300, 300, 600, 300)
        
        # إنشاء تبويب رئيسي
        self.tabs = QTabWidget()
        
        # إنشاء التبويبات
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        
        # إضافة التبويبات
        self.tabs.addTab(self.tab1, "Downloads EXE")
        self.tabs.addTab(self.tab2, "Wine 32bit Apps")
        
        # إعداد التبويب الأول
        self.setup_first_tab()
        
        # إعداد التبويب الثاني
        self.setup_second_tab()
        
        # تخطيط رئيسي
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        
        # تعيين التخطيط
        self.setLayout(main_layout)
    
    def setup_first_tab(self):
        # إنشاء تخطيط رأسي للتبويب الأول
        layout = QVBoxLayout()
        
        # إنشاء تخطيط أفقي للمسار وزر التصفح
        path_layout = QHBoxLayout()
        
        # مساحة إدخال المسار مع المسار الافتراضي
        self.path_input1 = QLineEdit()
        default_path = os.path.expanduser('~/Downloads')
        self.path_input1.setText(default_path)
        path_layout.addWidget(self.path_input1)
        
        # زر التصفح
        browse_btn1 = QPushButton('Browse')
        browse_btn1.clicked.connect(lambda: self.browse_file(self.path_input1))
        path_layout.addWidget(browse_btn1)
        
        # إضافة تخطيط المسار للتخطيط الرئيسي
        layout.addLayout(path_layout)
        
        # زر التشغيل
        run_btn1 = QPushButton('Run')
        run_btn1.clicked.connect(lambda: self.run_exe(self.path_input1))
        layout.addWidget(run_btn1)
        
        # منطقة عرض النتائج
        self.result_label1 = QLabel('النتائج ستظهر هنا')
        layout.addWidget(self.result_label1)
        
        # تعيين التخطيط للتبويب الأول
        self.tab1.setLayout(layout)
    
    def setup_second_tab(self):
        # إنشاء تخطيط رأسي للتبويب الثاني
        layout = QVBoxLayout()
        
        # إنشاء تخطيط أفقي للمسار وزر التصفح
        path_layout = QHBoxLayout()
        
        # مساحة إدخال المسار مع المسار الافتراضي لتطبيقات Wine 32bit
        self.path_input2 = QLineEdit()
        default_path = os.path.expanduser('~/.wine/drive_c/Program Files (x86)')
        self.path_input2.setText(default_path)
        path_layout.addWidget(self.path_input2)
        
        # زر التصفح
        browse_btn2 = QPushButton('Browse')
        browse_btn2.clicked.connect(lambda: self.browse_file(self.path_input2))
        path_layout.addWidget(browse_btn2)
        
        # إضافة تخطيط المسار للتخطيط الرئيسي
        layout.addLayout(path_layout)
        
        # زر إنشاء الاختصار
        create_shortcut_btn = QPushButton('إنشاء اختصار في قائمة ابدأ')
        create_shortcut_btn.clicked.connect(self.create_wine_shortcut)
        layout.addWidget(create_shortcut_btn)
        
        # زر التشغيل
        run_btn2 = QPushButton('Run')
        run_btn2.clicked.connect(lambda: self.run_exe(self.path_input2))
        layout.addWidget(run_btn2)
        
        # منطقة عرض النتائج
        self.result_label2 = QLabel('النتائج ستظهر هنا')
        layout.addWidget(self.result_label2)
        
        # تعيين التخطيط للتبويب الثاني
        self.tab2.setLayout(layout)
    
    def browse_file(self, path_input):
        # فتح مربع حوار اختيار الملف
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'اختر ملف EXE', 
            path_input.text(), 
            'Executable Files (*.exe)'
        )
        
        # تحديث مساحة الإدخال بالمسار المختار
        if file_path:
            path_input.setText(file_path)
    
    def create_wine_shortcut(self):
        # الحصول على المسار من مساحة الإدخال
        exe_path = self.path_input2.text()
        
        try:
            # التحقق من وجود الملف
            if not os.path.exists(exe_path):
                self.result_label2.setText('خطأ: الملف غير موجود')
                return
            
            # استخراج اسم البرنامج
            program_name = os.path.splitext(os.path.basename(exe_path))[0]
            
            # مسار مجلد الاختصارات لـ Wine
            start_menu_path = os.path.expanduser('~/.local/share/applications')
            os.makedirs(start_menu_path, exist_ok=True)
            
            # مسار الاختصار الجديد
            shortcut_path = os.path.join(start_menu_path, f'{program_name}_wine.desktop')
            
            # محتوى ملف الاختصار
            shortcut_content = f'''[Desktop Entry]
Name={program_name}
Exec=wine "{exe_path}"
Type=Application
Categories=Wine;
Icon=wine
'''
            
            # كتابة الاختصار
            with open(shortcut_path, 'w') as f:
                f.write(shortcut_content)
            
            # جعل الاختصار قابل للتنفيذ
            os.chmod(shortcut_path, 0o755)
            
            # تحديث قاعدة التطبيقات
            subprocess.run(['update-desktop-database', start_menu_path], check=True)
            
            # عرض رسالة نجاح
            self.result_label2.setText(f'تم إنشاء اختصار للبرنامج: {program_name}')
            
            # عرض رسالة تأكيد
            QMessageBox.information(
                self, 
                'نجاح', 
                f'تم إنشاء اختصار للبرنامج {program_name} في قائمة ابدأ'
            )
        
        except Exception as e:
            self.result_label2.setText(f'خطأ في إنشاء الاختصار: {str(e)}')
            
            # عرض رسالة خطأ
            QMessageBox.critical(
                self, 
                'خطأ', 
                f'حدث خطأ أثناء إنشاء الاختصار: {str(e)}'
            )
    
    def run_exe(self, path_input):
        # الحصول على المسار من مساحة الإدخال
        exe_path = path_input.text()
        
        try:
            # التحقق من وجود الملف
            if not os.path.exists(exe_path):
                # تحديد مربع النتائج المناسب
                result_label = self.result_label1 if path_input == self.path_input1 else self.result_label2
                result_label.setText('خطأ: الملف غير موجود')
                return
            
            # تشغيل الملف باستخدام Wine
            result = subprocess.run(
                ['wine', exe_path], 
                capture_output=True, 
                text=True
            )
            
            # تحديد مربع النتائج المناسب
            result_label = self.result_label1 if path_input == self.path_input1 else self.result_label2
            
            # عرض النتيجة
            if result.returncode == 0:
                result_label.setText('تم التشغيل بنجاح')
            else:
                result_label.setText(f'خطأ في التشغيل: {result.stderr}')
        
        except Exception as e:
            # تحديد مربع النتائج المناسب
            result_label = self.result_label1 if path_input == self.path_input1 else self.result_label2
            result_label.setText(f'خطأ: {str(e)}')

def main():
    app = QApplication(sys.argv)
    ex = WineExeRunner()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
