# راهنمای نصب اصلاحیه تصاویر ClipSift

۱. سرور پورت 8766 را متوقف کن.

۲. از سه فایل فعال نسخه پشتیبان بگیر و سه فایل داخل ZIP را در پوشه‌های متناظر نسخه مستقل جایگزین کن. این بسته را در نسخه اصلی `ClipSift_GitHub` جایگزین نکن تا ابتدا تست مستقل موفق شود.

۳. از پوشه `F:\SMU\ClipSift_Release_Test\ClipSift_Source` اجرا کن:

```powershell
F:\SMU\ClipSift_GitHub\.venv\Scripts\python.exe scripts\build_review_queue_v2.py outputs\release_test\subsamples_v6.json
```

۴. سرور را روی پورت 8766 اجرا کن و صفحه `/review?run=release_test` را تازه‌سازی کن. باید برای هر کاندیدا دو عکس ببینی: نمای نزدیک بدون کادر اضافی و فریم اصلی با فقط یک کادر.

این عملیات مدل را دوباره اجرا نمی‌کند و تصمیم‌های ذخیره‌شده در `review_decisions.json` را دست نمی‌زند.
