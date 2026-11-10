# Service_Coverage_Project

## اختيار مواقع الخدمات لتغطية أكبر طلب

**BIA601 — Intelligent Algorithms / الخوارزميات الذكية — الوظيفة الثانية (F25)**

**المجموعة: خوارزميات ذكية&Bia**

مشروع تغطية موزونة قصوى: نختار عدداً محدداً `k` من مواقع الخدمات لتغطية أكبر مجموع لأوزان الطلب. نقارن خوارزمية جينية (GA) وأسراب الجسيمات (PSO) ومستعمرة النمل (ACO) مكتوبة داخل المشروع، مع حل جشع ومرجع دقيق للحالات الصغيرة وحد أعلى لبقية الأحجام. البيانات مولّدة وليست بيانات جهة حقيقية.

Weighted maximum coverage: choose k service locations to cover the most demand weight, comparing GA, PSO, and ACO written from scratch.

## فريق العمل — خوارزميات ذكية&Bia

| العضو | GitHub | المسؤولية | القضية |
|---|---|---|---|
| لمى الحميد | [Lama219293](https://github.com/Lama219293) | تعريف المشكلة وتجهيز البيانات | [#1](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/1) |
| إبراهيم العسالي | [ibrahim188964](https://github.com/ibrahim188964) | مراجعة الخوارزمية الجينية | [#2](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/2) |
| حسن العش | — | مراجعة سرب الجسيمات | [#3](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/3) |
| بلال احمد قلاوي | — | مراجعة مستعمرة النمل | [#4](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/4) |
| ماريا خالد السعدي | [mariakhaled636-dotcom](https://github.com/mariakhaled636-dotcom) | فحص القيود والحل المرجعي، والتكامل النهائي والتوثيق | [#6](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/6) و[#10](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/10) |
| هديل شرف | [hadeel12-ctrl](https://github.com/hadeel12-ctrl) | إعادة التجارب والتحقق | [#5](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/5) |
| رهف النجار | — | الجداول والرسوم | [#7](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/7) |
| آيه أمين العلي | — | كتابة التقرير وتدقيقه | [#8](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/8) |
| ليال ميهوب | — | عرض النتائج ودليل التشغيل | [#9](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/9) |

مساهمة كل عضو موثّقة في التقرير (`Report.docx`) وفي تاريخ المستودع. الفريق تسعة أعضاء (ضمن شرط المقرر: 6 إلى 9).

حساب GitHub [l00349800-maker](https://github.com/l00349800-maker) أضاف اعتمادات Python في `project/requirements.txt` ([#11](https://github.com/mariakhaled636-dotcom/Service_Coverage_Project/issues/11)). لم يُطابَق هذا الحساب بعد مع أحد أسماء التقرير.

## التشغيل

Python 3.12 أو أحدث، من مجلد `project`:

```text
python -m pip install -r requirements.txt
python main.py
python verify.py
```

تجربة قصيرة تكتب في مجلد مستقل:

```text
python main.py --runs 2 --output ../trial_results
python verify.py --results ../trial_results
```

إعادة أول تشغيلة لكل خوارزمية ولكل مسألة، مع فحص سجل التقارب:

```text
python verify.py --rerun
```

التفاصيل التقنية موجودة في [`project/README.md`](project/README.md).

## النتائج والعرض

- التقرير: [`Report.docx`](Report.docx)
- لوحة النتائج التفاعلية: افتح [`index.html`](index.html) في المتصفح (ملف مستقل، لا يحتاج تشغيل خادم).
  لعرض الجداول والرسوم بعد التجربة الكاملة يكفي فتح الملف محلياً. الصفحة لا تنفّذ خوارزميات Python.
- بعد إعادة التجارب يمكن تحديث بيانات الصفحة عبر:

```text
python export_web_data.py
```

- مخرجات التجارب والرسوم: [`project/results/`](project/results/)
