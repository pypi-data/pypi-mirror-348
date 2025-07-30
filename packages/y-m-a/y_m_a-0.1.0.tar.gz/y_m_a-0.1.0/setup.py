from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="y_m_a",  # يجب أن يكون هذا الاسم فريدًا على PyPI
    version="0.1.0",  # ابدأ بإصدار 0.1.0 أو ما شابه
    author="Y_M_A_2025",
    author_email="your.email@example.com",
    description="مكتبة بسيطة لعمليات على النصوص.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="Non",  # رابط مستودع الكود الخاص بك (إذا كان موجودًا)
    packages=find_packages(),  # سيجد هذا تلقائيًا مجلد y_m_a كحزمة
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # استبدل بالترخيص الخاص بك
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
