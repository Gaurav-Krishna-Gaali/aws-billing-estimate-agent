# aws_s3_estimate.py
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
import time
import sys

def click_any(page, selectors, timeout=10000):
    """Try multiple selector/text options until one works (returns True)"""
    for s in selectors:
        try:
            page.wait_for_selector(s, timeout=timeout)
            page.click(s)
            print(f"Clicked selector: {s}")
            return True
        except PWTimeout:
            # try next
            continue
        except Exception as e:
            # sometimes clicking by text needs a locator
            try:
                page.locator(s).click(timeout=timeout)
                print(f"Clicked locator: {s}")
                return True
            except Exception:
                continue
    return False

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # set True for headless
        page = browser.new_page()

        page.goto("https://calculator.aws/", wait_until="networkidle")
        print("Opened https://calculator.aws/")

        # Give the SPA some time to initialize
        page.wait_for_timeout(2000)

        # Step 1: create estimate - try several likely texts/selectors
        created = click_any(
            page,
            [
                'text="Create estimate"',
                'text="Create new estimate"',
                'text=/Create\\s+(estimate|new estimate)/i',
                'button:has-text("Create estimate")',
                'button:has-text("Create new estimate")'
            ],
            timeout=8000
        )
        if not created:
            print("No explicit 'Create estimate' button found — continuing (estimate UI may auto-open).")

        # Wait for presence of Add / Add service / + button
        added = click_any(
            page,
            [
                'text="Add service"',
                'button:has-text("Add service")',
                'text="Add service to estimate"',
                'button[aria-label="Add service"]',
                'button:has-text("+ Add service")',
                'button:has-text("+ Add")'
            ],
            timeout=10000
        )

        if not added:
            # Try opening "Add service" via search input or Services list
            print("Could not find Add service button by direct labels — attempting to open Services panel.")
            # some UI exposes a "Browse services" or search icon
            click_any(
                page,
                [
                    'text="Browse services"',
                    'button:has-text("Browse services")',
                    'input[placeholder*="Search services"]',
                    'input[placeholder*="Find services"]'
                ],
                timeout=7000
            )

        # Allow panel to appear
        page.wait_for_timeout(1500)

        # Step: search for S3 in services search box (many UIs use a search field)
        search_success = False
        try:
            # Try common search input possibilities
            for sel in [
                'input[placeholder*="Search"]',
                'input[placeholder*="Find services"]',
                'input[placeholder*="Search services"]',
                'input[aria-label*="Search"]',
                'input[type="search"]'
            ]:
                try:
                    page.fill(sel, "S3")
                    print(f"Filled service search at {sel}")
                    page.wait_for_timeout(800)
                    # click the S3 result (try several text variants)
                    if click_any(page, ['text="Amazon Simple Storage Service (Amazon S3)"', 'text="Amazon S3"', 'text=/S3/'], timeout=4000):
                        search_success = True
                        break
                except Exception:
                    continue
        except Exception:
            pass

        if not search_success:
            # fallback: try to click any S3-like text thats visible
            if not click_any(page, ['text=/Amazon\\s+Simple\\s+Storage\\s+Service/i', 'text=/Amazon\\s+S3/i', 'text=/S3/i'], timeout=6000):
                print("Could not find S3 entry automatically. You may need to inspect the service list and update the selector.")
                # still continue — the estimate item may already be added or page structure different

        # Wait for estimate form panel to appear
        page.wait_for_timeout(1500)

        # Now attempt to fill the common fields. Labels vary between UIs; attempt several label forms.
        def try_fill_by_labels(labels, value):
            for lab in labels:
                try:
                    page.get_by_label(lab).fill(value, timeout=3000)
                    print(f"Filled '{lab}' with '{value}'")
                    return True
                except Exception:
                    continue
            return False

        # Storage amount (GB)
        storage_labels = [
            "Storage amount", "Storage (GB)", "Storage (GiB)", "Storage amount (GB)", "Storage (GB) per month", "Amount (GB)"
        ]
        if not try_fill_by_labels(storage_labels, "500"):
            # fallback: try input placeholders or numeric inputs
            for sel in ['input[placeholder*="GB"]', 'input[placeholder*="Amount"]', 'input[type="number"]']:
                try:
                    page.fill(sel, "500")
                    print(f"Filled {sel} with 500")
                    break
                except Exception:
                    continue

        # Storage class select - try label or select drop-down
        storage_class_options = ["S3 Standard", "Standard"]
        try:
            # try by label for select
            for lab in ["Storage class", "Storage class (tier)", "Storage Class"]:
                try:
                    page.get_by_label(lab).select_option(label="S3 Standard")
                    print(f"Selected S3 Standard via label '{lab}'")
                    break
                except Exception:
                    # try select elements with the label text near them
                    continue
            else:
                # fallback: open any select and try to pick by visible text
                if click_any(page, ['select[aria-label*="Storage class"]', 'select[aria-label*="Class"]'], timeout=3000):
                    page.wait_for_timeout(400)
                    # pick option via click
                    click_any(page, ['text="S3 Standard"', 'text="Standard"'], timeout=3000)
        except Exception:
            pass

        # PUT / COPY / POST / LIST Requests
        put_labels = [
            "PUT, COPY, POST, or LIST Requests", "PUT requests", "PUT, COPY, POST or LIST requests", "PUT/COPY/POST/LIST"
        ]
        if not try_fill_by_labels(put_labels, "100000"):
            # try placeholders or nearby input fields
            for sel in ['input[placeholder*="PUT"]', 'input[aria-label*="PUT"]', 'input[placeholder*="Requests"]']:
                try:
                    page.fill(sel, "100000")
                    print(f"Filled {sel} with 100000")
                    break
                except Exception:
                    continue

        # GET Requests
        get_labels = ["GET and all other Requests", "GET requests", "GET and all other requests", "GET"]
        if not try_fill_by_labels(get_labels, "200000"):
            for sel in ['input[placeholder*="GET"]', 'input[aria-label*="GET"]']:
                try:
                    page.fill(sel, "200000")
                    print(f"Filled {sel} with 200000")
                    break
                except Exception:
                    continue

        # Give the calculator a moment to recalc
        page.wait_for_timeout(3000)

        # Screenshot full page or a specific estimate panel if you know the selector
        try:
            # if you know an estimate panel selector, replace below with that selector
            page.screenshot(path="s3_estimate.png", full_page=True)
            print("✅ Screenshot saved as s3_estimate.png")
        except Exception as e:
            print("Could not full-page screenshot:", e)
            # try screenshotting viewport
            page.screenshot(path="s3_estimate_viewport.png")
            print("Saved viewport screenshot as s3_estimate_viewport.png")

        browser.close()

if __name__ == "__main__":
    run()
