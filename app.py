from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT
        )
    """)
    db.commit()

init_db()

# ---------------- HOME + CREATE + READ ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()

    # CREATE
    if request.method == "POST":
        db.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?,?,?)",
            (request.form["name"], request.form["phone"], request.form["email"])
        )
        db.commit()
        return redirect("/")

    # READ
    contacts = db.execute("SELECT * FROM contacts").fetchall()
    return render_template_string(HTML, contacts=contacts)

# ---------------- DELETE ----------------
@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM contacts WHERE id=?", (id,))
    db.commit()
    return redirect("/")

# ---------------- HTML + BOOTSTRAP ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Contact Manager</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

<nav class="navbar navbar-dark bg-dark">
<div class="container">
<span class="navbar-brand">📇 Contact Manager</span>
</div>
</nav>

<div class="container mt-4">

<div class="card shadow mb-4">
<div class="card-body">
<h4>Add Contact</h4>

<form method="post">
<div class="row">
<div class="col-md-4">
<input name="name" class="form-control" placeholder="Name" required>
</div>
<div class="col-md-4">
<input name="phone" class="form-control" placeholder="Phone" required>
</div>
<div class="col-md-4">
<input name="email" class="form-control" placeholder="Email" required>
</div>
</div>
<button class="btn btn-success mt-3">Add Contact</button>
</form>

</div>
</div>

<table class="table table-bordered table-striped">
<thead class="table-dark">
<tr>
<th>Name</th>
<th>Phone</th>
<th>Email</th>
<th>Action</th>
</tr>
</thead>
<tbody>
{% for c in contacts %}
<tr>
<td>{{ c.name }}</td>
<td>{{ c.phone }}</td>
<td>{{ c.email }}</td>
<td>
<a href="/delete/{{ c.id }}" class="btn btn-danger btn-sm">Delete</a>
</td>
</tr>
{% endfor %}
</tbody>
</table>

</div>
</body>
</html>
"""

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True) 
