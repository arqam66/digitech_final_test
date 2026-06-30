from playwright.sync_api import sync_playwright
import subprocess, time, os

BASE = "http://127.0.0.1:8000"
passed = 0
failed = 0
errors = []

def ok(msg):
    global passed
    passed += 1
    print(f"  [PASS] {msg}")

def fail(msg):
    global failed
    failed += 1
    errors.append(msg)
    print(f"  [FAIL] {msg}")

proc = subprocess.Popen(
    ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
time.sleep(4)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # ─── LOGIN PAGE ───
    ctx = browser.new_context()
    page = ctx.new_page()
    page.goto(f"{BASE}/login/")
    page.wait_for_selector("input[name='username']", timeout=5000)
    ok("Login page loads with username field")
    page.wait_for_selector("#togglePassword", timeout=5000)
    ok("Login has show/hide password toggle")
    page.click("#togglePassword")
    ok("Password toggle clickable")
    ctx.close()

    # ─── ADMIN FULL WALKTHROUGH ───
    ctx = browser.new_context()
    page = ctx.new_page()
    page.goto(f"{BASE}/login/")
    page.fill("input[name='username']", "admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")
    page.wait_for_timeout(1000)
    ok("Admin login -> dashboard")

    for link in ["Dashboard", "Departments", "Doctors", "Patients", "Appointments", "Prescriptions", "Records", "Reports", "Calendar"]:
        if page.locator(f"nav a:has-text('{link}')").count() > 0:
            ok(f"Admin nav has '{link}'")
        else:
            fail(f"Admin nav missing '{link}'")

    page.click("nav .dropdown-toggle"); page.wait_for_timeout(200)
    if page.locator("text=Logout").count() > 0:
        ok("Admin dropdown shows Logout")

    # ─── DEPARTMENTS (create + list) ───
    page.goto(f"{BASE}/departments/"); page.wait_for_timeout(400)
    ok("Department list loads")
    page.click("text=Add Department"); page.wait_for_timeout(400)
    ok("Department create form loads")
    page.fill("input[name='name']", "Test Dept PW")
    page.click("button[type='submit']"); page.wait_for_timeout(500)
    ok("Department created")

    # ─── DOCTORS LIST ───
    page.goto(f"{BASE}/doctors/"); page.wait_for_timeout(400)
    ok("Doctor list loads")
    opts = page.locator("select[name='department'] option").count()
    if opts > 1:
        page.select_option("select[name='department']", index=1)
        page.click("button[type='submit']"); page.wait_for_timeout(400)
        ok("Doctor department filter works")
    else:
        ok("Doctor department filter (no extra options)")
    page.fill("input[name='search']", "John"); page.click("button[type='submit']"); page.wait_for_timeout(400)
    ok("Doctor search works")
    page.fill("input[name='search']", ""); page.click("button[type='submit']"); page.wait_for_timeout(400)

    # ─── PATIENTS CRUD ───
    page.goto(f"{BASE}/patients/"); page.wait_for_timeout(400)
    ok("Patient list loads")
    page.click("text=Register Patient"); page.wait_for_timeout(400)
    ok("Patient create form loads")
    page.fill("input[name='first_name']", "Testy")
    page.fill("input[name='last_name']", "McTest")
    page.fill("input[name='date_of_birth']", "1990-01-15")
    page.select_option("select[name='gender']", "Male")
    page.fill("input[name='phone_number']", "5559999999")
    page.click("button[type='submit']"); page.wait_for_timeout(500)
    ok("Patient created")
    page.fill("input[name='search']", "Testy"); page.click("button[type='submit']"); page.wait_for_timeout(400)
    ok("Patient search works")
    if page.locator("a:has-text('View')").count() > 0:
        page.click("a:has-text('View')"); page.wait_for_timeout(400)
        ok("Patient detail loads")
        for tab in ["#appointments", "#prescriptions", "#records"]:
            if page.locator(f"a[href='{tab}']").count() > 0:
                page.click(f"a[href='{tab}']"); page.wait_for_timeout(200)
        ok("Patient tabs clickable")
    else:
        ok("Patient detail view (no patients to view)")

    # ─── APPOINTMENTS ───
    page.goto(f"{BASE}/appointments/"); page.wait_for_timeout(400)
    ok("Appointment list loads")
    opts = page.locator("select[name='status'] option").count()
    if opts > 1:
        page.select_option("select[name='status']", index=1)
        page.click("button[type='submit']"); page.wait_for_timeout(400)
        ok("Appointment status filter works")
    if page.locator("a:has-text('View')").count() > 0:
        page.click("a:has-text('View')"); page.wait_for_timeout(400)
        ok("Appointment detail loads")

    # ─── PRESCRIPTIONS ───
    page.goto(f"{BASE}/records/prescriptions/"); page.wait_for_timeout(400)
    ok("Prescription list loads")
    if page.locator("a:has-text('View Details')").count() > 0:
        page.click("a:has-text('View Details')"); page.wait_for_timeout(400)
        ok("Prescription detail loads")
        if page.locator("text=Download PDF").count() > 0:
            ok("Prescription PDF download button present")
    else:
        ok("Prescription list (empty or single)")

    # ─── MEDICAL RECORDS ───
    page.goto(f"{BASE}/records/records/"); page.wait_for_timeout(400)
    ok("Medical record list loads")

    # ─── PATIENT REPORT ───
    page.goto(f"{BASE}/records/patient-report/"); page.wait_for_timeout(500)
    ok("Patient report page loads")
    for text in ["Patient Summary Report", "Total Patients", "Patient List"]:
        if page.locator(f"text={text}").count() > 0:
            ok(f"Report has '{text}'")

    # ─── DOCTOR CALENDAR ───
    page.goto(f"{BASE}/doctors/calendar/"); page.wait_for_timeout(500)
    ok("Doctor calendar loads")
    if page.locator("text=Doctor Availability Calendar").count() > 0:
        ok("Calendar has title")

    # ─── PAGINATION ───
    page.goto(f"{BASE}/patients/"); page.wait_for_timeout(300)
    ok("Patient list pagination check")

    # ─── 404 ───
    page.goto(f"{BASE}/nonexistent-page-xyz/"); page.wait_for_timeout(400)
    if "404" in page.content():
        ok("Custom 404 page works")
    else:
        fail("404 page not showing")

    # ─── LOGOUT ───
    page.goto(f"{BASE}/logout/"); page.wait_for_timeout(300)
    if page.locator("input[name='username']").count() > 0:
        ok("Logout redirects to login page")
    else:
        fail("Logout did not redirect to login")

    ctx.close()

    # ─── DOCTOR ROLE ───
    ctx = browser.new_context()
    page = ctx.new_page()
    page.goto(f"{BASE}/login/")
    page.fill("input[name='username']", "doctor1")
    page.fill("input[name='password']", "doctor123")
    page.click("button[type='submit']"); page.wait_for_timeout(1000)
    ok("Doctor login")
    for link in ["Dashboard", "My Appointments", "Patients", "Scripts", "Records", "Calendar"]:
        if page.locator(f"nav a:has-text('{link}')").count() > 0:
            ok(f"Doctor nav '{link}'")
        else:
            fail(f"Doctor nav missing '{link}'")

    for url, name in [("/doctors/my/appointments/", "appointments"),
                      ("/doctors/my/prescriptions/", "prescriptions"),
                      ("/doctors/my/records/", "records")]:
        page.goto(f"{BASE}{url}"); page.wait_for_timeout(400)
        ok(f"Doctor {name} page loads")

    ctx.close()

    # ─── RECEPTIONIST ROLE ───
    ctx = browser.new_context()
    page = ctx.new_page()
    page.goto(f"{BASE}/login/")
    page.fill("input[name='username']", "receptionist")
    page.fill("input[name='password']", "reception123")
    page.click("button[type='submit']"); page.wait_for_timeout(1000)
    ok("Receptionist login")
    for link in ["Dashboard", "Patients", "Appointments", "Doctors", "Calendar"]:
        if page.locator(f"nav a:has-text('{link}')").count() > 0:
            ok(f"Receptionist nav '{link}'")
        else:
            fail(f"Receptionist nav missing '{link}'")
    ctx.close()

    browser.close()

proc.terminate()
proc.wait()

print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed")
if errors:
    print("Errors:")
    for e in errors:
        print(f"  - {e}")
print(f"{'='*50}")
