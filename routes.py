from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, EditUserForm
from getipinfo import get_ip_info
import requests
from db import *
from logins import admin_required
from flask_login import login_user, logout_user, login_required
from nmapscan import run_nmap_scan
from whois import *

@app.route("/whois", methods=["GET", "POST"])
@login_required
def whois_search():
    search_result = None

    if request.method == "POST":
        target_ip = request.form.get("target_ip")

        if target_ip:
            # Run the WHOIS search
            search_result = run_whois_search(target_ip)

            # Save search history
            history = SearchHistory(
                user_id=current_user.id,  # Link the history to the current user
                target_ip=target_ip,
                scan_depth="whois",  # We'll treat it as a special scan type for WHOIS
                result=search_result
            )
            db.session.add(history)
            db.session.commit()

            flash(f"WHOIS search completed for {target_ip}!", "success")
        else:
            flash("Please provide an IP address.", "danger")

    return render_template("whois_search.html", search_result=search_result)

@app.route("/nmap", methods=["GET", "POST"])
@login_required
def nmap_scan():
    scan_result = None

    if request.method == "POST":
        target_ip = request.form.get("target_ip")
        scan_depth = request.form.get("scan_depth")  # Get the selected scan depth

        if target_ip and scan_depth:
            # Run the Nmap scan with the selected scan depth
            scan_result = run_nmap_scan(target_ip, scan_depth)

            # Save search history
            history = SearchHistory(
                user_id=current_user.id,  # Link the history to the current user
                target_ip=target_ip,
                scan_depth=scan_depth,
                result=scan_result
            )
            db.session.add(history)
            db.session.commit()

            # Flash a message indicating scan result
            flash(f"Scan completed for {target_ip} with depth: {scan_depth}!", "success")
        else:
            flash("Please provide both IP address and scan depth.", "danger")

    return render_template("nmap_scan.html", scan_result=scan_result)

@app.route("/history")
@login_required
def view_history():
    # Paginate results, 5 per page
    page = request.args.get('page', 1, type=int)  # Get current page number from the query string
    history = SearchHistory.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=3, error_out=False)  # Correct arguments

    return render_template("history.html", history=history)




# Admin route to view users
@app.route("/admin/users")
@admin_required
def view_users():
    users = User.query.all()  # Get all users from the database
    return render_template("user_management.html", users=users)

@app.route("/admin/delete_user/<int:user_id>")
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)  # Get user by ID
    db.session.delete(user)
    db.session.commit()  # Commit the deletion to the database
    flash("User deleted successfully!", "danger")
    return redirect(url_for("view_users"))


# Route to edit a user
@app.route("/admin/edit_user/<int:user_id>", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)  # Get the user by ID
    form = EditUserForm() # Assuming you have a form for editing the user

    if form.validate_on_submit():
        # If the form is submitted, update the user's information
        user.email = form.email.data  # Example: Update the email
        db.session.commit()  # Save the changes to the database
        flash("User updated successfully!", "success")
        return redirect(url_for("view_users"))  # Redirect to the user list page

    # Pre-fill the form with existing user data
    form.email.data = user.email
    return render_template("edit_user.html", form=form)

@app.route("/")
def home():
    # Example static cybersecurity tips
    tips = [
        "Use a strong and unique password for each account.",
        "Enable two-factor authentication (2FA) wherever possible.",
        "Be cautious of phishing emails and suspicious links.",
        "Keep your software and devices updated with the latest patches.",
        "Use a VPN for secure browsing, especially on public Wi-Fi.",
        "Regularly back up your important data to a secure location.",
        "Monitor your accounts for unusual activity and report anything suspicious.",
    ]

    # Fetch latest cybersecurity news using NewsAPI
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q=cybersecurity&apiKey={api_key}"

    try:
        # Sending GET request to NewsAPI
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        news_data = response.json()
        articles = news_data.get("articles", [])

        # Filter out articles with titles like "Removed", "Default Image", or other invalid placeholders
        articles = [
            article
            for article in articles
            if article.get("title") not in ["Removed", "Default Image", None]
            and article.get("description") not in ["[Removed]", None]
        ]
    except requests.exceptions.RequestException:
        articles = []

    # Limit the number of articles to display
    articles_to_show = articles[:4]  # Show only the first 5 articles

    print("Current user:", current_user.is_authenticated)  # Debug line to check user status

    # Pass tips and articles to the template
    return render_template("info.html", articles=articles_to_show, tips=tips, current_user = current_user)

# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Check if email is already in the database
        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Example: Creating a super user with email 'admin@admin.com'
        is_admin = True if email == 'admin@admin.com' else False
        new_user = User(email=email, password=hashed_password, is_admin=is_admin)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)  # This logs in the user and sets up the session
            flash("Login successful!", "success")
            return redirect(url_for("home"))  # Redirect to the home page
        else:
            flash("Invalid login credentials", "danger")

    return render_template("login.html", form=form)

@app.route('/logout')
@login_required  # This ensures that only logged-in users can log out
def logout():
    logout_user()
    return redirect(url_for('home'))

# Route for IP check page (showing an error message)
@app.route("/ipcheck/")
@login_required
def clearcheck():
    return render_template("IP_Error.html")

# Route for displaying information about a specific IP address
@app.route("/ipcheck/<ip>")
@login_required
def ipcheck(ip):
    ip_info = get_ip_info(ip)  # Assuming you have a function to fetch IP info
    return render_template("ipcheck.html", ip_info=ip_info)

# Route for displaying the security vulnerabilities page
@app.route("/security-vulnerabilities")
def security_vulnerabilities():
    return render_template("report.html")

# Route for displaying penetration testing tools
@app.route("/penetration-tools")
def penetration_tools():
    return render_template("tools.html")

# Define how Flask-Login loads the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
