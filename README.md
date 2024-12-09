# Wine EXE Runner

## المتطلبات
- Python 3.x
- PyQt5
- Wine

## التثبيت
1. قم بتثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

2. تأكد من تثبيت Wine:
```bash
sudo apt-get install wine  # للأنظمة القائمة على Debian/Ubuntu
```

## التشغيل
```bash
python wine_exe_runner.py
```

## الميزات
- مسار إدخال تلقائي في ~/Downloads
- زر تصفح لاختيار ملفات EXE
- زر تشغيل لفتح الملفات باستخدام Wine
