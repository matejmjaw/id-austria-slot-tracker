# Open ID Austria Appointment Tracker

An automated, serverless monitor that checks for open ID Austria registration slots across Vienna police stations and emails alerts immediately when an early cancellation is detected.

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
