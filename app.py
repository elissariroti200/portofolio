
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "portfolio_elis_secret"

# Lokasi file JSON
DATA_FILE = os.path.join("data", "portfolio.json")


# Membaca data JSON
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Menyimpan data JSON
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# HALAMAN UTAMA (READ)
@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", data=data)


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    data = load_data()
    return render_template("dashboard.html", data=data)


# MENAMBAH PROYEK (CREATE)
@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        data = load_data()

        proyek_baru = {
            "id": max(
                [p.get("id", 0) for p in data["projects"]],
                default=0
            ) + 1,
            "name": request.form.get("name", ""),
            "category": request.form.get("category", ""),
            "description": request.form.get("description", ""),
            "technologies": [
                t.strip()
                for t in request.form.get("technologies", "").split(",")
                if t.strip()
            ],
            "github": request.form.get("github", ""),
            "demo": request.form.get("demo", ""),
            "image": request.form.get("image", "")
        }

        data["projects"].append(proyek_baru)
        save_data(data)

        flash("Proyek berhasil ditambahkan!")
        return redirect(url_for("dashboard"))

    return render_template("tambah.html")


# MENGEDIT PROYEK (UPDATE)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    data = load_data()

    proyek = next(
        (p for p in data["projects"] if p["id"] == id),
        None
    )

    if proyek is None:
        flash("Proyek tidak ditemukan!")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        proyek["name"] = request.form.get("name", "")
        proyek["category"] = request.form.get("category", "")
        proyek["description"] = request.form.get("description", "")

        teknologi = request.form.get("technologies", "")
        proyek["technologies"] = [
            t.strip() for t in teknologi.split(",") if t.strip()
        ]

        proyek["github"] = request.form.get("github", "")
        proyek["demo"] = request.form.get("demo", "")
        proyek["image"] = request.form.get("image", "")

        save_data(data)

        flash("Proyek berhasil diperbarui!")
        return redirect(url_for("dashboard"))

    return render_template("edit.html", proyek=proyek)


# MENGHAPUS PROYEK (DELETE)
@app.route("/hapus/<int:id>", methods=["POST"])
def hapus(id):
    data = load_data()

    data["projects"] = [
        p for p in data["projects"] if p["id"] != id
    ]

    save_data(data)

    flash("Proyek berhasil dihapus!")
    return redirect(url_for("dashboard"))


# MENJALANKAN APLIKASI
if __name__ == "__main__":
    app.run(debug=True)
