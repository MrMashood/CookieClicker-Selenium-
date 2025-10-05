# Cookie Clicker Auto-Clicker (Selenium + Brave)

This project is a **guided project inspired by [Tech With Tim’s YouTube tutorial](https://www.youtube.com/watch?v=NB8OceGZGjA&t)**.  
In his original tutorial, he demonstrated how to automate the Cookie Clicker game using **Google Chrome** and Selenium.  
This version modifies and extends that project to work with the **Brave Browser** (which is Chromium-based) and adds additional stability and automation improvements.

---

## 🎯 Overview

This Python script automatically:
- Opens [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/)
- Clicks the big cookie continuously
- Buys affordable products and upgrades automatically  

It uses **Selenium** with **Brave**, and thanks to **Selenium Manager**, there’s **no need to manually download or manage ChromeDriver** — everything works out of the box.

---

## 🧰 Requirements
- **Windows** (with Brave installed)
- **Python 3.9+**
- **Selenium 4.36+**

---

## ⚙️ Setup

```powershell
# (optional) create and activate a virtual environment
python -m venv myenv
.\myenv\Scripts\activate

# install dependencies
pip install -r requirements.txt
