# Open ID Austria Appointment Tracker

An automated, serverless monitor that checks for open ID Austria registration slots across Vienna police stations and emails alerts immediately when an early cancellation is detected.

## Why?
As a non-Austrian resident living in Vienna, securing an ID Austria registration appointment through official channels often means facing months-long waiting lists or endless manual page refreshing. This tool automates the process entirely on free cloud infrastructure, scanning every 10 minutes to notify you the exact moment an early cancellation drops so you can secure a spot immediately.

## How It Works
- **Automated Cloud Polling**: Runs on a 10-minute cron schedule via GitHub Actions entirely on free cloud infrastructure.
- **Smart Filtering**: Simulates form submissions across all Vienna police precincts, parsing availability tables to look exclusively for slots within your 30-day window.
- **Instant Direct Alerts**: Sends an encrypted email straight to your personal inbox the microsecond an early cancellation drops so you can beat everyone else to the booking link.

## Setup Instructions

### 1. Generate a Gmail App Password
Because Google requires 2-Step Verification to use App Passwords, follow these steps:
1. Go to your [Google Account Security Page](https://myaccount.google.com/security).
2. Ensure **2-Step Verification** is turned **On**.
3. In the search bar at the top of the Google Account page, search for **App passwords** and click it.
4. Enter an app name (e.g., `GitHub Tracker`) and click **Create**.
5. Copy the generated **16-character code** (you will use this for your repository secrets).

### 2. Configure Repository Secrets
Add the following secrets under your repository **Settings > Secrets and variables > Actions**:
- `EMAIL_USER`: Your full Gmail address (used to send alerts).
- `EMAIL_PASS`: Your 16-character Gmail App Password.
- `NOTIFICATION_TO`: Your real personal email address where you want to receive slot notifications.
- `USER_EMAIL`: A dummy placeholder email (e.g., `wile-e.coyote@acme.com`) submitted to the BMI form payload.
- `USER_LASTNAME`: `coyote` (dummy text for the form)
- `USER_FIRSTNAME`: `wile-e` (dummy text for the form)
- `USER_DOB`: `01.01.2000` (dummy text for the form)
